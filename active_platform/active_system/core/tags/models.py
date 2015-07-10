"""
Module used to define the data model for Entity and Tag objects.
"""

from django.db import models
from core.items.models import Item
import logging

from django.db.models.signals import post_delete,pre_delete

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
    
    print('Deleting all orphan Entities, after '+instance.__class__.__name__+' '+ str(instance.id) +' deletion') 
    # save the entity reference
    temp = instance.entity.id   
    # check if the entity is used (on another Tag object)
    # if not delete the entity object
    if Tag.objects.filter(entity_id = temp).count() == 0:
        Entity.objects.filter(pk = temp).delete()
 
      
 
    
#Connect the post_delete signal (associated with the Tag class), with the delete_entity method 
pre_delete.connect(delete_entity, sender=Tag)



