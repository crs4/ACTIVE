"""
This module contains all class necessary to define a REST API for Audio item objects.
It is possible to list all stored Audio item objects and apply CRUD operation of Audio
items, providing an id when necessary.
All Audio items data is provided and requested in JSON format.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.audio.models import AudioItem
from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


# used to handle the concurrent update of an Audio object.
import threading
edit_lock = threading.Lock()


class AudioItemList(EventView):
    """
    This class implements the views necessary to list
    all stored audio digital items in a serialized format.
    Moreover it defines an HTTP method for the creation of a
    new AudioItem objects through the REST API.
    """
    model = AudioItem

    def get(self, request, format=None):
        """
        Method used to retrieve all data about stored audio items.
        All data is returned in a JSON format (serialized).

        @param request: HttpRequest object used to retrieve all AudioItems.
        @type request: HttpRequest
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all requested audio items data.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored AudioItem objects')
        audio = AudioItem.objects.all()
        paginator = AudioItemPagination()
        result = paginator.paginate_queryset(audio, request)
        serializer = AudioItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used create a new AudioItem object.
        All data is provided in a JSON format (serialized) an then is
        converted in an object that will be saved in the database.

        @param request: HttpRequest object containing all AudioItem data.
        @type request: HttpRequest
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the id of the new AudioItem object or an error.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new AudioItem object')
        serializer = AudioItemSerializer(data=request.data)
        if request.FILES and request.FILES['file'].content_type.split('/')[0] != 'audio' :
            logger.error('File missing or content type not supported for AudioItem')
            return Response('Content type not supported', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            logger.debug('New AudioItem object saved - ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for AudioItem object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioItemDetail(EventView):
    """
    This module implement all methods necessary to retrieve, update or
    delete a AudioItem object providing its id.
    """
    model = AudioItem

    def get_object(self, pk):
        """
        Method used retrieve a AudioItem object from its id.

        @param pk: AudioItem primary key used to retrieve the object.
        @type pk: int
        @return: AudioItem object corresponding to the provided id.
        @rtype: AudioItem
        """
        try:
            return AudioItem.objects.get(item_ptr_id = pk)
        except AudioItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve data about a specific AudioItem object.

        @param request: HttpRequest object used to retrieve an AudioItem.
        @type request: HttpRequest
        @param pk: Audio's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the requested audio item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        logger.debug('Requested AudioItem object ' + str(pk))
        item = self.get_object(pk)
        serializer = AudioItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a specific AudioItem object data
        providing serialized updated data.

        @param request: HttpRequest object containing the updated AudioItem fields.
        @type request: HttpRequest
        @param pk: Audio's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the uploaded audio item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on AudioItem object ' + str(pk))
        with edit_lock:
            item = self.get_object(pk)
            serializer = AudioItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('AudioItem object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for AudioItem object ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete data of a specific AudioItem object providing its id.

        @param request: HttpRequest object used to delete a AudioItem object.
        @type request: HttpRequest
        @param pk: Audio Item's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of the item deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on AudioItem object ' + str(pk))
        item = self.get_object(pk)
        item.delete()
        logger.debug('AudioItem object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)