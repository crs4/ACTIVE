"""
This module contains all classes needed to handle the event triggering.
It is only possible to trigger the execution of a specific event or the execution
of a specific script providing its id.
"""

from core.views import EventView
from core.plugins.event_manager import EventManager
from core.plugins.models import Event, Script

from rest_framework.response import Response
from rest_framework import status

import json
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class EventTrigger(EventView):
    """
    This class is used to trigger a event by its id.
    All scripts associated to the specified event will be executed.
    """
    model = Script

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

            # assign the user authentication token and id
            input_dict['token']   = str(request.auth)
            input_dict['user_id'] = request.user.pk

            # trigger the specified event
            EventManager().start_scripts(e.name, input_dict, output_dict)
        except Event.DoesNotExist:
            logger.error('Event ' + event_id + ' does not exist!')
            return Response(status=status.HTTP_404_NOT_FOUND)

        logger.debug('Event ' + event_id + ' correctly started')
        return Response(status=status.HTTP_200_OK)


class EventExec(EventView):
    """
    This class is used to execute a script providing its id.
    """
    model = Script

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
        input_dict = request.POST.get('input_dict', data["input_dict"])
        output_dict = request.POST.get('output_dict', data["output_dict"])

        # assign the user authentication token and id
        input_dict['token'] = str(request.auth)
        input_dict['user_id'] = request.user.pk

        # trigger the specified event
        EventManager().execute_script_by_id(script_id, input_dict, output_dict)

        logger.debug('Script ' + script_id + ' correctly started')
        return Response(status=status.HTTP_200_OK)
