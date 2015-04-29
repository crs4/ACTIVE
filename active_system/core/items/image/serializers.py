from core.items.serializers import ItemSerializer
from core.items.image.models import ImageItem
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers

class ImageItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serialized that will be used
    to define a REST API for ImageItem manipulations.
    """
    class Meta(ItemSerializer.Meta):
        model = ImageItem
        fields = ('id', 'description', 'type', 'mime_type', 'filename', 'filesize', 'visibility', 'uploaded_at',
		  'published_at', 'owner', 'frame_width', 'frame_height', 'format', 'file', 'thumb', 'preview')




class ImageItemPagination(PageNumberPagination):
    """
    This class has been used in order to paginate image items.
    """
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 24
