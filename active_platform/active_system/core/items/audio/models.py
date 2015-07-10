"""
This module contain the class used to define the Audio item objects
data model. Audio item class extends the generic Item properties.
"""

from django.db import models
from core.items.models import Item


class AudioItem(Item):
    """
    This class is used to define the content model for
    audio digital items extending all fields provided by
    a generic Item object.
    """
    sample_rate = models.IntegerField(null=True)
    bits_per_sample = models.IntegerField(null=True)
    num_channels = models.IntegerField(null=True)
    duration = models.BigIntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    
    def __init__(self, *args, **kwargs):
        super(AudioItem, self).__init__(*args, **kwargs)
        self.type = 'audio'

