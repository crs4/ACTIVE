# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the items module, in order to 
check if it is possible to manage the digital items uploaded in the ACTIVE platform.
For authentication purposes it is necessary to create a User called "root".
"""

from core.items.models import Item
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
import os


class ItemsTest(TestCase):

    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new file
        item = Item()
        item.filename = ''
        item.type = 'image'
        item.file = File(os.path.join(settings.MEDIA_ROOT, 'tests', 'test_image', 'test.jpg'))
        item.owner = user
        item.save()


    def test_get_all(self):
        """
        Retrieve all Item objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)


    def test_get(self):
        """
        Retrieve an Item object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_put(self):
        """
        Update an Item object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/items/1/', {'description': 'test file'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete(self):
        """
        Delete an Item object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/items/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


