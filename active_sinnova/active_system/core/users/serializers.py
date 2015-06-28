"""
This module contains all classes needed for model serialization.
For each model it has been defined a class with all available fields.
"""

from core.users.models import ActiveUser
from rest_framework import serializers


class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ActiveUser
        fields = ('id', 'role', 'user')
        #depth  = 1
