from django.conf import settings
from core.plugins.models import Event, Action, Script
import requests
import json


class EventManager():
	"""
	This class has been defined in order to handle event generation/triggering,
	detecting all functions associated to an event, all plugin scripts associated to each event
	and then executing each plugin script on the job processor (through REST API).
	"""

	def start_scripts(self, event_name, input_dict={}, output_dict={}):
		"""
		This method is used to detect all scripts associated to an event, giving the
		unique event name. They are executed as soon as detected.

		@param event_name: The name of the event that has been triggered.
		@type event_name: string
		@param input_dict: Optional dictionary containing all action input data provided to the event.
		@type input_dict: dictionary
		@param output_dict: Optional dictionary containing all action output data provided to the event.
		@type output_dict: dictionary
		"""
		print 'The event', event_name, 'has been triggered'
		if (Script.objects.filter(events__name = event_name).count() > 0):
			for script in Script.objects.filter(events__name = event_name):
				self.execute_script(script, input_dict, output_dict)
	
	
	def start_scripts_by_action(self, action_name, input_dict={}, output_dict={}):
		"""
		This method is used to execute all plugin scripts that are associated to any
		event, whose is associated to a generic action/function.
	
		@param action_name: The name of the action (function) that will trigger one or more events.
		@type action_name: string
		@param input_dict: Optional dictionary containing all action input data provided to the event.
                @type input_dict: dictionary
                @param output_dict: Optional dictionary containing all action output data provided to the event.
                @type output_dict: dictionary
		"""
		for action in Action.objects.filter(path_abs = action_name):
			print 'The action ', action.path_abs, 'has been triggered'
			self.start_scripts(action.event.name, input_dict, output_dict)
	
	def execute_script_by_id(self, script_id, input_dict={}, output_dict={}):
		"""
		This method is used to execute a script by its id.
		All input parameters must be specified, otherwise they will be empty.

                @param script_id: The id of the script that will be executed.
                @type action_name: int
                @param input_dict: Optional dictionary containing inputs that will be provided to the script.
                @type input_dict: dictionary
                @param output_dict: Optional dictionary containing inputs that will be provided to the script.
                @type output_dict: dictionary
		"""
		script = Script.objects.get(pk=script_id)

		self.execute_script(script, input_dict, output_dict)

	def execute_script(self, script, input_dict={}, output_dict={}):
		"""
		This method is used to execute a provided plugin script,embedding
		all necessary information.
		The script will be executed in a (potentially remote) job processor invoked
		through a REST API providing all necessary data.

		@param script: The plugin script object that will be executed in a remote job processor.
		@type script: The plugin that will be executed in a remote job processor.
		@param input_dict: Optional dictionary containing all action input data provided to the event.
                @type input_dict: dictionary
                @param output_dict: Optional dictionary containing all action output data provided to the event.
                @type output_dict: dictionary
		"""
		server_url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
		# problema TemporaryUploadedFile!
		r = requests.post(server_url,	{'func_name': script.path,
						 'job_name': script.job_name,
						 'event_in_params' : json.dumps(input_dict),
						 'event_out_params' : json.dumps(output_dict),
						 'name' : 'Event generated job'})		
		print 'Running ', script.details, 'script...'
		
