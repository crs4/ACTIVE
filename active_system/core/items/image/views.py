"""
This module contains all classes and methods used to define a REST API
for ImageItem objects. In this module it has been defined the methods
used to retrieve all stored ImageItem objects and CRUD methods. providing
an id if requested.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.image.models import ImageItem
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class ImageItemList(EventView):
    """
    This class provides all views necessary to list all available
    ImageItem objects and to create and store a new one, providing necessary data.
    """
    model = ImageItem

    def get(self, request, format=None):
        """
        Method used to retrieve all stored ImageItem objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest used to retrieve all ImageItem objects.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized ImageItem objects.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored ImageItem objects')
        images = ImageItem.objects.all()
        paginator = ImageItemPagination()
        result = paginator.paginate_queryset(images, request)
        serializer = ImageItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new ImageItem object.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide ImageItem data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new ImageItem object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new ImageItem object')
        serializer = ImageItemSerializer(data=request.data)
        if request.FILES and request.FILES['file'].content_type.split('/')[0] != 'image' :
            logger.error('File missing or content type not supported')
            return Response('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            logger.debug('New ImageItem object saved - ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for ImageItem object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageItemDetail(EventView):
    """
    This class implements all methods necessary to retrieve, update or
    delete a ImageItem instance, providing its id.
    """
    model = ImageItem

    def get_object(self, pk):
        """
        Method used to retrieve an ImageItem object by its id.

        @param pk: ImageItem's primary key.
        @type pk: int
        @return: Object containing the item retrieve data, error otherwise.
        @rtype: ImageItem
        """
        try:
            return ImageItem.objects.get(item_ptr_id = pk)
        except ImageItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific ImageItem object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of an ImageItem object.
        @type request: HttpRequest
        @param pk: ImageItem primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested ImageItem object ' + str(pk))
        item = self.get_object(pk)
        serializer = ImageItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update an ImageItem object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated ImageItem field data.
        @type request: HttpRequest
        @param pk: ImageItem primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """

        print request.auth
        print request.META['HTTP_AUTHORIZATION']

        logger.debug('Requested edit on ImageItem object ' + str(pk))
        with edit_lock:
            item = self.get_object(pk)
            serializer = ImageItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('ImageItem object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for ImageItem object ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete an ImageItem object providing its id.

        @param request: HttpRequest used to delete an ImageItem object.
        @type request: HttpRequest
        @param pk: ImageItem primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on ImageItem object ' + str(pk))
        item = self.get_object(pk)
        item.delete()
        logger.debug('ImageItem object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
