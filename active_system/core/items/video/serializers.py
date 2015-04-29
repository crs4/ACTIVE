from core.items.serializers import ItemSerializer
from core.items.video.models import VideoItem
from rest_framework.pagination import PageNumberPagination

class VideoItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serializer that will
    be used to define a REST API for VideoItem objects.
    """
    class Meta(ItemSerializer.Meta):
        model = VideoItem
        fields = ('id', 'description', 'type', 'mime_type', 'filename', 'filesize', 'visibility', 'uploaded_at', 'published_at', 'owner', 
		  'frame_rate', 'frame_width', 'frame_height', 'duration', 'format', 'file', 'thumb', 'preview')


class VideoItemPagination(PageNumberPagination):
    """
    This class is used to create a paginator for video item
    object. Results are returned specifing the maximum number of results per page.
    """
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 24
