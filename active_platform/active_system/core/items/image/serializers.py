# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes needed to define a REST API for Image item objects.
Two classes has been defined:
    - a serializer used to convert each Image item in a JSON format;
    - a paginator necessary to retrieve a potentially big amount of Image items.
"""

from core.items.serializers import ItemSerializer
from core.items.image.models import ImageItem
from rest_framework.pagination import PageNumberPagination


class ImageItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serialized that will be used
    to define a REST API for ImageItem manipulations.
    """
    class Meta(ItemSerializer.Meta):
        model = ImageItem
        fields = ('id', 'description', 'type', 'mime_type', 'filename',
                  'filesize', 'visibility', 'uploaded_at', 'published_at',
                  'frame_width', 'frame_height',
                  'file', 'thumb', 'preview', 'state', 'owner')


class ImageItemPagination(PageNumberPagination):
    """
    This class has been used in order to paginate Image items.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
