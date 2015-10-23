# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
    description = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super(Keyword, self).save(*args, **kwargs)
        self.description = self.description.strip().lower().replace(' ', '_')
        self.category = 'Keyword - ' + self.description
        super(Keyword, self).save()
