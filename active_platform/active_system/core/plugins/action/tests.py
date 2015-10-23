# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to test the internal API for the action module.
It is possibile to check if it is possible to create, update, retrieve and
delete Action objects.
"""

from core.plugins.models import Action, Event
from django.test import TestCase

def create_action(event_id=1):
    action = Action()
    action.path_abs = 'org.my.module.test'
    action.event = Event.objects.get(pk=event_id)
    action.save()
    return action

class ActionTests(TestCase):
    """
    Test suite used to check if Action objects are corretely stored in the database.
    """
    def setUp(self):
        """
        Method used to init the test database creating some Event objects.
        """
        event1 = Event.objects.create(name="TEST_CREATE")
        event2 = Event.objects.create(name="TEST_DELETE")

    def test_create(self):
        """
        Test used to create and save a Action object.
        """
        action = create_action()
        self.assertTrue(1, Action.objects.count())
        
    def test_get(self):
        """
        Test used to create and retrieve a Action object.
        """
        action = create_action()
        action_retrieved = Action.objects.filter(pk=action.pk)[0]        
        self.assertEqual(action.id, action_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a Action object.
        """
        action = create_action()

        action.path_abs = 'org.sample.test'
        action.save()

        action_retrieved = Action.objects.filter(pk=action.pk)[0]
        self.assertEqual(action.path_abs, action_retrieved.path_abs)

    def test_delete(self):
        """
        Test used to create and retrieve a Action object.
        """
        action = create_action()
        action.delete()
        self.assertEqual(0, Action.objects.count())
