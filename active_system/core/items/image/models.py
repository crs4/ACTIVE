"""
This module is used to define the data model for image digital items.
The class used extends the generic Item object class,
defining new fields and overriding methods if necessary.
"""

from django.db import models
from core.items.models import Item
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ImageItem(Item):
    """
    This class extend a generic Item metadata
    and it supports image specific data.
    """
    frame_width = models.IntegerField(null=True, blank=True)
    frame_height = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(ImageItem,self).__init__(*args, **kwargs)
        self.type = 'image'
        logger.debug('Creating a new ImageItem object')

