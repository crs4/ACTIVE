"""
This module is used to define the Image item data model.
The class used extends the generic Item object class,
defining new fields and overriding methods if necessary.
"""

from django.db import models
from core.items.models import Item


class ImageItem(Item):
    """
    This class has been defined in order to extend a generic
    item metadata and support image specific data.
    """
    frame_width = models.IntegerField(null=True)
    frame_height = models.IntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    
    def __init__(self, *args, **kwargs):
        super(ImageItem,self).__init__(*args, **kwargs)
        self.type = 'image'

