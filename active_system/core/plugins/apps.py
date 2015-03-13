"""
This module is defined in order to execute all code at system startup.
In this particular case it will be executed all code necessary to:
- scan all plugin manifest files
- parse each manifest file
- load/save plugin data in the database 
"""

from django.apps import AppConfig
from django.conf import settings
from ConfigParser import ConfigParser
from core.plugins.models import Plugin
from core.plugins.models import Event
from core.plugins.event_manager import EventManager
import os


class PluginConfig(AppConfig):
	name = 'core.plugins'
	verbose_name = "Plugin manifest file parsing"

	def ready(self):
		"""
		This method overrides the standard method and
		it will be executed at system startup.
		NB: this function will edit the database every time that
		a django configuration operation will be executed!!!
		"""
		# obtain all manifest files scanning the defined directory
		modules = []
		for file in os.listdir(settings.PLUGIN_MANIFEST_PATH):
			absolute_file_path = os.path.join(settings.PLUGIN_MANIFEST_PATH, file)
		        if os.path.isfile(absolute_file_path) and file.endswith('.ini'):
		                modules.append(absolute_file_path)

		
		# parse each manifest file and upload the plugin data if needed
		for module in modules:
			# read the manifest file
		        parser = ConfigParser()
		        parser.read(module)
		    	config = dict(parser._sections)

			# convert the list of couples in a dictionary
			for k in config:
		            config[k] = dict(parser._defaults, **config[k])
		            config[k].pop('__name__', None)


			# detect all referenced events and save them if
                        # haven't been stored before in the database
                        event_list = []
                        for event in config['PLUGIN']['events'].split(','):
				event = event.replace(' ', '').upper()
                                if(len(event) == 0):
					continue

				if(Event.objects.filter(name = event).count() == 0):
                                        e = Event(name=event)
                                        e.save()
                                event_list.append(Event.objects.get(name = event))
                        del config['PLUGIN']['events']


			# detect if the Plugin has already been stored or create a new one
			p = None
			try:
				p = Plugin.objects.get(title = config['PLUGIN']['title'])
			except Plugin.DoesNotExist as ex:
				# store all parsed Plugin data
	                        p = Plugin(**config['PLUGIN'])
        	                p.save()
				
			# add referenced events from scratch
			p.events.clear()
			for event in event_list:
        	        	p.events.add(event)
			p.save()


		# generate the startup event
		e = EventManager()
		e.start_plugins("STARTUP")


