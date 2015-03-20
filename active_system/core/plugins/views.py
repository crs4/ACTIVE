from django.http import HttpResponse, Http404
from django.shortcuts import render

from core.plugins.decorators import generate_event
from core.plugins.models import Action, Event, Script, Plugin
from core.plugins.serializers import EventSerializer

from rest_framework.response import Response
from rest_framework import status

from core.views import EventView


class EventList(EventView): 
    """
    List all existing Events or create/save a new one.
    """
    def get(self, request, format=None):
	"""
        This method will be converted in a HTTP GET API and it
        will allow to list all already stored Event objects in the database.
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	"""
	This method will be converted in a HTTP POST API and it
	will allow to save new Event objects in the database.
	"""
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(EventView): 
    """
    Retrieve, update or delete a event instance.
    """
    def get_object(self, pk):
        """
        Method used to obtain event data by its id.
        @param pk: Event's id.
        @returns: Object containing event data if any, HTTP error otherwise.
        """
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to return serialized data of a event.
        @param pk: Event's id.
        @param format: Format used for data serialization.
        @returns: Event serialized data.
        """
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update event information providing
        serialized data.
        @param pk: event id.
        @param format: Format used for data serialization.
        @returns: Event data update status.
        """
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete event information providing his ID.
        @param pk: Event id.
        @param format: Format used for data serialization.
        @returns: Event data deletion status.
        """
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
