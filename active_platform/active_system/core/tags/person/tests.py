# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from core.tags.person.models import Person
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
import json

def create_person():     
    person = Person.objects.create(first_name = "Pippo",last_name="Pluto", gender="male")
    return person


class PersonTests(TestCase):
    def test_create(self):
        """
        Test used to create and save a fake person.
        """        
        person = create_person()
        self.assertTrue(isinstance(person, Person))
        self.assertEqual(1,Person.objects.count())
        
    def test_get(self):
        """
        Test used to get a fake person.
        """   
        person = create_person()
        person_retrieved = Person.objects.filter(pk=person.pk)        
        self.assertEqual(person, person_retrieved[0])
        
    def test_update(self):
        """
        Test used to update fake person.
        """   
        person = create_person()
        person.gender = 'female'
        person.save()
        person_retrieved = Person.objects.filter(pk=person.pk)     
        self.assertEqual(person.gender, person_retrieved[0].gender)

    def test_delete(self):
        """
        Test used to delete a fake person.
        """   
        person = create_person()
        person.delete()
        if Person.objects.filter(pk=person.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
