from django.db import models
from core.items.models import Item

class VideoItem(Item):
    """
    This class is used to provide an object representation to a generic
    video item, extending the base attributes of an item with specific ones.
    """
    # TODO decidere se i campi sono obbligatori o possono essere nulli
    # inizialmente per poi essere compilati da appositi script
    bitrate = models.IntegerField(null = False)
    frame_width = models.IntegerField(null = False)
    frame_height = models.IntegerField(null = False)
    duration = models.BigIntegerField(null = False)
    format = models.CharField(max_length = 100)
    
    def __init__(self, *args, **kwargs):
        super(VideoItem,self).__init__(*args, **kwargs)
        self.type = 'video'

    def __repr__(self):
        return 'VideoItem ', self.filename, ' ', self.type
