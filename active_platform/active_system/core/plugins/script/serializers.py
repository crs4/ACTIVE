# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contain the class which is used to serialize Script objects from
and to a JSON format.
This class will be used in order to provide a REST API for Script objects.
"""

from rest_framework import serializers
from core.plugins.models import Script


class ScriptSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Script objects.
    """
    class Meta:
        model = Script
        fields = ('id', 'title', 'details', 'path', 'job_name',
                  'plugin', 'events', 'item_type')
        depth = 2

