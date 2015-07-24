"""
Module used to test the internal API for the script module.
It is possibile to check if it is possible to create, update, retrieve and
delete Script objects.
"""

from core.plugins.models import Script, Event, Plugin
from django.test import TestCase


def create_script(event_id=1, plugin_id=1):        
    """
    Method used to create and return a simple Script object.
    """
    event = Event.objects.get(pk=event_id)
    plugin = Plugin.objects.get(pk=plugin_id)

    script = Script()
    script.title = "org.module.test"
    script.plugin = plugin
    script.save()
    script.events.add(event)
    script.save()
    return script


class ScriptTests(TestCase):
    """
    Test suite used to check if Script objects are corretely stored in the database.
    """
    def setUp(self):
        """
        Method used to init the test database.
        It creates a new User with id 1.
        """
        event1 = Event.objects.create(name="TEST_CREATED")
        event2 = Event.objects.create(name="TEST_DELETED")
        plugin = Plugin.objects.create(title="MyPlugin")

    def test_create(self):
        """
        Test used to create and save a Script object.
        """
        create_script()
        self.assertTrue(1, Script.objects.count())
        
    def test_get(self):
        """
        Test used to create and retrieve a Item object.
        """
        script = create_script()
        script_retrieved = Script.objects.filter(pk=script.pk)[0]        
        self.assertEqual(script.id, script_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a Script object.
        """
        script = create_script()

        script.details = 'sample2.mp4'
        script.save()

        script_retrieved = Script.objects.filter(pk=script.pk)[0]
        self.assertEqual(script.details, script_retrieved.details)

    def test_delete(self):
        """
        Test used to create and retrieve a Script object.
        """
        script = create_script()
        script.delete()
        self.assertEqual(0, Script.objects.count())
        
