from django.http import HttpResponse, Http404
from django.shortcuts import render

from core.plugins.models import View
from core.plugins.models import Event
from core.plugins.models import Plugin

from core.plugins.serializers import EventSerializer
from core.plugins.decorators import generate_event


from rest_framework.response import Response
from rest_framework import status

from core.views import EventView




######### spostare nel file __init__.py ###############
"""
from plugin_mount_point import ActionProvider
from plugins import *

def run_plugins(request):
    
    result= []
    actions = ActionProvider.get_plugins()

    for a in actions:
        a.perform()
        result.append(a.configuration)    
 
    return HttpResponse(result)
""" 
#####################################################


class EventList(EventView): 

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
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
        :param pk: Event's id.
        :returns: Object containing event data if any, HTTP error otherwise.
        """
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to return serialized data of a event.
        :param pk: Event's id.
        :param format: Format used for data serialization.
        :returns: Event serialized data.
        """
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update event information providing
        serialized data.
        :param pk: event id.
        :param format: Format used for data serialization.
        :returns: Event data update status.
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
        :param pk: Event id.
        :param format: Format used for data serialization.
        :returns: Event data deletion status.
        """
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
