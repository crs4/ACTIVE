# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the items.video module, in order to 
check if it is possible to manage the video digital items uploaded in the ACTIVE platform.
For authentication purposes it is necessary to create a User called "root".
"""

from core.items.video.models import VideoItem
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
import os


class VideoItemsTest(TestCase):

    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new VideoItem
        item = VideoItem()
        item.filename = ''
        item.type = 'video'
        item.file = File(os.path.join(settings.MEDIA_ROOT, 'tests', 'test_video', 'test.mp4'))
        item.owner = user
        item.save()


    def test_get_all(self):
        """
        Retrieve all VideoItem objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/video/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(response.data['count'], 1)


    def test_get(self):
        """
        Retrieve an VideoItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/items/video/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post(self):
        """
        Upload an VideoItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/items/video/', {'description':'test', 'filename':'test.mp4'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_put(self):
        """
        Update an VideoItem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/items/video/1/', {'description': 'test file'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete(self):
        """
        Delete an Videotem object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete('/api/items/video/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


