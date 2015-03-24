from core.items.serializers import ItemSerializer
from core.items.image.models import ImageItem

class ImageItemSerializer(ItemSerializer):
    """
    This class is used to define a JSON serialized that will be used
    to define a REST API for ImageItem manipulations.
    """
    class Meta(ItemSerializer.Meta):
        model = ImageItem
        fields = ('id', 'type', 'filename', 'filesize', 'visibility', 'uploaded_at',
		  'published_at', 'owner', 'frame_width', 'frame_height', 'format', 'file')
