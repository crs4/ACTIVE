from django.contrib import admin
from core.users.models import ActiveUser
from core.items.models import Item
from core.items.video.models import VideoItem
from core.items.image.models import ImageItem
from core.items.audio.models import AudioItem
from core.plugins.models import Event, Action, Plugin, Script

# Register your models here.
admin.site.register(ActiveUser)
admin.site.register(Item)
admin.site.register(VideoItem)
admin.site.register(ImageItem)
admin.site.register(AudioItem)
admin.site.register(Plugin)
admin.site.register(Script)
admin.site.register(Event)
admin.site.register(Action)
