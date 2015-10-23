# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes necessary to provide a object representation for
the data necessary to manage different type of training sets.
"""

from core.tags.models import Entity
from core.tags.dynamic_tags.models import DynamicTag
from core.items.models import Item
from django.conf import settings
from django.db import models
import os, shutil, datetime


def models_upload_path(instance, filename):
    """
    Function used to generate the correct upload path for EntityModel resources.
    """
    return os.path.join('models', str(instance.id), filename)

def instances_upload_path(instance, filename):
    """
    Function used to generate the correct upload path for Instance resources.
    """
    return os.path.join('instances', str(instance.id), filename)


class EntityModel(models.Model):
    """
    Class used to provide an object representation to recognition model for entity objects.
    """
    name = models.CharField(max_length=300, default="Generic Entity model")
    entity = models.ForeignKey(Entity)
    model_file = models.FileField(upload_to=models_upload_path, blank=True, null=True)
    type = models.CharField(max_length=50)
    last_update = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + ' - ' + self.type

    def __str__(self):
        return str(self.id) + ' - ' + self.type

    def save(self, *args, **kwargs):
        """
        Method overridden in order to correctly store a EntityModel.
        """
	super(EntityModel, self).save(*args, **kwargs)
        base_dir = os.path.join(settings.MEDIA_ROOT, 'models', str(self.id))
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        self.last_update = datetime.datetime.now()
	super(EntityModel, self).save()

    
    def delete(self, *args, **kwargs):
        """
        Method overridden to remove all stored information about a EntityModel object.
        """
        try:
            # retrieve all instances associated to the model
            for i in Instance.objects.filter(entity_model=self):
                 i.entity_model = None
                 i.save()
            shutil.rmtree(settings.MEDIA_ROOT + '/models/' + str(self.id) + '/')
            super(EntityModel, self).delete(*args, **kwargs)
        except Exception as e:
            print e
            print "Error on entity model deletion"


class Instance(models.Model):
    """
    Class used to provide the object representation to Instance objects.
    """
    thumbnail = models.FileField(upload_to=instances_upload_path, blank=True, null=True, default='thumbnails/generic_file.jpeg')
    features  = models.FileField(upload_to=instances_upload_path, blank=True, null=True)
    trusted = models.BooleanField(default=False)
    type = models.CharField(max_length=50)
    entity_model = models.ForeignKey(EntityModel, blank=True, null=True)
    item = models.ForeignKey(Item, blank=True, null=True)
    dtag = models.ForeignKey(DynamicTag, blank=True, null=True)


    def __unicode__(self):
        return str(self.id) + ' - ' + self.type

    def save(self, *args, **kwargs):
        """
        Method overridden in order to correctly store an Instance object.
        """
        super(Instance, self).save(*args, **kwargs)
        base_dir = os.path.join(settings.MEDIA_ROOT, 'models', str(self.id))
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        super(Instance, self).save()
    
    def delete(self, *args, **kwargs):
        """
        Method overridden to remove all stored information about a Instance object.
        """
        try:
            shutil.rmtree(settings.MEDIA_ROOT + '/instances/' + str(self.id) + '/')
            super(Instance, self).delete(*args, **kwargs)

        except Exception as e:
            print e
            print "Error on Instance deletion"    
