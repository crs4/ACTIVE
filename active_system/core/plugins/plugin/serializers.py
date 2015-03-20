from rest_framework import serializers
from core.plugins.models import Plugin

class PluginSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Plugin objetcs.
    """
    class Meta:
        model = Plugin
        fields = ('id', 'title', 'description', 'active_version', 'plugin_version', 'url_info', 'authors')

