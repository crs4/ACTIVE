"""
This module contains the class necessary to define a custom serializer
for Person objects. Data will be converted from and to a JSON format,
in order to provide a REST API for manipulating Person objects.
"""

from rest_framework import serializers
from core.tags.person.models import Person


class PersonSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic person object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Person
