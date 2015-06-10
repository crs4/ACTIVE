"""
This module used to define the data model for generic Item objects.
Item model class redefines some methods in order to handle the
storage of resources on the current file system.
"""

import datetime
import os
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

def compute_upload_path(instance, filename):
    """
    Function used to generate the correct absolute path of uploaded resources.
    This function has been defined also to avoid the overlapping between
    different items uploaded at the same time.
    """
    return os.path.join('items', str(instance.id), filename)


class Item(models.Model):
    """
    This class provides an object representation for a generic digital item
    that could be stored by the platform.
    """
    type = models.CharField(max_length=100, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    filename = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    filesize = models.CharField(max_length = 10, blank=True)
    visibility = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    #owner = models.py.ForeignKey(User)
    file = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    thumb = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    preview = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    state = models.CharField(max_length=300, default='', blank=True)

    def __repr__(self):
        return str(self.id) + ' - ' + self.type + ' ' + self.filename

    def __unicode__(self):
        return str(self.id) + ' - ' + self.type + ' - ' + self.filename

    def save(self, *args, **kwargs):
        """
        This method has been overridden to store a digital item in the file system.
        """
        temp = self.file
        self.file = None
        self.__set_visibility()
        self.full_clean()
        super(Item, self).save(*args, **kwargs)

        # save the item with a file resource associated
        self.file = temp
        super(Item, self).save()
        logger.debug('Item object ' + str(self.id) + ' successfully saved')

    def delete(self, *args, **kwargs):
        """
        This method has been overridden to delete all
        resources associated to an Item object.
        """

        # remove the directory associated to an item
        shutil.rmtree(settings.MEDIA_ROOT + '/items/' + str(self.id) + '/')
        # delete all data stored for the current item
        super(Item, self).delete(*args, **kwargs)
        logger.debug('Deleted all resources associated to Item object ' + str(self.id))

    def __set_visibility(self):
        """
        Method used to set the time when the item visibility has been set to public (True).
        """
        if self.visibility:
            self.published_at = datetime.datetime.now()
        else:
            self.published_at = None
