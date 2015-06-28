"""
This module has been defined to provide a function/application that is executed at platform startup.
All unused tags are removed in order to reduce the amount of space for stored items.
"""

from django.apps import AppConfig


class TagsConfig(AppConfig):
    name = 'core.tags'
    verbose_name = "Delete unused keywords"

    def ready(self):
        """
        This method remove all unused keywordshe standard method and
        it will be executed at system startup.

        PS: this function will edit the database every time
        that Django configuration operation is executed!!!
        """
        # loads data from plugin manifest files
        # TODO decidere se cancellare o meno le keywrod non associate ad item