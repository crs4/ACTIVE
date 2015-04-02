from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from abc import ABCMeta
import datetime
import os
import shutil

"""
Module used to define the ACTIVE core data model.
"""

class Item(models.Model):
    """
    This class provides an object representation for
    any multimediafile that could be stored by the platform.
    """
    type = models.CharField(max_length=100, blank=True)
    filename = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    filesize = models.CharField(max_length = 10, blank=True)
    visibility = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User)
    file = models.FileField(null=True)
    thumb = models.FileField(null=True)
    
    def __repr__(self):
        return 'Item ', self.filename, ' ', self.type

    def __unicode__(self):
	return str(self.id) + ' - ' + self.type + " - '" + self.filename + "'"

    def save(self, *args, **kwargs):
	"""
	Method overrided in order to correctely store a digital item.
	"""

	# save the item without a file
	temp = self.file
	self.file = None
	super(Item, self).save(*args, **kwargs)
	
	# create the path where the file will be stored
	# TODO	save the thumbnail image in a folder named "thumbnail"
	self.file = temp
	for field in self._meta.fields:
		if field.name == 'file' or field.name == 'thumb' :
			field.upload_to = str(self.id) + '/'
			

	# delete the file if it already exists
	#if os.path.exists(self.file.path):
	#	shutil.rmtree(self.file.path)

	# set plublish data on item visibility
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
