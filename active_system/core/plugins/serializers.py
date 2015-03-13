from rest_framework import serializers

from models import Plugin
from models import Event
from models import View

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name')


