from rest_framework import serializers
from core.plugins.models import Script

class ScriptSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Script objetcs.
    """
    class Meta:
        model = Script
        fields = ('id', 'title', 'details', 'path', 'job_name', 'plugin', 'events', 'item_type')
	depth = 2

