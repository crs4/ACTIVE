# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the serializer necessary to provide a REST API for Action objects.
"""

from rest_framework import serializers
from core.plugins.models import Action


class ActionSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Event objects.
    """
    class Meta:
        model = Action
        fields = ('id', 'path_abs', 'events')


