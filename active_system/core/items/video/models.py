from django.db import models
from core.items.models import Item

class VideoItem(Item):
    """
    This class is used to provide an object representation to a generic
    video item, extending the base attributes of an item with specific ones.
    """
    # TODO decidere se i campi sono obbligatori o possono essere nulli
    # inizialmente per poi essere compilati da appositi script
    frame_rate = models.IntegerField(null=True)
    frame_width = models.IntegerField(null=True)
    frame_height = models.IntegerField(null=True)
    duration = models.BigIntegerField(null=True) #seconds
    format = models.CharField(max_length = 100, null=True)
    
    def __init__(self, *args, **kwargs):
        super(VideoItem,self).__init__(*args, **kwargs)
        self.type = 'video'

    def __repr__(self):
        return 'VideoItem ', self.filename
