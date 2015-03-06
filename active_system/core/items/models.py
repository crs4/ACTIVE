from django.db import models
from django.contrib.auth.models import User
from abc import ABCMeta
import datetime


class Item(models.Model):
    """
    This class provides an object representation for
    any multimediafile that could be stored by the platform.
    """
    type = models.CharField(max_length = 100, null=True)
    title = models.CharField(max_length = 100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    filesize = models.IntegerField(default = 0, null=True)
    visibility = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User)
    file = models.FileField()
    #path = models.CharField(max_length = 200)
    
    def __repr__(self):
        return 'Item ', self.title, ' ', self.type

  

    def set_visibility(self, flag):
	"""
	Method used to set item visibility through a boolean flag.
	:param flag: Boolean flag used to decide if the item is public or not.
	"""
        if(flag):
	    self.published_at = datetime.datetime.now()
 	
        self.visibility = flag


class VideoItem(Item):
    bitrate = models.IntegerField(null = False)
    frame_width = models.IntegerField(null = False)
    frame_height = models.IntegerField(null = False)
    duration = models.BigIntegerField(null = False)
    format = models.CharField(max_length = 100)


    def __repr__(self):
        return 'VideoItem ', self.title, ' ', self.type


class ImageItem(Item):
    frame_width = models.IntegerField(null = False)
    frame_height = models.IntegerField(null = False)
    format = models.CharField(max_length = 100)

    def __repr__(self):
        return 'ImageItem ', self.title, ' ', self.type


class AudioItem(Item):
    bitrate = models.IntegerField(null = False)
    duration = models.BigIntegerField(null = False)
    format = models.CharField(max_length = 100)

    def __repr__(self):
        return 'AudioItem ', self.title, ' ', self.type
