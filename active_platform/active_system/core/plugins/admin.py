"""
This module is used in order to include the available data
models on the Django admin interface.
"""
from django.contrib import admin
from core.plugins.models import Plugin, Script, Action, Event


# adding the models.py that will be available on Django interface
admin.site.register(Plugin)
admin.site.register(Script)
admin.site.register(Action)
admin.site.register(Event)

