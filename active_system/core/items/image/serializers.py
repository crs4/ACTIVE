"""
This module contains all classes needed to define a REST API for ImageItem objects.
Two classes has been defined:
    - a serializer used to convert each ImageItem object in a JSON format;
    - a paginator necessary to retrieve a potentially big amount of ImageItem objects.
"""

from core.items.serializers import ItemSerializer
from core.items.image.models import ImageItem
from rest_framework.pagination import PageNumberPagination


class ImageItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serialized that will be used
    to define a REST API for ImageItem objects manipulations.
    """
    class Meta(ItemSerializer.Meta):
        model = ImageItem
        #fields = ('id', 'description', 'type', 'mime_type', 'filename',
        #          'filesize', 'visibility', 'uploaded_at', 'published_at',
        #          'owner', 'frame_width', 'frame_height', 'format',
        #          'file', 'thumb', 'preview', 'state')


class ImageItemPagination(PageNumberPagination):
    """
    This class has been used in order to paginate ImageItem objects.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32