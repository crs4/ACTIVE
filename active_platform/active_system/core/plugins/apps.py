# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been defined to provide a function/application that is executed at platform startup.
A event is generated and all actions associated are called.
Moreover at system startup all available plugins manifest files are scanned and their
values are uploaded and stored in the database, through the PluginManager.
"""

from django.apps import AppConfig
from core.plugins.event_manager import EventManager
from core.plugins.plugin_manager import PluginManager


class PluginConfig(AppConfig):
    name = 'core.plugins'
    verbose_name = "Plugin manifest file parsing"

    def ready(self):
        """
        This method overrides the standard method and it will be executed at system startup.

        PS: this function will edit the database every time
        that Django configuration operation is executed!!!
        """
        # loads data from plugin manifest files
        PluginManager().detect_plugins()

        # generate the startup event
        e = EventManager()
        e.start_scripts("STARTUP",{},{})


