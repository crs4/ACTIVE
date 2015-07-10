"""
This module is used to define the classes necessary in order to define a REST API.
Two classes has been defined:
    - a serializer used to convert generic Item objects in JSON format;
    - a paginator necessary to handle the potentially big amount of retrieved items.
"""

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
        fields = ('id', 'description', 'type', 'mime_type', 'filename',
                  'filesize', 'visibility', 'uploaded_at', 'published_at',
                  'file', 'thumb', 'preview', 'state')#, 'owner')


class ItemPagination(PageNumberPagination):
    """
    This class is used to create a paginator for video item
    object. Results are returned providing the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
