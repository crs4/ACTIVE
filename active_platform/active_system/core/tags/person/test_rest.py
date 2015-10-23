# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the tags.person module, in order to 
check if it is possible to manage the Person associated to ACTIVE platform digital items.
For authentication purposes it is necessary to create a User called "root".
"""

from core.tags.person.models import Person
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
import os


class PersonTest(TestCase):    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Person
        person = Person()
        person.first_name = 'John'
        person.last_name = 'Doe'
        person.gender    = 'male'
        person.save()

    def test_get_all(self):
        """
        Retrieve all Person objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/people/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)

    def test_get(self):
        """
        Retrieve a Person object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/people/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """
        Create a Person object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'first_name' : 'Jane',
                'last_name'  : 'Doe',
                'gender'     : 'female',
                'category'   : 'person'
               }
        response = client.post('/api/people/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post2(self):
        """
        Avoid the collision of two Person objects
        """
        # create a new Person
        person2 = Person()
        person2.first_name = 'John'
        person2.last_name  = 'Doe'
        person2.gender     = 'male'
        person2.save()

        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'first_name' : 'John',
                'last_name'  : 'Doe',
                'gender'     : 'male',
                'category'   : 'person'
               }
        response = client.post('/api/people/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)

    def test_put(self):
        """
        Update a Person object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/people/1/', {'gender' : 'female'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put2(self):
        """
        Avoid the collision of two Person objects
        """
        # create a new Person
        person = Person()
        person.first_name = 'Jane'
        person.last_name  = 'Doe'
        person.gender     = 'female'
        person.save()

        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'first_name' : 'John',
                'last_name'  : 'Doe',
        }
        response = client.put('/api/people/' + str(person.id) + '/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_delete(self):
        """
        Delete a Person object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/people/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

