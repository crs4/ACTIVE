"""
This module contains all class that will implement methods required by the
REST API for Person object data.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.tags.person.models import Person
from core.tags.person.serializers import PersonSerializer

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class PersonList(EventView):
    """
    This class provides the methods necessary to list all available
    Person objects and to create and store a new one, providing necessary data.
    """

    def get(self, request, format=None):
        """
        Method used to retrieve all stored Person objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Person.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Person.
        @rtype: HttpResponse
        """
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new Person object.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide person data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new Person object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(EventView):
    """
    Retrieve, update or delete a Person instance.
    """

    def get_object(self, pk):
        """
        Method used to retrieve a Person object by its id.

        @param pk: Person object primary key.
        @type pk: int
        @return: Object containing the person retrieved data, error otherwise.
        @rtype: Person
        """
        try:
            return Person.objects.get(entity_ptr_id = pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific Person object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a Person object.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a Person object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated Person field data.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        with edit_lock:
            person = self.get_object(pk)
            serializer = PersonSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a Person object providing its id.

        @param request: HttpRequest used to delete a Person object.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonImage(EventView):

    def get(self, request, pk, format=None):
        """

        :param request:
        :param pk:
        :param format:
        :return:
        """
        try:
            p = Person.objects.get(pk=pk)
            return HttpResponse(p.image, content_type = 'image/jpg')
        except Exception as e:
            raise Http404
