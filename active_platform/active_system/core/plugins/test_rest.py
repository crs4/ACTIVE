# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the plugins module, in order to 
check if it is possible to trigger an Event or a Script.
For authentication purposes it is necessary to create a User called "root".
"""

from core.plugins.models import Plugin, Script, Event
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
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
        # create a new Plugin
        plugin = Plugin()
        plugin.title = 'My test plugin'
        plugin.description = ''
        plugin.active_version = '1.0.0'
        plugin.plugin_version = '1.0.0'
        plugin.url_info = 'http://active.crs4.it'
        plugin.authors  = 'John Doe'
        plugin.save()
        # create a new Script
        script = Script()
        script.title = 'Test script for image items'
        script.details = ''
        script.path = 'mytestplugin.utils.script1'
        script.job_name = 'job_manager.job.job.PlainJob'
        script.plugin = plugin
        script.item_type = 'image'
        script.save()
        # create a new Event
        event = Event()
        event.name = 'ITEM_CREATED'
        event.description = 'Must be used when a new Item is uploaded on the platform'
        event.save()

    def test_trigger_1(self):
        """
        Trigger the execution of an Event
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data =  {
            'func_params' : {},
            'auth_params' : {}
        }
        response = client.post('/api/triggers/event/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_trigger_2(self):
        """
        Trigger the execution of a Script
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data =  {
            'func_params' : {},
            'auth_params' : {}
        }
        response = client.post('/api/triggers/script/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

