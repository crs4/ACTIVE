
from rest_framework import serializers
from models import Item
from models import VideoItem
from models import AudioItem
from models import ImageItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','type', 'title', 'filesize', 'visibility', 'uploaded_at', 'visibility', 'published_at', 'owner', 'file')



class VideoItemSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = VideoItem
        fields = ('id','type', 'title', 'filesize', 'visibility', 'uploaded_at', 'visibility', 'published_at', 'owner', 'file','bitrate','frame_width','frame_height','duration','format')



class ImageItemSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = ImageItem
        fields = ('id','type', 'title', 'filesize', 'visibility', 'uploaded_at', 'visibility', 'published_at', 'owner', 'file','frame_width','frame_height','format')




class AudioItemSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = AudioItem
        fields = ('id','type', 'title', 'filesize', 'visibility', 'uploaded_at', 'visibility', 'published_at', 'owner', 'file','bitrate','duration','format')
