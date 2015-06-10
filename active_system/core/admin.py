"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from core.active_tools.models import ActiveTools
#from core.users.models.py import ActiveUser
from core.items.models import Item
from core.items.video.models import VideoItem
from core.items.image.models import ImageItem
from core.items.audio.models import AudioItem
from core.plugins.models import Event, Action, Plugin, Script
from core.tags.models import Tag,Entity
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.person.models import Person
from core.tags.keywords.models import Keyword


# adding the models.py that will be available on Django interface
admin.site.register(ActiveTools)
#admin.site.register(ActiveUser)
admin.site.register(Item)
admin.site.register(VideoItem)
admin.site.register(ImageItem)
admin.site.register(AudioItem)
admin.site.register(Plugin)
admin.site.register(Script)
admin.site.register(Event)
admin.site.register(Action)
admin.site.register(Tag)
admin.site.register(DynamicTag)
admin.site.register(Entity)
admin.site.register(Person)
admin.site.register(Keyword)
