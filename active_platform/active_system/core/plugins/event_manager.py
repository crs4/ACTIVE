# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from core.plugins.models import Event, Action, Script
import requests
import json
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class EventManager():
    """
    This class has been defined in order to handle event generation/triggering,
    detecting all functions associated to an event, all plugin scripts associated to each event
    and then executing each plugin script on the job processor (through REST API).
    """

    def start_scripts(self, event_name, auth_dict, func_dict):
        """
        This method is used to detect all scripts associated to an event, giving the
        unique event name. They are executed as soon as detected.

        @param event_name: The name of the event that has been triggered.
        @type event_name: string
        @param auth_dict: Optional dictionary containing all action input data provided to the event.
        @type auth_dict: dictionary
        @param func_dict: Optional dictionary containing all action output data provided to the event.
        @type func_dict: dictionary
        """
        logger.debug('The event ' + event_name + ' has been triggered')
        if (Script.objects.filter(events__name = event_name).count() > 0):
            for script in Script.objects.filter(events__name = event_name):
                self.execute_script(script, auth_dict, func_dict)

    def start_scripts_by_action(self, action_name, auth_dict, func_dict):
        """
        This method is used to execute all plugin scripts that are associated to any
        event, whose is associated to a generic action/function.

        @param action_name: The name of the action (function) that will trigger one or more events.
        @type action_name: string
        @param auth_dict: Optional dictionary containing all action input data provided to the event.
        @type auth_dict: dictionary
        @param func_dict: Optional dictionary containing all action output data provided to the event.
        @type func_dict: dictionary
        """
        action = Action.objects.filter(path_abs = action_name)
        if action:
            events = action[0].events.all()
            print "events associated with the action ", action, events
            for event in events:
                self.start_scripts(event.name, auth_dict, func_dict)

    def execute_script_by_id(self, script_id, auth_dict, func_dict):
        """
        This method is used to execute a script by its id.
        All input parameters must be specified, otherwise they will be empty.

        @param script_id: The id of the script that will be executed.
        @type script_id: int
        @param auth_dict: Optional dictionary containing inputs that will be provided to the script.
        @type auth_dict: dictionary
        @param func_dict: Optional dictionary containing inputs that will be provided to the script.
        @type func_dict: dictionary
        """
        script = Script.objects.get(pk=script_id)
        self.execute_script(script, auth_dict, func_dict)

    def execute_script(self, script, auth_dict, func_dict):
        """
        This method is used to execute a provided plugin script,embedding
        all necessary information.
        The script will be executed in a (potentially remote) job processor invoked
        through a REST API providing all necessary data.

        @param script: The plugin script object that will be executed in a remote job processor.
        @type script: The plugin that will be executed in a remote job processor.
        @param auth_dict: Optional dictionary containing all action input data provided to the event.
        @type auth_dict: dictionary
        @param func_dict: Optional dictionary containing all action output data provided to the event.
        @type func_dict: dictionary
        """
        desc = script.details
        
        if 'id' in func_dict:
            desc += ' - ' + str(func_dict['id'])
        server_url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
        r = requests.post(server_url,	{'func_name': script.path,
                                          'job_name': script.job_name,
                                          'auth_params' : json.dumps(auth_dict),
                                          'func_params' : json.dumps(func_dict),
                                          'name' : desc})
        logger.debug('Running ' + script.details + 'script...')
