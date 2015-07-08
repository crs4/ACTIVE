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

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
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
        logger.debug('Requested all stored Keyword objects')
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
        logger.debug('Requested Keyword objects ' + str(pk))
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
        logger.debug('Requested edit on Keyword object ' + str(pk))
        with edit_lock:
            keyword = self.get_object(pk)
            serializer = KeywordSerializer(keyword, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Keyword object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for Keyword object ' + str(pk))
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
        logger.debug('Requested delete on Keyword object ' + str(pk))
        keyword = self.get_object(pk)
        keyword.delete()
        logger.debug('Keyword object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class KeywordFind(EventView):
    """
    This class defines all methods necessary to find a Keyword object
    providing its character sequence.
    This approach is useful in order to create the minimum number of
    keyword stored in the db.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

    def get(self, request, value, format=None):
        """
        Method used to retrieve an existing Keyword object,
        providing its character value.
        The object is serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword.
        @type request: HttpRequest
        @param value: The string associated to a keyword.
        @type value: string
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.
        @rtype: HttpResponse
        """
        logger.debug('Searching a Keyword object with value ' + value)
        try:
            k = Keyword.objects.filter(description = value)
            if k and len(k) > 0:
                logger.debug('Find Keyword object ' + str(k[0].pk) + ' for value ' + value)
                serializer = KeywordSerializer(k[0])
                return Response(serializer.data)

            logger.error('No Keyword object found for value ' + value)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Http404


class KeywordSearch(EventView):
    """
    This class provides the methods necessary to search a specific keywords (if any)
    associated to a generic digital item.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

    def get(self, request, item_type, keyword_list,  format=None):
        """
        Method used to retrieve all stored Keyword objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword.
        @type request: HttpRequest
        @param item_type: The type of digital item searched.
        @type item_type: string
        @param keyword_list: The keywords that will be searched in the selected digital items.
        @type keyword_list: List of strings
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.
        @rtype: HttpResponse
        """
        logger.debug('Searching all Item objects associated to keyword list ' + keyword_list)
        # create a map to specific item object handlers
        item_map = { "audio" : [AudioItem, AudioItemSerializer, AudioItemPagination],
                     "image" : [ImageItem, ImageItemSerializer, ImageItemPagination],
                     "video" : [VideoItem, VideoItemSerializer, VideoItemPagination] }

        # check if the item type is supported
        if item_type not in item_map:
            logger.error('Provided item type for search is not supported - ' + item_type)
            return Response({'error' : 'The specified item type is not supported.'}, status=status.HTTP_400_BAD_REQUEST)

        # all items are returned if there is no keyword
        if len(keyword_list) == 0:
            logger.debug('Returned all Item objects of type ' + item_type)
            return Response(ItemSerializer(Item.objects.filter(type = item_type), many=True).data)

        item_list = []
        # retrieve the provided keywords (if they exist)
        keyword_list = set(keyword_list.strip().lower().replace(' ', '_').split(','))
        for k in keyword_list:
            keywords = Keyword.objects.filter(description__icontains = k)

            # retrieve all tags associated to each keyword
            temp = []
            for k2 in keywords:
                tags = Tag.objects.filter(entity__id = k2.id)
                temp += ([t.item.id for t in tags])
            item_list.append(temp)
        
        # intersect the list of item ids
        ids = set(item_list[0])
        for i in range(1, len(item_list)):
            ids = ids.intersection(item_list[i])

        # return the retrieved list of specific digital items
        logger.debug('Returning all Item objects found for keyword list ' + str(keyword_list))
        items = item_map[item_type][0].objects.filter(item_ptr_id__in = ids)


        paginator = item_map[item_type][2]()
        result = paginator.paginate_queryset(items, request)
        serializer = item_map[item_type][1](result, many=True)
        return paginator.get_paginated_response(serializer.data)




class KeywordsItem(EventView):


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
                item = Item.objects.get(pk = pk)
            except Item.DoesNotExist:
                raise Http404
                
        
            tags = Tag.objects.filter(item_id = item.id).filter(type = 'keyword')
            entities_ids_list = []
            if tags:
                entities_ids_list += ([t.entity.id for t in tags])
                keywords = Keyword.objects.filter(entity_ptr_id__in = entities_ids_list)
                serializer = KeywordSerializer(keywords, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            return Response([],status=status.HTTP_200_OK)
            

            

