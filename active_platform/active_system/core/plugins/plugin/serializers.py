"""
This module contains the serializer needed to convert Plugin objects to
and from a JSON format, in order to create a REST API.
"""

from rest_framework import serializers
from core.plugins.models import Plugin


class PluginSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Plugin objects.
    """
    class Meta:
        model = Plugin
        fields = ('id', 'title', 'description', 'active_version',
                  'plugin_version', 'url_info', 'authors')

