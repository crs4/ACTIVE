from core.items.serializers import ItemSerializer
from core.items.video.models import VideoItem

class VideoItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serializer that will
    be used to define a REST API for VideoItem objects.
    """
    class Meta(ItemSerializer.Meta):
        model = VideoItem
        fields = ('id', 'type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner', 
		  'frame_rate', 'frame_width', 'frame_height', 'duration', 'format', 'file', 'thumb')
