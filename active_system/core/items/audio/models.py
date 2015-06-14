"""
This module contain the class used to define the data model for audio digital items.
Audio item class extends the generic Item properties.
"""

from django.db import models
from core.items.models import Item
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class AudioItem(Item):
    """
    This class is used to define the content model for
    audio digital items extending fields provided by
    a generic Item object.
    """
    sample_rate = models.IntegerField(null=True, blank=True)
    bits_per_sample = models.IntegerField(null=True, blank=True)
    num_channels = models.IntegerField(null=True, blank=True)
    duration = models.BigIntegerField(null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(AudioItem, self).__init__(*args, **kwargs)
        self.type = 'audio'

    def save(self, *args, **kwargs):
        super(AudioItem, self).save(*args, **kwargs)
        logger.debug('Saved a new Audio digital item ' + str(self.id))