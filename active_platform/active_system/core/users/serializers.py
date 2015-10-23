# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes used to define the JSON serializers
that will be used in the REST API for the User, Group, Permission, ContentType
objects manipulation.
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    Class used to define a JSON serialized for User objects.
    """
    class Meta:
        model = User


class GroupSerializer(ModelSerializer):
    """
    Class used to define a JSON serialized for Group objects.
    """
    class Meta:
        model = Group


class PermissionSerializer(ModelSerializer):
    """
    Class used to define a JSON serialized for Permission objects.
    """
    class Meta:
        model = Permission


class ContentTypeSerializer(ModelSerializer):
    """
    Class used to define a JSON serialized for ContentType objects.
    """
    class Meta:
        model = ContentType
