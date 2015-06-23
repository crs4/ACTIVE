"""
This module contains all classes needed to handle the event triggering.
It is only possible to trigger the execution of a specific event or the execution
of a specific script providing its id.
"""

from core.views import EventView
from core.plugins.event_manager import EventManager
from core.plugins.models import Event, Script

from django.contrib.auth.models import Group

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
            auth_params = {}
            func_params = request.data.get('func_params', {})

            # assign the user authentication token and id
            auth_params['token']   = 'Bearer ' + request.auth.token
            auth_params['user_id'] = request.user.pk
            auth_params['is_root'] = request.user.is_superuser or Group.objects.filter(name = 'Admin') in request.user.groups.all()

            # trigger the specified event
            EventManager().start_scripts(e.name, auth_params, func_params)
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
        of the HTTP request, looking for auth_params and func_params fields.

        @param script_id: Primary key used to retrieve a Script object.
        @type script_id: int
        """
        # retrieve script parameters
        auth_params = {}
        data = json.loads(request.body)
        func_params = data['func_params']

        # assign the user authentication token and id
        # assign the user authentication token and id
        auth_params['token']   = 'Bearer ' + request.auth.token
        auth_params['user_id'] = request.user.pk
        auth_params['is_root'] = request.user.is_superuser or Group.objects.filter(name = 'Admin') in request.user.groups.all()

        # trigger the specified event
        EventManager().execute_script_by_id(script_id, auth_params, func_params)

        logger.debug('Script ' + script_id + ' correctly started')
        return Response(status=status.HTTP_200_OK)
