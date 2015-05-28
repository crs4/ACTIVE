"""
This module contains all classes needed to define the serializers
for Tag and Entity objects. These serializers are defined in order
to provide a REST API converting the objects from and to a JSON format.
"""

from rest_framework import serializers
from core.tags.models import Tag, Entity


class TagSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic tag object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Tag
        fields = ('id', 'entity', 'item', 'type', 'dynamictag_set')


class EntitySerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic entity object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Entity
        fields = ('id', 'category')
