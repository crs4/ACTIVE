# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tools.xmp.models import XMPMetadata
from rest_framework import serializers

class XMPMetadataSerializer(serializers.ModelSerializer):
    """
    Class used to define the serialzer for XMPMetadata object.
    """
    class Meta:
        model = XMPMetadata
        fields = ('id', 'item', 'metadata')
