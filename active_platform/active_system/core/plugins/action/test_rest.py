# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the plugins.action module, in order to 
check if it is possible to handle the Action objects loaded in the ACTIVE platform.
For authentication purposes it is necessary to create a User called "root".
"""

from core.plugins.models import Action, Event
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
import os


class ActionTest(TestCase):
    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Event object
        event = Event()
        event.name = 'ITEM_CREATED'
        event.description = ''
        event.save()
        # create a new Action object
        action = Action.objects.create(path_abs='core.items.video.views.VideoItemList.post')
        action.events.add(event)
        action.save()

    def test_get_all(self):
        """
        Retrieve all Action objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/actions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(len(response.data), 1)

    def test_get(self):
        """
        Retrieve an Action object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/actions/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
