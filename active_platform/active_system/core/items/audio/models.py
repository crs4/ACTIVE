# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contain the class used to define the Audio item objects
data model. Audio item class extends the generic Item properties.
"""

from django.db import models
from core.items.models import Item

class AudioOwnerManager(models.Manager):
    """
    Class used to implement a methothat will be used to specify
    dynamically the item owner.
    """
    def by_user(self, user):
        """
        Method used to  filter the items by user basis.
        """
        return super(AudioOwnerManager, self).get_queryset().filter(owner=user)


class AudioItem(Item):
    """
    This class is used to define the content model for
    audio digital items extending all fields provided by
    a generic Item object.
    """
    sample_rate = models.IntegerField(null=True)
    bits_per_sample = models.IntegerField(null=True)
    num_channels = models.IntegerField(null=True)
    duration = models.BigIntegerField(null=True)
    objects = models.Manager()
    user_objects = AudioOwnerManager()
    
    def __init__(self, *args, **kwargs):
        super(AudioItem, self).__init__(*args, **kwargs)
        self.type = 'audio'

