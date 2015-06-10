"""
This module has been defined to provide a function/application that is executed at platform startup.
A event is generated and all actions associated are called.
Moreover at system startup all available plugins manifest files are scanned and their
values are uploaded and stored in the database, through the PluginManager.
"""

from django.apps import AppConfig
from core.plugins.event_manager import EventManager
from core.plugins.plugin_manager import PluginManager
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class PluginConfig(AppConfig):
    name = 'core.plugins'
    verbose_name = "Plugin manifest file parsing"

    def ready(self):
        """
        This method overrides the standard method and it will be executed at system startup.

        PS: this function will edit the database every time
        that a Django configuration operation is executed!!!
        """
        logger.info('Loading data from plugin manifest files')
        PluginManager().detect_plugins()

        logger.info('Generating the startup event')
        e = EventManager()
        e.start_scripts("STARTUP")
