"""
Module used to define the data model for Keywords objects.
In this
"""

from django.db import models
from core.tags.models import Entity


class Keyword(Entity):
    """
    This class extends the Entity class in order to provide
    additional fields for a keywords.
    A keywords is a sequence of alphanumeric characters that are
    associated to a digital item.
    """
    description = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        super(Keyword, self).save(*args, **kwargs)
        self.description = self.description.strip().lower().replace(' ', '_')
        self.category = 'Keyword - ' + self.description
        super(Keyword, self).save()