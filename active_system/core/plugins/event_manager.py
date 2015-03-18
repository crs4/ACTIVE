from django.conf import settings
from core.plugins.models import Event, View, Script
import requests
import json

# TODO aggiungere i parametri alle chiamate delle funzioni, passare dei parametri agli eventi/plugin

class EventManager():
	"""
	This class has been defined in order to handle event generation/triggering,
	detecting all functions associated to an event, all plugins associated to each event
	and then executing each plugin on the job processor (through REST API).
	"""

	def start_scripts(self, event_name, input_dict={}, output_dict={}):
		"""
		This method is used to detect all scripts associated to an event, giving the
		unique event name. They are executed as soon as detected.
		:param event_name: The name of the event that will be triggered.
		"""
		print "Generato evento ", event_name
		if (Script.objects.filter(events__name = event_name).count() > 0):
			for script in Script.objects.filter(events__name = event_name):
				self.execute_script(script, input_dict, output_dict)

		######### TODO determinare che non si tratta di un plugin ############
		else:
			pass
	
	
	def start_scripts_by_view(self, view_name, input_dict={}, output_dict={}):
		"""
		This method is used to execute all plugins that are associated to any
		event, whose is associated to a generic function.
		:param view_name: The name of the function that trigger one or more events.
		"""
		for view in View.objects.filter(path_abs = view_name):
			print "Chiamata la funzione ", view.path_abs
			self.start_scripts(view.event.name, input_dict, output_dict)
	
	
	def execute_script(self, script, input_dict, output_dict):
		"""
		This method is used to execute a plugin, providing the object which embedd
		all necessary information.
		The plugin will be executed in a (potentially remote) job processor through the
		REST API, providing all necessary data.
		:param plugin: The plugin that will be executed in a remote job processor.
		"""		
		#print kwargs['func_res'].data
		r = requests.post(settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/',
						{'func_name': script.path,
						 'job_name':script.job_name,
						 'event_in_params': json.dumps(input_dict),
						 'event_out_params': json.dumps(output_dict),
						 'name':''})		
		print "Esecuzione ", script.details
