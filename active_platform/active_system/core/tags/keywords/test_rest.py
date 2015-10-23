# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the tags.keywords module, in order to 
check if it is possible to manage the keywords associated to ACTIVE platform digital items.
For authentication purposes it is necessary to create a User called "root".
"""

from core.tags.keywords.models import Keyword
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
import os


class KeywordTest(TestCase):    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Keyword
        keyword = Keyword()
        keyword.category    = 'keyword'
        keyword.description = 'kangoo'
        keyword.save()

    def test_get_all(self):
        """
        Retrieve all Keyword objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/keywords/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(len(response.data), 1)

    def test_get(self):
        """
        Retrieve a Keyword object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/keywords/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """
        Create a Keyword object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'category'    : 'keyword',
                'description' : 'koala',
               }
        response = client.post('/api/keywords/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post2(self):
        """
        Avoid the collision of two Keyword objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'category'    : 'keyword',
                'description' : 'kangoo',
        }
        response = client.post('/api/keywords/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)

    def test_put(self):
        """
        Update a Keyword object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/keywords/1/', {'description' : 'koala'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put2(self):
        """
        Avoid the collision of two Keyword objects
        """
        # create a new Keyword
        keyword = Keyword()
        keyword.category    = 'keyword'
        keyword.description = 'koala'
        keyword.save()

        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/keywords/' + str(keyword.id) + '/', {'description' : 'kangoo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_delete(self):
        """
        Delete a Keyword object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/keywords/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

