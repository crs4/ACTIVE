# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all class that will implement methods required by the
REST API for Keyword object data.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.tags.keywords.models import Keyword
from core.tags.keywords.serializers import KeywordSerializer

from core.tags.models import Tag
from core.items.models import Item
from core.items.serializers import ItemSerializer

from core.items.audio.models import AudioItem
from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination

from core.items.image.models import ImageItem
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination

from core.items.video.models import VideoItem
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination
import logging
import threading

# variable used for logging purposes
logger = logging.getLogger('active_log')

# used to solve the concurrent acccess to item objects
edit_lock = threading.Lock()

def find_keyword(desc):
    """
    Function used to detect if a keyword already exists by its description.
    """
    if Keyword.objects.filter(description__iexact = desc).count() > 0:
        return Keyword.objects.filter(description__iexact = desc)[0]
    return None


class KeywordList(EventView):
    """
    This class provides the methods necessary to list all available
    Keyword objects and to create and store a new one, providing necessary data.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        Method used to retrieve all stored Keyword objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword objects.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.
        @rtype: HttpResponse
        """
        logger.debug('Requested all Keyword objects')
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new Keyword object.
        If the provided keyword already exists, the existing one is returned.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide keywords data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new Keyword object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new Keyword object')
        
        if 'description' in request.data:
            kw = find_keyword(request.data['description'])
            if kw:
                serializer = KeywordSerializer(kw)
                logger.debug('Keyword object found for string - ' + str(kw.description))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            serializer = KeywordSerializer(data=request.data)
            if serializer.is_valid() :
                serializer.save()
                logger.debug('New Keyword object saved ')
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for Keyword object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeywordDetail(EventView):
    """
    This class implements the methods necessary to retrieve, update or
    delete a Keyword instance providing its id and additional data.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        """
        Method used to retrieve a Keyword object by its id.

        @param pk: Keyword object primary key.
        @type pk: int
        @return: Object containing the keywords retrieved data, error otherwise.
        @rtype: Keyword
        """
        try:
            return Keyword.objects.get(entity_ptr_id = pk)
        except Keyword.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific Keyword object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a Keyword object.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested details for Keyword object with id ' + str(pk))
        keyword = self.get_object(pk)
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a Keyword object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated Keyword field data.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        with edit_lock:
            # check if the keyword already exists
            if 'description' in request.data:
                kw = find_keyword(request.data['description'])
                if kw:
                    serializer = KeywordSerializer(kw)
                    logger.debug('Keyword object found for string - ' + str(kw.description))
                    return Response(serializer.data, status=status.HTTP_200_OK)

            keyword = self.get_object(pk)
            serializer = KeywordSerializer(keyword, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Updated data for Keyword object with id ' + str(pk))
                return Response(serializer.data)

            logger.error('Error on update of Keyword object with id' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a Keyword object providing its id.

        @param request: HttpRequest used to delete a Keyword object.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on Keyword object with id ' + str(pk))
        keyword = self.get_object(pk)
        keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'id': pk})


class KeywordsItem(EventView):
        """
        This class is used to implement a method necessary to retrieve all item objects
        associate to a given keyword.
        """

        queryset = Keyword.objects.none()  # required for DjangoModelPermissions
    
        def get(self, request, pk, format=None):
            """
            Method used to retrieve all existing Keyword objects,
            associated with a given item.
            Objects are serialized in a JSON format and then returned.

            @param request: HttpRequest use to retrieve all Keyword.
            @type request: HttpRequest
            @param pk: Item primary key used to retrieve all Keywords associated with it.
            @type pk: int	    
            @param format: The format used for object serialization.
            @type format: string
            @return: HttpResponse containing all serialized Keyword.
            @rtype: HttpResponse
            """
            
            item = None
            try:
                item = Item.user_objects.by_user(request.user).get(pk = pk)
            except Item.DoesNotExist:
                raise Http404
                
        
            tags = Tag.user_objects.by_user(request.user).filter(item_id = item.id).filter(type = 'keyword')
            entities_ids_list = []
            if tags:
                logger.debug('Retrieving all items associated to Keyword object with id ' + str(pk))
                entities_ids_list += ([t.entity.id for t in tags])
                keywords = Keyword.objects.filter(entity_ptr_id__in = entities_ids_list)
                serializer = KeywordSerializer(keywords, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            logger.warning('No items associated to Keyword object with id ' + str(pk))
            return Response([],status=status.HTTP_200_OK)
