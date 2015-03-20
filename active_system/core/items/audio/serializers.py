from core.items.serializers import ItemSerializer
from core.items.audio.models import AudioItem

class AudioItemSerializer(ItemSerializer):
    """
    This class defines a JSON serializer for audio digital items
    extending the basic item metadata.
    """
    class Meta(ItemSerializer.Meta):
        model = AudioItem
        fields = ('id', 'type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 
		  'owner', 'bits_per_sample', 'sample_rate', 'num_channels', 'duration', 'format', 'file')

