"""
This module contains all class necessary to define a REST API for
Audio item objects using Django REST framework.
Two class has been defined:
    - a serializer necessary to convert Audio item objects in JSON format;
    - a paginator necessary to handle the potentially big amount
    of retrieved Audio item objects through pagination.
"""

from core.items.serializers import ItemSerializer
from core.items.audio.models import AudioItem
from rest_framework.pagination import PageNumberPagination


class AudioItemSerializer(ItemSerializer):
    """
    This class defines a JSON serializer for audio digital items
    extending the basic digital item metadata.
    """

    class Meta(ItemSerializer.Meta):
        model = AudioItem
        #fields = ('id', 'description', 'type', 'mime_type', 'filename',
        #          'filesize', 'visibility', 'uploaded_at', 'published_at',
        #          'owner', 'bits_per_sample', 'sample_rate', 'num_channels',
        #          'duration', 'format', 'file', 'thumb', 'preview', 'state')


class AudioItemPagination(PageNumberPagination):
    """
    This class has been defined in order to paginate audio items.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
