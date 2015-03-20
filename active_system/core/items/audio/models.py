from django.db import models
from core.items.models import Item


class AudioItem(Item):
    """
    """
    sample_rate = models.IntegerField(null=True)
    bits_per_sample = models.IntegerField(null=True)
    num_channels = models.IntegerField(null=True)
    duration = models.BigIntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    
    def __init__(self, *args, **kwargs):
        super(AudioItem,self).__init__(*args, **kwargs)
        self.type = 'audio'

