"""
This module contains all classes needed to handle the event triggering
"""

from core.views import EventView
from core.plugins.event_manager import EventManager
from core.plugins.models import Event

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import json


class EventTrigger(APIView):
    """
    This class is used to trigger a event by its id.
    All scripts associated to the specified event will be executed.
    """
    queryset = Event.objects.none()  # required for DjangoModelPermissions

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
            if request.user and request.auth:
                auth_params['user_id'] = request.user.pk
                auth_params['token']   = 'Bearer ' + str(request.auth.token)
                auth_params['is_root'] = request.user.is_superuser or Group.objects.filter(name = 'Admin') in request.user.groups.all()

            func_params = request.POST.get('func_params', {})
            # trigger the specified event
            EventManager().start_scripts(e.name, auth_params, func_params)
        except Event.DoesNotExist:
            print "Event does not exist!"
        return Response(status=status.HTTP_200_OK)


class EventExec(APIView):
    """
    This class is used to execute a script providing its id.
    """
    queryset = Event.objects.none()  # required for DjangoModelPermissions
    
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
        auth_params = {}
        if request.user and request.auth:
            auth_params['user_id'] = request.user.pk
            auth_params['token']   = 'Bearer ' + str(request.auth.token)
            auth_params['is_root'] = request.user.is_superuser or Group.objects.filter(name = 'Admin') in request.user.groups.all()

        func_params = request.POST.get('func_params', data["func_params"])

        # trigger the specified event
        EventManager().execute_script_by_id(script_id, auth_params, func_params)

        return Response(status=status.HTTP_200_OK)
