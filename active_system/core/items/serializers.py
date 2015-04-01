from rest_framework import serializers
from models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic digital items.
    Only main field of a digital item are converted in a JSON format.
    """
    class Meta:
        model = Item
        fields = ('id','type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner', 'file', 'thumb')
