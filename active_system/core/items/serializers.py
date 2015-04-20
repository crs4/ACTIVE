from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


from core.items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic digital items.
    Only main field of a digital item are converted in a JSON format.
    """
 
    class Meta:
        model = Item
        fields = ('id', 'description', 'type', 'mime_type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner', 'file', 'thumb')

class ItemPagination(PageNumberPagination):
    """
    This class is used to create a paginator for video item
    object. Results are returned specifing the maximum number of results per page.
    """
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 24

