from django.http import HttpResponse, Http404
from django.shortcuts import render

from core.plugins.event_manager import EventManager
from core.plugins.models import Event

from rest_framework.response import Response
from rest_framework import status

from core.views import EventView

import json

##### classi e metodi necessari per l'avvio di eventi e script attraverso l'API REST

class EventTrigger(EventView):
    def post(self, request, event_id, format=None):
        """
        Method used to trigger an event by its id.

        @param pk: Primary key used to retrieve a Event object.
        @type pk: int
        """
        try:
            # retrieve event data
            e = Event.objects.get(pk=event_id)
            # retrieve script parameters
            input_dict = request.POST.get('input_dict', {})
            output_dict = request.POST.get('output_dict', {})
            # trigger the specified event
            EventManager().start_scripts(e.name, input_dict, output_dict)
        except Event.DoesNotExist:
            print "Event does not exist!"

	return Response(status=status.HTTP_200_OK)

class EventExec(EventView):
    def post(self, request, script_id, format=None):
        """
        Method used to execute a script by its id.

        @param pk: Primary key used to retrieve a Script object.
        @type pk: int
        """
        # retrieve script parameters
	data = json.loads(request.body)
	print data["output_dict"]['file'], '\n\n\n'
        input_dict = request.POST.get('input_dict', data["input_dict"])
        output_dict = request.POST.get('output_dict', data["output_dict"])

        # trigger the specified event
        #EventManager().execute_script_by_id(script_id, data["input_dict"], data["output_dict"])
	#print '\n\n\n', input_dict, output_dict, '\n\n\n'
        EventManager().execute_script_by_id(script_id, input_dict, output_dict)

        return Response(status=status.HTTP_200_OK)
