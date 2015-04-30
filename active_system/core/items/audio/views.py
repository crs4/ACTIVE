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
        serializer = AudioItemSerializer(data=request.data)
        if request.FILES and request.FILES['file'].content_type.split('/')[0] != 'audio' :
            return Response('Content type not supported', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioItemDetail(EventView):
    """
    Retrieve, update or delete a Audio item object providing its id.
    """

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
        Method used to retrieve data about a specific audio item.

        @param request: HttpRequest object used to retrieve an AudioItem.
        @type request: HttpRequest
        @param pk: Audio's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the requested audio item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        item = self.get_object(pk)
        serializer = AudioItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update the audio item information providing
        serialized fresh data.

        @param request: HttpRequest object containing the updated AudioItem fields.
        @type request: HttpRequest
        @param pk: Audio's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the uploaded audio item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        with edit_lock:
            item = self.get_object(pk)
            serializer = AudioItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete user information providing his ID.

        @param request: HttpRequest object used to delete a AudioItem object.
        @type request: HttpRequest
        @param pk: Audio Item's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of the item deletion.
        @rtype: HttpResponse
        """
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)