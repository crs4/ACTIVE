# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from core.items.models import Item
from core.items.video.models import VideoItem
from core.items.image.models import ImageItem
from core.items.audio.models import AudioItem


# adding the models.py that will be available on Django interface
admin.site.register(Item)
admin.site.register(VideoItem)
admin.site.register(ImageItem)
admin.site.register(AudioItem)
