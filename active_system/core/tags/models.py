"""
Module used to define the data model for Entity and Tag objects.
"""

from django.db import models
from core.items.models import Item


class Entity(models.Model):
    """
    Class used to define the object representation for a generic entity.
    """
    category = models.CharField(max_length=100)

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
        return self.id + ' - ' + self.type