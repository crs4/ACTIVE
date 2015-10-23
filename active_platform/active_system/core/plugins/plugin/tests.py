# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to test the internal API for the plugin module.
It is possibile to check if it is possible to create, update, retrieve and
delete Plugin objects.
"""

from core.plugins.models import Plugin
from django.test import TestCase


def create_plugin():        
    """
    Method used to create and return a simple Plugin object.
    """     
    plugin = Plugin()
    plugin.name = 'SamplePlugin'
    plugin.plugin_version = 1.0
    plugin.save()
    return plugin



class PluginTests(TestCase):
    """
    Test suite used to check if Plugin objects are corretely stored in the database.
    """

    def test_create(self):
        """
        Test used to create and save a simple Plugin object.
        """
        create_plugin()
        self.assertTrue(1, Plugin.objects.count())
        
    def test_get(self):
        """
        Test used to create and retrieve a simple Plugin object.
        """
        plugin = create_plugin()
        plugin_retrieved = Plugin.objects.filter(pk=plugin.pk)[0]        
        self.assertEqual(plugin.id, plugin_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic Plugin object.
        """
        plugin = create_plugin()

        plugin.description = 'sample_plugin'
        plugin.save()

        plugin_retrieved = Plugin.objects.filter(pk=plugin.pk)[0]
        self.assertEqual(plugin.description, plugin_retrieved.description)

    def test_delete(self):
        """
        Test used to create and retrieve a simple Plugin object.
        """
        plugin = create_plugin()
        plugin.delete()
        self.assertEqual(0, Plugin.objects.count())
        

