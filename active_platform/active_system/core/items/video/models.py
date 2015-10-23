# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the class which defines the Video item data model.
This class extends the generic Item object class adding specific field
for Video item objects.
"""

from django.db import models
from core.items.models import Item



class VideoObjectOwnerManager(models.Manager):
    """
    Class used to implement a methothat will be used to specify
    dynamically the item owner.
    """
    def by_user(self, user):
        """
        Method used to  filter the items by user basis.
        """
        return super(VideoObjectOwnerManager, self).get_queryset().filter(owner=user)

class VideoItem(Item):
    """
    This class is used to define the content model of video digital item, 
    extending the base attributes provided by a generic digital item.
    """
    frame_rate = models.FloatField(null=True)
    frame_width = models.IntegerField(null=True)
    frame_height = models.IntegerField(null=True)
    duration = models.BigIntegerField(null=True) #seconds
    objects = models.Manager()
    user_objects = VideoObjectOwnerManager()
    
    def __init__(self, *args, **kwargs):
        super(VideoItem, self).__init__(*args, **kwargs)
        self.type = 'video'



