"""
This module contains all class that will implement all methods required by the
REST API for Tag objects manipulation.
These classes allow to retrieve all available Tag objects and invoke CRUD
operations over them.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.models import Item
from core.items.audio.models import AudioItem
from core.items.image.models import ImageItem
from core.items.video.models import VideoItem
from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination

from core.tags.models import Tag, Entity
from core.tags.serializers import TagSerializer
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


def check_tags(tag):
    """
    Check if there are multiple tags similar to the current one.
    If any remove the old one and maintain the current one.

    @param tag: Tag object used for search
    @type tag: Tag
    @return: Result of the search.
    @rtype: boolean
    """

    res = Tag.objects.filter(entity_id = tag.entity.pk, item_id = tag.item.pk, type = tag.type).exclude(pk = tag.pk)
    if len(res) == 0:
        return True

    # associate all dynamic tags to one tag
    # TODO ripulire il codice!!! Dipendenza da dtags
    for _tag in res:
        for _dtag in _tag.dynamictag_set.all():
            _dtag.tag = tag
            _dtag.save()

    # remove duplicate tags
    for _tag in res:
        # delete the entity if there are no tags associated to it
        if Tag.objects.filter(entity_id = _tag.entity.pk).count() == 0:
            _tag.entity.delete()
        _tag.delete()

    return False


class TagList(EventView):
    """
    This class is used to implement methods necessary to obtain all Tag objects
    and create a new one with provided JSON serialized data.
    """
    model = Tag

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
        logger.debug('Requested all stored Tag objects')
        tag = Tag.objects.all()
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

        tag = Tag.objects.filter(item_id=item, entity_id=entity, type=type)
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
    model = Tag

    def get_object(self, pk):
        """
        Method used to retrieve a Tag object by its id.

        @param pk: Tag primary key.
        @type pk: int
        @return: Object containing the tag retrieved data, error otherwise.
        @rtype: Tag
        """
        try:
            return Tag.objects.get(pk=pk)
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
        tag = self.get_object(pk)
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
        logger.debug('Requested edit on Tag object ' + str(pk))
        with edit_lock:
            tag = self.get_object(pk)
            serializer = TagSerializer(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Tag object ' + str(pk) + ' successfully edited')
                check_tags(tag)
                return Response(serializer.data)

            logger.error('Provided data not valid for Tag object ' + str(pk))
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
        logger.debug('Requested delete on Tag object ' + str(pk))
        tag = self.get_object(pk)
        
            
        tag.delete()
        logger.debug('Tag object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchTagItem(EventView):
    """
    Class used to implement methods necessary to search all Tags
    objects associated to a specific digital item.
    """
    model = Tag

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all Tag objects containing
        the occurrences in a specific digital item (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Item object primary key, used to retrieve tag data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Searching all Tag objects associated to Item object ' + str(pk))
        tag = Tag.objects.filter(item__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)


class SearchTagPerson(EventView):
    """
    Class used to implement methods necessary to search all Tags objects
    associated to a specific person.
    """
    model = Tag

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all Tag objects containing
        the occurrences of a specific person (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Searching all Tag objects associated to Entity object ' + str(pk))
        tag = Tag.objects.filter(entity__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)


# ha senso una funziona del genere? molti riferimenti ad altri moduli e
# si chiedere al server di bufferizzare i risultati invece di lasciare che
# sia il client a richiederli uno per volta.
class SearchItemByEntity(EventView):
    """
    Class used to implement methods necessary to search all Item objects
    of a specific type associated to a specific Entity.
    """
    model = Tag

    def get(self, request, item_type, pk,  format=None):
        """
        Method used to retrieve all Item objects containing
        the occurrences of a specific person (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param item_type: Type of the requested item.
        @type item_type: string
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Searching all Item objects associated to Entity object ' + str(pk) + ' with type ' + item_type)

        item_map = {'audio' : [AudioItem, AudioItemSerializer, AudioItemPagination],
                    'image' : [ImageItem, ImageItemSerializer, ImageItemPagination],
                    'video' : [VideoItem, VideoItemSerializer, VideoItemPagination]}
        # check if the requested item is valid
        if item_type not in item_map:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # retrieve items object by their tags
        tags = Tag.objects.filter(entity = pk)
        items = []
        for tag in tags:
            print str(tag), str(tag.item), str(tag.entity)
            item = Item.objects.get(pk=tag.item.id)
            if item.type == item_type:
                print 'item selected'
                items.append(item_map[item_type][0].objects.get(item_ptr_id=tag.item))
        # return the retrieved items in a serialized and paginated format
        paginator = item_map[item_type][2]()
        result = paginator.paginate_queryset(items, request)
        serializer = item_map[item_type][1](result, many=True)
        return paginator.get_paginated_response(serializer.data)
