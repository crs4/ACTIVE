# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the items.audio module, in order to 
check if it is possible to manage the audio digital items uploaded in the ACTIVE platform.
For authentication purposes it is necessary to create a User called "root".
"""

from core.items.audio.models import AudioItem
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
import os


class AudioItemsTest(TestCase):

    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new AudioItem
        item = AudioItem()
        item.filename = ''
        item.type = 'audio'
        item.file = File(os.path.join(settings.MEDIA_ROOT, 'tests', 'test_audio', 'test.mp3'))
        item.owner = user
        item.save()


    def test_get_all(self):
        """
        Retrieve all AudioItem objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/audio/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)


    def test_get(self):
        """
        Retrieve an AudioItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/audio/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post(self):
        """
        Upload an AudioItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/items/audio/', {'description':'test', 'filename':'test.mp3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_put(self):
        """
        Update an AudioItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/items/audio/1/', {'description': 'test file'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete(self):
        """
        Delete an AudioItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/items/audio/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


