# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes needed to provide a REST API to Video item objects.
The defined classes are:
    - a serializer used to convert the video items in a JSON format;
    - a paginator needed to handle the potentially big amount of retrieved video items.
"""

from core.items.serializers import ItemSerializer
from core.items.video.models import VideoItem
from rest_framework.pagination import PageNumberPagination


class VideoItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serializer that will
    be used to define a REST API for VideoItem objects.
    """
    class Meta(ItemSerializer.Meta):
        model = VideoItem
        fields = ('id', 'description', 'type', 'mime_type', 'filename',
                  'filesize', 'visibility', 'uploaded_at', 'published_at',
                  'frame_rate', 'frame_width', 'frame_height', 'duration',
                  'file', 'thumb', 'preview', 'state', 'owner')


class VideoItemPagination(PageNumberPagination):
    """
    This class is used to create a paginator for video item object.
    Results are returned setting the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
