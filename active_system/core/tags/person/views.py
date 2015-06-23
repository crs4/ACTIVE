"""
This module contains all methods necessary to implement a REST API for Person object data.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.tags.person.models import Person
from core.tags.person.serializers import PersonSerializer
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


def find_person(first_name, last_name):
    """
    Check if the user already exists based on the first and last name.
    A boolean value is returned based on the size of the result set.

    @param first_name: First name of the person searched
    @type first_name: string
    @param last_name: Last name of the persona searched
    @type last_name: string
    @return: The result of the uniqueness search
    @rtype: boolean
    """
    res = Person.objects.filter(first_name__iexact = first_name).filter(last_name__iexact= last_name)
    if res or len(res):
        logger.debug('Retrieved a Person object with name ' + res[0].first_name + ' ' + res[0].last_name)
        return res[0]

    logger.debug('No Person object found with name ' + first_name + ' ' + last_name)
    return None


class PersonList(EventView):
    """
    This class provides the methods necessary to list all available
    Person objects and to create and store a new one, providing required data.
    """
    model = Person

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
        logger.debug('Requested all stored Person objects')
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
        logger.debug('Creating a new Person object')

        # look for an already existing person with the same name
        person = find_person(request.data["first_name"], request.data["last_name"])
        if person is not None:
            logger.debug('Returned Person object ' + str(person.id) + ' - ' + person.first_name + ' ' + person.last_name)
            return Response(PersonSerializer(person).data, status=status.HTTP_201_CREATED)

        # if the person doesn't exist create a new one
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('New Person object saved - ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.debug('Provided data not valid for Person object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(EventView):
    """
    This class implements all methods necessary to retrieve, update or
    delete a Person object providing its id and required data.
    """
    model = Person

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
        logger.debug('Requested Person object ' + str(pk))
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
        @return: HttpResponse containing the Person object updated data, None in case of error
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on Person object ' + str(pk))
        with edit_lock:
            # check if there is already a person with the same name
            if 'first_name' in request.data and 'last_name' in request.data:
                person2 = find_person(request.data['first_name'], request.data['last_name'])
                if person2:
                    logger.debug('Returned Person object ' + str(person2.pk))
                    return Response(PersonSerializer(person2).data)

            # otherwise edit and return the current object
            person = self.get_object(pk)
            serializer = PersonSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Person object ' + str(pk) + ' successfully updated')
                return Response(serializer.data)

            logger.error('Provided data not valid for Person object ' + str(pk))
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
        logger.debug('Requested delete on Person object ' + str(pk))
        person = self.get_object(pk)
        person.delete()
        logger.debug('Person object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonImage(EventView):
    """
    Class used to implement the method necessary to retrieve the image
    associated to a specific person.
    """
    model = Person

    def get(self, request, pk, format=None):
        """
        Method used to retrieve the image associated to a specific Person object
        providing its id.

        @param request: HttpRequest used to obtain the Person object image
        @type request: HttpRequest
        @param pk: Id of the considered Person object
        @type: int
        @param format: Format of the serialized Person object image
        @type format: string
        @return: HttpResponse containing the image associate to the Person object
        @rtype: HttpResponse
        """
        logger.debug('Requested Person object ' + str(pk) + ' image')
        p = Person.objects.get(pk=pk)
        return HttpResponse(p.image, content_type='image/jpg')


class PersonSearch(EventView):
    """
    Class used to implement the method necessary to retrieve an existing person from
    its full name.
    """
    model = Person

    def get(self, request, first_name, last_name, format=None):
        """
        Method used to retrieve a Person object providing the full name of a person.
        It returns None if there is no person associated to this name.

        @param request: HttpRequest used to obtain the Person object
        @type request: HttpRequest
        @param first_name: First name of the searched person.
        @type: string
        @param last_name: Last name of the searched person.
        @type: string
        @param format: Format of the serialized Person object image
        @type format: string
        @return: HttpResponse containing the retrieved Person object
        @rtype: HttpResponse
        """
        logger.debug('Requested Person object with name ' + first_name + ' ' + last_name)
        res = find_person(first_name, last_name)

        if not res:
            return Response(status=status.HTTP_404_NOT_FOUND)

        person = Person.objects.get(pk=res.pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)