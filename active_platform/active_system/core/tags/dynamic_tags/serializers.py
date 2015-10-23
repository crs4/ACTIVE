# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define all classes needed to create a REST API,
in order to convert DynamicTag objects from and to JSON format.
"""

from rest_framework import serializers
from core.tags.dynamic_tags.models import DynamicTag


class DynamicTagSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for a dynamic tag object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = DynamicTag
        fields = ('id', 'tag', 'start', 'duration', 'x_position',
                  'y_position', 'size_width', 'size_height')
