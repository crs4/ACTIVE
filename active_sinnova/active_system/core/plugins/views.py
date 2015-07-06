"""
This module contains all classes needed to handle the event triggering

"""

from core.views import EventView
from core.plugins.event_manager import EventManager
from core.plugins.models import Event

from rest_framework.response import Response
from rest_framework import status

import json


class EventTrigger(EventView):
    """
    This class is used to trigger a event by its id.
    All scripts associated to the specified event will be executed.
    """

    def post(self, request, event_id, format=None):
        """
        Method used to trigger an event by its id.

        @param event_id: Primary key used to retrieve a Event object.
        @type event_id: int
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
    """
    This class is used to execute a script providing its id.
    """

    def post(self, request, script_id, format=None):
        """
        Method used to execute a script by its id.
        Parameters provided to the script are extracted from the body
        of the HTTP request, looking for input_dict and output_dict fields.

        @param script_id: Primary key used to retrieve a Script object.
        @type script_id: int
        """
        # retrieve script parameters
        data = json.loads(request.body)
        print data["func_params"]['file'], '\n\n\n'
        input_dict = request.POST.get('input_dict', data["auth_params"])
        output_dict = request.POST.get('output_dict', data["func_params"])

        # trigger the specified event
        #EventManager().execute_script_by_id(script_id, data["input_dict"], data["output_dict"])
        #print '\n\n\n', input_dict, output_dict, '\n\n\n'
        EventManager().execute_script_by_id(script_id, input_dict, output_dict)

        return Response(status=status.HTTP_200_OK)
