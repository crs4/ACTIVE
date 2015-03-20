"""
This module is defined in order to execute all code at system startup.
In this particular case it will be executed all code necessary to:
- scan all plugin manifest files
- parse each manifest file
- load/save plugin data in the database 
"""

from django.apps import AppConfig
from ConfigParser import ConfigParser
from core.plugins.event_manager import EventManager
from core.plugins.plugin_manager import PluginManager
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

		PluginManager().detect_plugins()

		# generate the startup event
		e = EventManager()
		e.start_scripts("STARTUP")


