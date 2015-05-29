"""
This module contains all class that will implement all methods required by the
REST API for tags object data.
These classes allow to retrieve all available Tag objects and invoke CRUD
operations over them, providing a id if needed.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status
 
from core.tags.models import Tag
from core.tags.serializers import TagSerializer

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class TagList(EventView):
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
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new DynamicTag object.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide tag data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new DynamicTag object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(EventView):
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

        @param request: HttpRequest used to retrieve data of a Tag object.
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a DynamicTag object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated Tag field data.
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        with edit_lock:
            tag = self.get_object(pk)
            serializer = TagSerializer(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
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
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchTagItem(EventView):
    """
    Class used to implement methods necessary to search all Tags
    objects associated to a specific digital item.
    """

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
        tag = Tag.objects.filter(item__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)


class SearchTagPerson(EventView):
    """
    Class used to implement methods necessary to search all Tags objects
    associated to a specific person.
    """

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all DynamicTag objects containing
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
        tag = Tag.objects.filter(entity__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)