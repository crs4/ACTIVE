
from django.conf import settings
from ConfigParser import ConfigParser
from core.plugins.models import Plugin, Script, Event

import os


class PluginManager():
    """
    This class has been defined in order to create a unique handler of plugin data.
    It exposes all methods necessary to detect available plugins from manifest files,
    save them in the database and create a dedicated object representation.
    """

    def get_modules(self):
	"""
	Method used to detect all available manifest files.
	Manifest files are searched inside a directory specified in the project settings.
	:returns: A list of absolute paths to all available manifest files.
	"""
	modules = []
	for file in os.listdir(settings.PLUGIN_MANIFEST_PATH):
		absolute_file_path = os.path.join(settings.PLUGIN_MANIFEST_PATH, file)
	        if os.path.isfile(absolute_file_path) and file.endswith('.ini'):
	                modules.append(absolute_file_path)
	return modules

    
    def get_sections(self, module):
	"""
	This method is used to extract all sections from a given manifest file.
	Sections are stored inside a dictionary and each section is a dictionary himself.
	:param module: The module contining the manifest file that will be parsed.
	:returns: A dictoionary containing all extracted sections.
	"""
	# read the manifest file
	parser = ConfigParser()
	parser.read(module)
    	config = dict(parser._sections)

	# convert the list of couples in a dictionary
	for k in config:
            config[k] = dict(parser._defaults, **config[k])
            config[k].pop('__name__', None)
	# return the obtained dictionary of sections
	return config


    def extract_plugin(self, sections):
	"""
	This method allow to extract all data related to the plugin which all sections are referred to.
	:param sections: All sections extracted from the considered manifest file.
	:returns: A Plugin object corresponding to the 
	"""
	# detect if the Plugin has already been stored or create a new one
	p = None
	try:
		p = Plugin.objects.get(title = sections['PLUGIN']['title'])
	except Plugin.DoesNotExist as ex:
		# store all parsed Plugin data
       		p = Plugin(**sections['PLUGIN'])
   		p.save()
	return p


    def extract_events(self, section):
	"""
	This method is used to extract all events associated to a plugin
	from a given sections. If an Event name has already been stored in
	the database it is retrieved otherwise a new Event object is created.
	:param section: Script section containing all related information, such as event list.
	:returns: A list of Event objects associated to the considered script.
	"""
	event_list = []
	# extract the list of event identifiers
	for event in section['events'].split(','):
		event = event.replace(' ', '').upper()
		if(len(event) == 0):
			continue
		# save the event if it doesn't exist
		if(Event.objects.filter(name = event).count() == 0):
                	e = Event(name=event)
                	e.save()
		# retrieve the saved event
        	event_list.append(Event.objects.get(name = event))
	return event_list


    def extract_scripts(self, section):
	"""
	The method is used to extract all informations related to a
	script (except for the event data that must be associated later).
	:param section: The section containg current script related data.
	:returns: A Script object constructed extracting section data.
	"""
	# detect if the plugin has already been stored
	s= None	
	try:
        	s = Script.objects.get(path = section['path'])
	# otherwise create a new one
	except Script.DoesNotExist as ex:
        	s = Script(**section)
                s.save()
	return s



    def detect_plugins(self):
	"""
	This method is the main method available to the user
	and it allow to extract and load all available plugin data,
	scanning data stored in a manifest file.
	"""

	modules = self.get_modules()
	for module in modules:
		# extract plugin information 
		config = self.get_sections(module)
		p = self.extract_plugin(config)	

		# for each script extract its data
		for section_name in config.keys():
			if not section_name.startswith('SCRIPT'):
				continue

			event_list = self.extract_events(config[section_name])

			# replace a string with a list of event objects
                        del config[section_name]['events']
			
			# add a reference to its plugin
			config[section_name]['plugin'] = p

			# detect if the script already exists or must be created
			s = self.extract_scripts(config[section_name])
			

			# save the list of events associated to this script
			s.events.clear()
			for event in event_list:
				s.events.add(event)
			s.save()
