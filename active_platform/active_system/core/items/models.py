"""
This module used to define the data model for a generic Item object.
Item model class redefines some methods in order to handle the
storage of file resources.
A custom object manager has been defined in order to retrieve only the
items owned by a specific user.
"""

import datetime
import os
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def compute_upload_path(instance, filename):
    """
    Function used to generate the correct absolute path of uploaded resources.
    This function has been defined also to avoid the overlapping between
    different items uploaded at the same time.
    """
    return os.path.join('items', str(instance.id), filename)


class ObjectOwnerManager(models.Manager):
    """
    Class used to implement a methothat will be used to specify
    dynamically the item owner.
    """
    def by_user(self, user):
        """
        Method used to  filter the items by user basis.
        """
        return super(ObjectOwnerManager, self).get_queryset().filter(owner=user)
        #return super(ObjectOwnerManager, self).get_query_set().filter(owner=user)


class Item(models.Model):
    """
    This class provides an object representation for
    any multimedia file that could be stored by the platform.
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
    file = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    thumb = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    preview = models.FileField(upload_to=compute_upload_path, null=True, blank=True)
    state = models.CharField(max_length=300, default='STORED')
    # custom object manager
    objects = models.Manager()
    user_objects = ObjectOwnerManager()

    def __repr__(self):
        return 'Item ' + self.filename + ' ' + self.type

    def __unicode__(self):
        return str(self.id) + ' - ' + self.type + ' - ' + self.filename

    def save(self, *args, **kwargs):
        """
        Method overridden in order to correctly store a digital item.
        """
        temp = self.file
        self.file = None
        super(Item, self).save(*args, **kwargs)

        # save the item with a file resource associated
        self.file = temp
        self.__set_visibility()
        super(Item, self).save()

    def delete(self, *args, **kwargs):
        """
        Method overridden in order to correctly delete all stored information about an item.
        """
        try:
            shutil.rmtree(settings.MEDIA_ROOT + '/items/' + str(self.id) + '/')
        except:
            pass
        super(Item, self).delete(*args, **kwargs)

    def __set_visibility(self):
        """
        Method used to set the time when the item visibility has been set to public (True).
        """
        if(self.visibility):
            self.published_at = datetime.datetime.now()
        else:
            self.published_at = None
