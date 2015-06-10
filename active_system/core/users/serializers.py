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