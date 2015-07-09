"""
This module contains all classes and methods needed to retrieve all Event objects
and invoke CRUD operations, providing a id if requested.
"""

from django.http import HttpResponse, Http404

from core.plugins.models import Event
from core.plugins.event.serializers import EventSerializer
from core.plugins.script.serializers import ScriptSerializer

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

import logging
import threading

# utilizzato per risolvere il problema dell'accesso concorrente agli item
edit_lock = threading.Lock()

# variable used for logging purposes
logger = logging.getLogger('active_log')


class EventList(EventView): 
    """
    List all existing Events or create/save a new one.
    """

    queryset = Event.objects.none()  # required for DjangoModelPermissions


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
        logger.debug('Requested all Event objects')
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        This method is used to create and store a new Event object.
        All required data is provided in a serialized format.

        @param request: HttpRequest containing all data for the new Event object.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing the id of the new object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Created a new Event object')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.debug('Error on new Event object creation')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(EventView): 
    """
    Retrieve, update or delete a event instance.
    """

    queryset = Event.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        """
        Method used to retrieve an Event objects using its id.

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
        Event data is returned in a serialized format.

        @param request: HttpRequest used to retrieve data of a specific Event object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Event object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Event object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested details for Event object with id ' + str(pk))
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update data of a specific Event object, providing fresh field data.

        @param request: HttpRequest which provide all update data fields.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Event object to update.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the Event updated serialized data, error otherwise.
        @rtype: HttpResponse
        """
        with edit_lock:
            event = self.get_object(pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Updated data for Event object with id ' + str(pk))
                return Response(serializer.data)
            logger.debug('Error on update of Event object with id ' + str(pk))
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
        logger.debug('Requested delete on Event object with id ' + str(pk))
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
