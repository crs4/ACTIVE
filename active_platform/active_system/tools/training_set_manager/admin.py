"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from tools.training_set_manager.models import Instance, EntityModel


# adding the models.py that will be available on Django interface
admin.site.register(Instance)
admin.site.register(EntityModel)
