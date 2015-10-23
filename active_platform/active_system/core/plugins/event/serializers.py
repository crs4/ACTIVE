# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the class needed to provide a REST API for Event objects.
The serializer defined in this class allow to convert Event data to and from the JSON format.
"""

from rest_framework import serializers
from core.plugins.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objects.
    """
    class Meta:
        model = Event
        fields = ('id', 'name', 'description')