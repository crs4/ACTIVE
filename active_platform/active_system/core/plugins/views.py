# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes needed to handle the event triggering
"""

from core.views import EventView
from core.plugins.event_manager import EventManager
from core.plugins.models import Script
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import json
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

class EventTrigger(APIView):
    """
    This class is used to trigger a event by its id.
    All scripts associated to the specified event will be executed.
    """
    queryset = Script.objects.none()  # required for DjangoModelPermissions

    def post(self, request, event_id, format=None):
        """
        Method used to trigger an event by its id.

        @param event_id: Primary key used to retrieve a Event object.
        @type event_id: int
        """
        logger.debug('Requested execution of Event object with id ' + str(event_id))
        try:
            # retrieve event data
            e = Event.objects.get(pk=event_id)
            # retrieve script parameters
            auth_params = {}
            if request.user and request.auth:
                auth_params['user_id'] = request.user.pk
                auth_params['token']   = 'Bearer ' + str(request.auth.token)
                auth_params['is_root'] = request.user.is_superuser or len(request.user.groups.filter(name='Admin'))

            func_params = request.POST.get('func_params', {})
            # trigger the specified event
            EventManager().start_scripts(e.name, auth_params, func_params)
        except:
            logger.error('Error on trigger of Event object with id ' + str(event_id))
        
        return Response(status=status.HTTP_200_OK)


class EventExec(APIView):
    """
    This class is used to execute a script providing its id.
    """
    queryset = Script.objects.none()  # required for DjangoModelPermissions

    def post(self, request, script_id, format=None):
        """
        Method used to execute a script by its id.
        Parameters provided to the script are extracted from the body
        of the HTTP request, looking for input_dict and output_dict fields.

        @param script_id: Primary key used to retrieve a Script object.
        @type script_id: int
        """
        logger.debug('Requested execution of Script object with id ' + str(script_id))
        try:
            # retrieve script parameters
            data = json.loads(request.body)
            auth_params = {}
            if request.user and request.auth:
                auth_params['user_id'] = request.user.pk
                auth_params['token']   = 'Bearer ' + str(request.auth.token)
                auth_params['is_root'] = request.user.is_superuser or len(request.user.groups.filter(name='Admin'))

            func_params = request.POST.get('func_params', data["func_params"])

            # trigger the specified event 
            EventManager().execute_script_by_id(script_id, auth_params, func_params)
        except:
            logger.error('Error on trigger of Script object with id ' + str(script_id))
        
        return Response(status=status.HTTP_200_OK)
