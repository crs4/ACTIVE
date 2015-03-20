
from rest_framework import serializers
from models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner','file')
