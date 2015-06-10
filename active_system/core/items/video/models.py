"""
This module contains the class which defines the data model for video digital items.
This class extends the generic Item object class adding specific field
for Video item objects.
"""

from django.db import models
from core.items.models import Item
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

class VideoItem(Item):
    """
    This class is used to define the content model of video digital item, 
    extending the base attributes provided by a generic digital item.
    """
    frame_rate = models.FloatField(null=True, blank=True)
    frame_width = models.IntegerField(null=True, blank=True)
    frame_height = models.IntegerField(null=True, blank=True)
    duration = models.BigIntegerField(null=True, blank=True) #seconds
    format = models.CharField(max_length=100, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(VideoItem, self).__init__(*args, **kwargs)
        self.type = 'video'
        logger.debug('Creating a new VideoItem object')