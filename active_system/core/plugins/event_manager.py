"""
This module define a class used to handle the event triggering based on the
name of the event or the script id.
"""

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

    def start_scripts(self, event_name, auth_dict={}, param_dict={}):
        """
        This method is used to detect all scripts associated to an event, giving the
        unique event name. They are executed as soon as detected.

        @param event_name: The name of the event that has been triggered.
        @type event_name: string
        @param auth_dict: Optional dictionary containing all action input data provided to the event.
        @type auth_dict: dictionary
        @param param_dict: Optional dictionary containing all action output data provided to the event.
        @type param_dict: dictionary
        """
        logger.info('Triggering all scripts associated to ' + event_name + ' event')
        if Script.objects.filter(events__name = event_name).count() > 0:
            for script in Script.objects.filter(events__name = event_name):
                self.execute_script(script, auth_dict, param_dict)

    def execute_script_by_id(self, script_id, auth_dict, param_dict={}):
        """
        This method is used to execute a script by its id.
        All input parameters must be specified, otherwise they will be empty.

        @param script_id: The id of the script that will be executed.
        @type script_id: int
        @param auth_dict: Optional dictionary containing inputs that will be provided to the script.
        @type auth_dict: dictionary
        @param param_dict: Optional dictionary containing inputs that will be provided to the script.
        @type param_dict: dictionary
        """
        logger.info('Triggering plugin script ' + str(script_id))
        script = Script.objects.get(pk=script_id)
        self.execute_script(script, auth_dict, param_dict)

    def execute_script(self, script, auth_dict={}, param_dict={}):
        """
        This method is used to execute a provided plugin script,embedding
        all necessary information.
        The script will be executed in a (potentially remote) job processor invoked
        through a REST API providing all necessary data.

        @param script: The plugin script object that will be executed in a remote job processor.
        @type script: The plugin that will be executed in a remote job processor.
        @param auth_dict: Optional dictionary containing all action input data provided to the event.
        @type auth_dict: dictionary
        @param param_dict: Optional dictionary containing all action output data provided to the event.
        @type param_dict: dictionary
        """

        logger.debug('Starting plugin script ' + str(script.pk) + ' on Job Processor')
        desc = script.details
        if 'id' in param_dict:
            desc += ' - ' + str(param_dict['id'])
        server_url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
        r = requests.post(server_url,	{'name'       : desc,
                                         'func_name'  : script.path,
                                         'job_name'   : script.job_name,
                                         'auth_params': json.dumps(auth_dict),
                                         'func_params': json.dumps(param_dict)})

        if r.status_code != requests.codes.ok:
            logger.error('Error on starting execution of script ' + script.pk)

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
        for action in Action.objects.filter(path_abs = action_name):
            logger.info('Triggering action ' + action.path_abs)
            self.start_scripts(action.event.name, auth_dict, func_dict)
