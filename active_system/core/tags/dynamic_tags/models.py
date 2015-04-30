"""
Module used to define the data model for dynamic tag objects.
A dynamic tag is an occurrence of an Entity object in a generic Item object
which presents some temporal information.
So the occurrence is enriched providing more information about when and
 where the occurrence appears.
"""

from django.db import models
from core.tags.models import Tag


class DynamicTag(models.Model):
    """
    Class used to define the object representation of a tag
    related to a digital item containing temporal information.
    Each occurrence is extended when and where the entity occurred.
    """
    tag = models.ForeignKey(Tag)
    start = models.BigIntegerField(blank=True)
    duration = models.BigIntegerField(blank=True)
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)
    size_width = models.IntegerField(default=0)
    size_height = models.IntegerField(default=0)