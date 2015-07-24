"""
Module used to test the internal API for the event module.
It is possibile to check if it is possible to create, update, retrieve and
delete Event objects.
"""

from core.plugins.models import Event
from django.test import TestCase


def create_event():        
    """
    Method used to create and return a simple Event object.
    """     
    event = Event()
    event.name = "TEST"
    event.save()
    return event



class EventTests(TestCase):
    """
    Test suite used to check if Event objects are corretely stored in the database.
    """

    def test_create(self):
        """
        Test used to create and save a simple Event object.
        """
        create_event()
        self.assertTrue(1, Event.objects.count())
        
    def test_get(self):	
        """
        Test used to create and retrieve a simple Event object.
        """
        event = create_event()
        event_retrieved = Event.objects.filter(pk=event.pk)[0]        
        self.assertEqual(event.id, event_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic Event object.
        """
        event = create_event()

        event.description = 'Sample test event'
        event.save()

        event_retrieved = Event.objects.filter(pk=event.pk)[0]
        self.assertEqual(event.description, event_retrieved.description)

    def test_delete(self):
        """
        Test used to create and retrieve a simple Event object.
        """
        event = create_event()
        event.delete()
        self.assertEqual(0, Event.objects.count())
