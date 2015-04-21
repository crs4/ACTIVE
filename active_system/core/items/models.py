from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from abc import ABCMeta
import datetime
import os
import shutil

from django.utils.encoding import force_unicode

"""
Module used to define the ACTIVE core data model.
"""


def compute_upload_path(instance, filename):
	"""
	Function used to upload all digital items inside the correct
	folder avoiding path overlapping between different items. 
	"""
	return os.path.join(str(instance.id), filename)

class Item(models.Model):
    """
    This class provides an object representation for
    any multimediafile that could be stored by the platform.
    """
    type = models.CharField(max_length=100, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    filename = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    filesize = models.CharField(max_length = 10, blank=True)
    visibility = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User)
    file = models.FileField(upload_to=compute_upload_path, null=True)
    thumb = models.FileField(upload_to=compute_upload_path, null=True)
    preview = models.FileField(upload_to=compute_upload_path, null=True)
    
    def __repr__(self):
        return 'Item ', self.filename, ' ', self.type

    def __unicode__(self):
	return str(self.id) + ' - ' + self.type + " - '" + self.filename + "'"

    def save(self, *args, **kwargs):
	"""
	Method overrided in order to correctely store a digital item.
	"""
	temp = self.file
	self.file = None
	super(Item, self).save(*args, **kwargs)
	
	# create the path where the file will be stored
	# TODO	save the thumbnail image in a folder named "thumbnail"
	self.file = temp

	self.__set_visibility()

	# save the item with a file associated
        super(Item, self).save()
	

    def delete(self, *args, **kwargs):
	"""
	Method overrided in order to correctely delete all stored information about an item.
	"""
	# remove the directory associated to an item
	shutil.rmtree(settings.MEDIA_ROOT + '/' + str(self.id) + '/')
	# delete all data stored for the current item
        super(Item, self).delete(*args, **kwargs)


    def __set_visibility(self):
	"""
	Method used to set the time when the item visibility has been set to public (True).
	"""
        if(self.visibility):
	    self.published_at = datetime.datetime.now()
	else:
	    self.published_at = None
