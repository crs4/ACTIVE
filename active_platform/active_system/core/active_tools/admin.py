"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from core.active_tools.models import ActiveTools

# adding the models.py that will be available on Django interface
admin.site.register(ActiveTools)
