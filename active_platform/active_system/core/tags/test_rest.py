# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the tags module, in order to 
check if it is possible to manage the tags associated to ACTIVE platform digital items.
For authentication purposes it is necessary to create a User called "root".
"""

from core.tags.models import Tag, Entity
from core.items.models import Item
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
import os


class TagTest(TestCase):   
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Item
        item = Item()
        item.filename = ''
        item.type     = 'image'
        item.owner    = user
        item.save()
        # create a new Person
        entity = Entity()
        entity.category  = 'entity'
        entity.save()
        # create a new Tag
        tag = Tag()
        tag.item   = item
        tag.entity = entity
        tag.type   = 'face'
        tag.save()
    
    def test_get_all(self):
        """
        Retrieve all Tag objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(len(response.data), 1)

    def test_get(self):
        """
        Retrieve a Tag object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/tags/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """
        Create a Tag object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'type'   : 'speaker',
                'item'   : 1,
                'entity' : 1,
                'dynamictag_set' : [] }
        response = client.post('/api/tags/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        """
        Update a Tag object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/tags/1/', {'type':'speaker'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete(self):
        """
        Delete a Tag object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/tags/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
