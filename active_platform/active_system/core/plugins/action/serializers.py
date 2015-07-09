"""
This module contains the serializer necessary to provide a REST API for Action objects.
"""

from rest_framework import serializers
from core.plugins.models import Action


class ActionSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objects.
    """
    class Meta:
        model = Action
        fields = ('id', 'path_abs', 'event')


