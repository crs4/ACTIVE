# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define the data model for Person entities.
For each person that will be used by the platform it will be
used to create a object with personal information fields.
"""

from core.tags.models import Entity
from django.db import models
import os

def compute_upload_path(instance, filename):
    """
    Function used to generate the correct absolute path of uploaded resources.
    This function has been defined also to avoid the overlapping between
    different items uploaded at the same time.
    """
    return os.path.join('persons',str(instance.id),filename)


class Person(Entity):
    """
    This class extends the Entity class in order to provide
    additional fields for a person.
    This class allow to extend the entities that could occur in
    a digital item.
    """
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.FileField(upload_to=compute_upload_path, default='persons/unknown_user.png')

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        self.category = 'Person - ' + self.first_name + ' ' + self.last_name + ' ' + str(self.id)
        super(Person, self).save()
