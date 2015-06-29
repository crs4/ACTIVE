"""
This module contains the class needed to provide a REST API for Event objects.
The serializer defined in this class allow to convert Event data to and from the JSON format.
"""

from rest_framework import serializers
from core.plugins.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objects.
    """
    class Meta:
        model = Event
        fields = ('id', 'name', 'description')