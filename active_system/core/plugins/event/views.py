"""
This module contains all classes and methods needed to retrieve all Event objects
and invoke CRUD operations on a Event object, providing its id and required additional data.
"""

from django.http import HttpResponse, Http404

from core.plugins.models import Event
from core.plugins.event.serializers import EventSerializer
from core.plugins.script.serializers import ScriptSerializer

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class EventList(EventView): 
    """
    This class implements all methods necessary to list all stored Event objects or
    create a new one providing the serialized data.
    """
    model = Event

    def get(self, request, format=None):
        """
        This method is used to retrieve all stored Event objects.
        Objects are returned in a serialized format, JSON by default.

        @param request: HttpRequest used to retrieve all stored Event objects.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing all serialized data.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored Event objects')
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        This method is used to create and store a new Event object.
        All required data is provided in a JSON serialized format.

        @param request: HttpRequest containing all data for the new Event object.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing the id of the new object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new Event object')
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('New Event object saved - ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for Event object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(EventView): 
    """
    This class implements all methods necessary to retrieve, update or
    delete a Event object providing its id and required JSON formatted data.
    """
    model = Event

    def get_object(self, pk):
        """
        Method used to retrieve a Event object using its id.

        @param pk: Primary key used to retrieve a Event object.
        @type pk: int
        @returns: Event object containing retrieved data, otherwise HTTP error.
        @rtype: Event
        """
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data of a specific Event object, providing its id.
        Event data is returned in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a specific Event object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Event object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Event object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested Event object ' + str(pk))
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update data of a specific Event object, providing
        its id and the updated data.

        @param request: HttpRequest which provide all updated data fields.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Event object to update.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the Event updated serialized data, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on Event object ' + str(pk))
        with edit_lock:
            event = self.get_object(pk)
            serializer = EventSerializer(event, data=request.data, )
            if serializer.is_valid():
                serializer.save()
                logger.debug('Event object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for Event object ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete an Event object providing its id.

        @param request: HttpRequest used to delete a specific Event object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Event object to delete.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of Event object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on Event object ' + str(pk))
        event = self.get_object(pk)
        event.delete()
        logger.debug('Event object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
