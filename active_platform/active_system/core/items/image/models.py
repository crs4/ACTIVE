"""
This module is used to define the Image item data model.
The class used extends the generic Item object class,
defining new fields and overriding methods if necessary.
"""

from django.db import models
from core.items.models import Item


class ImageObjectOwnerManager(models.Manager):
    """
    Class used to implement a methothat will be used to specify
    dynamically the item owner.
    """
    def by_user(self, user):
        """
        Method used to  filter the items by user basis.
        """
        return super(ImageObjectOwnerManager, self).get_queryset().filter(owner=user)


class ImageItem(Item):
    """
    This class has been defined in order to extend a generic
    item metadata and support image specific data.
    """
    frame_width = models.IntegerField(null=True)
    frame_height = models.IntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    # custom object manager
    objects = models.Manager()
    user_objects = ImageObjectOwnerManager()
    
    def __init__(self, *args, **kwargs):
        super(ImageItem,self).__init__(*args, **kwargs)
        self.type = 'image'
