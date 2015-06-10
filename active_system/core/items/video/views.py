"""
This module has been defined in order to handle VideoItem objects data through a REST API.
It is possible to invoke CRUD methods on VideoItem objects, providing an id if necessary,
or retrieve all stored objects.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.video.models import VideoItem
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

import threading
edit_lock = threading.Lock()


class VideoItemList(EventView):
    """
    This class implements two methods necessary to list all VideoItems objects
    and to create and store a new VideoItem object.
    """
    model = VideoItem

    def get(self, request, format=None):
        """
        Method used to list all stored VideoItem objects.
        Objects data is returned in a JSON serialized format and paginated.

        @param request: HttpRequest used to retrieve VideoItem objects data.
        @type request: HttpRequest
        @param format: The format used to serialize objects data, JSON by default.
        @type format: string
        @return: HttpResponse containing all serialized data of retrieved VideoItem objects.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored VideoItem objects')
        items = VideoItem.objects.all()
        paginator = VideoItemPagination()
        result = paginator.paginate_queryset(items, request)
        serializer = VideoItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create and store a new VideoItem object with the provided data.

        @param request: HttpRequest containing the serialized data that will be used to create a new VideoItem object.
        @type request: HttpRequest
        @param format: The format used to serialize objects data, JSON by default.
        @type format: string
        @return: HttpResponse containing the id of the new created VideoItem object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new VideoItem object')
        serializer = VideoItemSerializer(data=request.data)
        if request.FILES and request.FILES['file'].content_type.split('/')[0] != 'video' :
            logger.error('File missing or content type not supported')
            return Response('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            logger.debug('New VideoItem object saved ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for VideoItem object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoItemDetail(EventView):
    """
    Retrieve, update or delete a video item instance.
    """
    model = VideoItem

    def get_object(self, pk):
        """
        Method used to retrieve a VideoItem object using its id.

        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @return: VideoItem object retrieved by the provided id, error if it isn't available.
        @rtype: VideoItem
        """
        try:
            return VideoItem.objects.get(item_ptr_id = pk)
        except VideoItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve data of an existing VideoItem object.
        The retrieved data is returned in a serialized format, JSON by default.

        @param request: HttpRequest containing the updated VideoItem field data.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all serialized data of a VideoItem, error if it isn't available.
        @rtype: HttpResponse
        """
        logger.debug('Requested VideoItem object ' + str(pk))
        item = self.get_object(pk)
        serializer = VideoItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update stored information of a specific VideoItem object.
        The fresh data is provided in a serialized format.

        @param request: HttpRequest containing the updated VideoItem field data.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all update object data.
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on VideoItem object ' + str(pk))
        with edit_lock:
            item = self.get_object(pk)
            serializer = VideoItemSerializer(item, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('VideoItem object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for VideoItem object ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete data about a specific VideoItem object, providing its id.

        @param request: HttpRequest used to delete a specific VideoItem.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on VideoItem object ' + str(pk))
        item = self.get_object(pk)
        item.delete()
        logger.debug('VideoItem object' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
