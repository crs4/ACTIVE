# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the serializer needed to convert Plugin objects to
and from a JSON format, in order to create a REST API.
"""

from rest_framework import serializers
from core.plugins.models import Plugin


class PluginSerializer(serializers.ModelSerializer):
    """
    Method used for JSON serialization of Plugin objects.
    """
    class Meta:
        model = Plugin
        fields = ('id', 'name', #'title', 
                  'description', 'active_version',
                  'plugin_version', 'url_info', 'authors')

