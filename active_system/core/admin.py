from django.contrib import admin
from core.users.models import *
from core.items.models import *

# Register your models here.
admin.site.register(ActiveUser)
admin.site.register(Item)
admin.site.register(VideoItem)
admin.site.register(ImageItem)
admin.site.register(AudioItem)
