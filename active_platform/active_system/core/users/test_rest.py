# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the users module, in order
to check if it is possible to manage the User, Group, Permission, ContentType.
For authentication purposes it is necessary to create a User called "root".
"""

from core.users.models import User, Group, Permission, ContentType
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
import os

class UserTest(TestCase):
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
    
    def test_get_all(self):
        """
        Retrieve all User objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/users/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)

    def test_get(self):
        """
        Retrieve a User object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/users/users/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """
        Create a User object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'username'   : 'JohnDoe',
                'first_name' : 'John',
                'last_name'  : 'Doe',
                'email'      : 'JohnDoe@gmail.com',
                'password'   : 'qwerty',
                'groups'     : [],
                'user_permissions' : []
        }
        response = client.post('/api/users/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        """
        Update a User object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        # partial update is not supported
        data = {'username'   : 'JohnDoe',
                'first_name' : 'John',
                'last_name'  : 'Doe',
                'email'      : 'JohnDoe@gmail.com',
                'password'   : 'qwerty',
                'groups'     : [],
                'user_permissions' : []
        }
        response = client.put('/api/users/users/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Delete a User object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/users/users/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GroupTest(TestCase):    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new User
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Group
        group = Group()
        group.name = "my_group"
        group.save()
    
    def test_get_all(self):
        """
        Retrieve all Group objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/users/groups/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)
