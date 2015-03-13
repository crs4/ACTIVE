from django.db import models
from core.items.models import Item


class ImageItem(Item):
    """
    This class has been defined in order to extend a generic
    item and support image specific data.
    """
    frame_width = models.IntegerField(null = False)
    frame_height = models.IntegerField(null = False)
    format = models.CharField(max_length = 100)
    
    def __init__(self, *args, **kwargs):
        super(ImageItem,self).__init__(*args, **kwargs)
        self.type = 'image'

    def __repr__(self):
        return 'ImageItem ', self.filename, ' ', self.type

