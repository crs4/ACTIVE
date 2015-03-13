from django.db import models
from core.items.models import Item


class AudioItem(Item):
    """
    """
    bitrate = models.IntegerField(null = False)
    duration = models.BigIntegerField(null = False)
    format = models.CharField(max_length = 100)
    
    def __init__(self, *args, **kwargs):
        super(AudioItem,self).__init__(*args, **kwargs)
        self.type = 'audio'

    def __repr__(self):
        return 'AudioItem ', self.filename, ' ', self.type
