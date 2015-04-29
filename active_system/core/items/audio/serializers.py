from core.items.serializers import ItemSerializer
from core.items.audio.models import AudioItem
from rest_framework.pagination import PageNumberPagination

class AudioItemSerializer(ItemSerializer):
    """
    This class defines a JSON serializer for audio digital items
    extending the basic item metadata.
    """
    class Meta(ItemSerializer.Meta):
        model = AudioItem
        fields = ('id', 'description', 'type', 'mime_type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 
		  'owner', 'bits_per_sample', 'sample_rate', 'num_channels', 'duration', 'format', 'file', 'thumb', 'preview')


class AudioItemPagination(PageNumberPagination):
    """
    This class has been defined in order to paginate audio items.
    """
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 24
