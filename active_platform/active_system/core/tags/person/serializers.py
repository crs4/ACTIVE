# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the class necessary to define a custom serializer
for Person objects. Data will be converted from and to a JSON format,
in order to provide a .
"""

from rest_framework import serializers
from core.tags.person.models import Person
from rest_framework.pagination import PageNumberPagination

class PersonSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic person object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Person
        fields = ('id', 'category', 'first_name', 'last_name',
                  'gender', 'birth_date', 'image')


class PersonPagination(PageNumberPagination):
    """
    This class is used to create a paginator for person object.
    Results are returned setting the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
