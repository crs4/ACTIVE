# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define the data model for Entity and Tag objects.
"""

from core.items.models import Item
from django.db import models
from django.db.models.signals import post_delete,pre_delete
import logging


# variable used for logging purposes
logger = logging.getLogger('active_log')

class Entity(models.Model):
    """
    Class used to define the object representation for a generic entity.
    """
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Entities"

    def __unicode__(self):
        return self.category


class UserTagManager(models.Manager):
    """
    Custom manager used to retrieve only the tags associated to items owned by the user.
    """
    def by_user(self, user):
        return super(UserTagManager, self).get_queryset().filter(item__owner=user)


class Tag(models.Model):
    """
    Class used to define the object representation for a generic
    tag information.
    A Tag object is used to represent the occurrence of a generic instance
    in a generic digital item.
    """
    type = models.CharField(max_length=100, blank=True)
    entity = models.ForeignKey(Entity)
    item = models.ForeignKey(Item)
    # custom object manager
    objects = models.Manager()
    user_objects = UserTagManager()

    def __unicode__(self):
        return str(self.id) + ' - ' + self.type


def delete_entity(sender, instance, **kwargs):
    """
    This method is called after a Tag deletion.
    It checks if the associated Entity is used by other Tag objects (by reference). 
    If there is not other uses the entity object is deleted, avoiding pending objects in the database.
    
    :param sender: The model class that sends the signal
    :param instance: The actual instance being deleted
    :param kwargs: Key arguments used for the Tag deletion
    """
    
    logger.debug('Deleting all orphan Entities, after '+instance.__class__.__name__+' '+ str(instance.id) +' deletion') 
    # save the entity reference
    temp = instance.entity.id   
    # check if the entity is used (on another Tag object)
    # if not delete the entity object
    if Tag.objects.filter(entity_id = temp).count() == 0:
        Entity.objects.filter(pk = temp).delete()


    
#Connect the post_delete signal (associated with the Tag class), with the delete_entity method 
pre_delete.connect(delete_entity, sender=Tag)



