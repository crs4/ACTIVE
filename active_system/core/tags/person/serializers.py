from rest_framework import serializers
from core.tags.person.models import Person

"""
This module has been defined in order to define a custom serializer
for Person object informations. Data will be convertend in a JSON format.
"""

class PersonSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic person object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Person
        fields = ('id', 'category', 'first_name', 'last_name', 'gender', 'birth_date') #, 'image')
