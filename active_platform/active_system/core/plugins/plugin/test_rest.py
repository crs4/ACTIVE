# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the plugins.plugin module,
in order to check if it is possible to  handle the Plugin objects.
For authentication purposes it is necessary to create a User called "root".
"""

from core.plugins.models import Plugin
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
import os


class PluginTest(TestCase):

    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create a new Plugin
        plugin = Plugin()
        plugin.name = 'My test plugin'
        plugin.description = 'image'
        plugin.active_version = '1.0.0'
        plugin.plugin_version = '1.0.0'
        plugin.url_info = 'http://active.crs4.it'
        plugin.authors  = 'John Doe'
        plugin.save()

    def test_get_all(self):
        """
        Retrieve all Plugin objects
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/plugins/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(len(response.data), 1)


    def test_get(self):
        """
        Retrieve a Plugin object
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/plugins/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

