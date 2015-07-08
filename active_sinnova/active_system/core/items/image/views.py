"""
This module contains all classes and methods used to define a REST API
for Image item objects. In this module it has been defined the methods
used to retrieve all stored Image item objects and CRUD methods. providing
an id if requested.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.image.models import ImageItem
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()

class ImageItemList(EventView):
    """
    This class provides all views necessary to list all available
    ImageItems and to create and store a new one, providing necessary data.
    """
    queryset = ImageItem.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        Method used to retrieve all stored ImageItems.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all ImageItems.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized ImageItems.
        @rtype: HttpResponse
        """

        images = ImageItem.objects.all()
        paginator = ImageItemPagination()
        result = paginator.paginate_queryset(images, request)
        serializer = ImageItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new ImageItem object.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide item data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new ImageItem object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = ImageItemSerializer(data=request.data)

        if request.FILES and request.FILES['file'].content_type.split('/')[0] != 'image' :
            return Response('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageItemDetail(EventView):
    """
    Retrieve, update or delete a ImageItem instance.
    """

    queryset = ImageItem.objects.none()  # required for DjangoModelPermissions

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
        with edit_lock:
            item = self.get_object(pk)
            serializer = ImageItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print serializer.data, '\n\n\n'
                return Response(serializer.data)
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
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
