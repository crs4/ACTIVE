from rest_framework import serializers
from core.plugins.models import Event

class EventSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objetcs.
    """
    class Meta:
        model = Event
        fields = ('id', 'name', 'description')


