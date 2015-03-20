
from core.items.serializers import ItemSerializer
from core.items.audio.models import AudioItem


class AudioItemSerializer(ItemSerializer):
    """
    """
    class Meta(ItemSerializer.Meta):
        model = AudioItem
        fields = ('id','type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner', 'bits_per_sample', 'sample_rate', 'num_channels', 'duration','format','file')

