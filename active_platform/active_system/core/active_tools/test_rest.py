# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the active_tools module, in order to 
check if it is possible to retrieve all installed ACTIVE Tools.
For authentication purposes it is necessary to create a User called "root".
"""

from core.active_tools.views import ActiveToolsList
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

def createTestUser():
    """
    Function used to create and save User on the test database.
    User credentials are static and well known.
    """
    return User.objects.create_user('root', 'root@gmail.com', 'root')    
    
def createUserToken(user):
    """
    Function used to create an authentication token for the test User.
    This token will be used for authentication purposes.
    """
    return Token.objects.create(user=user)


class ActiveToolsTest(TestCase):
    def setUp(self):
        """
        Method used to setup the test database
        """
        user = createTestUser()
        createUserToken(user)

    def test_1(self):
        """
        Retrieve the installed ACTIVE Tools
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/active_tools/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_2(self):
        """
        Check the installed ACTIVE Tools
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/active_tools/')
        
        self.assertNotEqual(len(response.data), 0)
