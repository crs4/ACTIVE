# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been defined in order to define a custom serializer
for Keyword object information. Data will be converted from and to a
JSON format in order to provide a REST API.
"""

from rest_framework import serializers
from core.tags.keywords.models import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic keywords object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Keyword
        fields = ('id', 'category', 'description')
