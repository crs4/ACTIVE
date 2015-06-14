"""
Module used to define the data model for Entity and Tag objects.
"""

from django.db import models
from core.items.models import Item
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

    # questa delete non verra' mai chiamata alla cancellazione
    # di un tag in quanto avviene solo sul database, lato SQL!!!
    def delete(self, *args, **kwargs):
        """
        This method override the standard delete method.
        After deleting the current Tag object it checks if the associated
        Entity is used by other Tag objects (byu reference). If there is not other uses
        the entity object is deleted, avoiding pending objects in the database.

        :param args: Arguments used for the Tag deletion
        :param kwargs: Key arguments used for the Tag deletion
        """
        logger.debug('Deleting Tag object ' + self.pk + ' and all orphan Entities')
        # save the entity reference
        temp = self.entity.id
        # delete the tag
        super(Tag, self).delete()
        # check if the entity is used (on another Tag object)
        # if not delete the entity object
        if Tag.objects.filter(entity__id = temp).count() == 0:
            Entity.objects.filter(pk = temp).delete()