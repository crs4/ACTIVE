from django.contrib import admin

from core.models import Person
from core.models import Item
from core.models import Occurrence

admin.site.register(Person)
admin.site.register(Item)
admin.site.register(Occurrence)
