# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from core.items.models import Item


class XMPMetadata(models.Model):
    """
    Class used to associate a set of metadata
    to an existing Item object.
    Metadata is represented in the XMP format and
    is stored inside a char field for simplicity.
    """
    item     = models.ForeignKey(Item)
    metadata = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.item.filename
    
    def __repr__(self):
        return self.item.filename
