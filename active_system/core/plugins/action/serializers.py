from rest_framework import serializers
from core.plugins.models import Action

class ActionSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objetcs.
    """
    class Meta:
        model = Action
        fields = ('id', 'path_abs', 'event')


