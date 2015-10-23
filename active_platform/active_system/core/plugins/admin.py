# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used in order to include the available data
models on the Django admin interface.
"""
from django.contrib import admin
from core.plugins.models import Plugin, Script, Action, Event

admin.site.register(Plugin)
admin.site.register(Script)
admin.site.register(Action)
admin.site.register(Event)

