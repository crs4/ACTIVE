# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all class that will implement all methods required by the
REST API for Tag objects manipulation.
These classes allow to retrieve all available Tag objects and invoke CRUD
operations over them.
"""


from core.views import EventView
from core.items.models import Item
from core.items.audio.models import AudioItem
from core.items.image.models import ImageItem
from core.items.video.models import VideoItem
from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination
from core.tags.models import Tag, Entity
from core.tags.serializers import TagSerializer
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import status
import logging
import threading

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
edit_lock = threading.Lock()

def check_tags(tag, user):
    """
    Check if there are multiple tags similar to the current one.
    If any remove the old one and maintain the current one.

    @param tag: Tag object used for search
    @type tag: Tag
    @return: Result of the search.
    @rtype: boolean
    """
    res = Tag.user_objects.by_user(user).filter(entity_id = tag.entity.pk, item_id = tag.item.pk, type = tag.type).exclude(pk = tag.pk)
    if len(res) == 0:
        return True

    # associate all dynamic tags to one tag
    for _tag in res:
        for _dtag in _tag.dynamictag_set.all():
            _dtag.tag = tag
            _dtag.save()

    # remove duplicate tags
    for _tag in res:
        # delete the entity if there are no tags associated to it
        if Tag.user_objects.by_user(user).filter(entity_id = _tag.entity.pk).count() == 0:
            _tag.entity.delete()
        _tag.delete()

    return False


class TagList(EventView):
    """
    This class is used to implement methods necessary to obtain all Tag objects
    and create a new one with provided JSON serialized data.
    """
    queryset = Tag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        Method used to retrieve all stored DynamicTags.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all DynamicTags.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized DynamicTags.
        @rtype: HttpResponse
        """
        logger.debug('Requested all Tag objects')
        tag = Tag.user_objects.by_user(request.user).all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new Tag object.
        The object data is provided in a serialized format.
        If a similar Tag object (same entity, item and type) exists
        it must be returned instead of creating a new one.

        @param request: HttpRequest used to provide tag data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new Tag object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Check if a similar Tag object exists')
        item   = request.data.get('item', '')
        entity = request.data.get('entity', '')
        type   = request.data.get('type', '')
        serializer = None
	
	item_obj = Item.user_objects.by_user(request.user).get(pk = item)
	if not(item_obj.owner == request.user):
	    Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)  
      
        tag = Tag.user_objects.by_user(request.user).filter(item_id=item, entity_id=entity, type=type)
        if len(tag) > 0:
            logger.debug('Returned an existing Tag object ' + str(item) + ' ' + str(entity) + ' ' + str(type))
            serializer = TagSerializer(tag[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug('Creating a new Tag object')
            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.debug('New Tag object saved - ' + str(serializer.data['id']))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for Tag object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(EventView):
    """
    This class is used to implement methods necessary to retrieve, update or
    delete a Tag object providing its id and additional required data.
    """
    queryset = Tag.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk, user):
        """
        Method used to retrieve a Tag object by its id.

        @param pk: Tag primary key.
        @type pk: int
        @return: Object containing the tag retrieved data, error otherwise.
        @rtype: Tag
        """
        try:
            return Tag.user_objects.by_user(user).get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific Tag object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a Tag object
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data
        @type pk: int
        @param format: Format used for data serialization
        @type format: string
        @return: HttpResponse containing the serialized data
        @rtype: HttpResponse
        """
        logger.debug('Requested Tag object ' + str(pk))
        tag = self.get_object(pk, request.user)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a Tag object, providing its id
        and updated data in a serialized form.

        @param request: HttpRequest containing the updated Tag field data.
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized updated data
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on Tag object with id ' + str(pk))
        with edit_lock:
            tag = self.get_object(pk, request.user)
            serializer = TagSerializer(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Updated data of Tag object with id ' + str(pk))
                check_tags(tag, request.user)
                return Response(serializer.data)

            logger.error('Error on data update of Tag object with id ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a DynamicTag object providing its id.

        @param request: HttpRequest used to delete a DynamicTag object.
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on Tag object with id' + str(pk))
        tag = self.get_object(pk, request.user)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,data={'id': pk})
