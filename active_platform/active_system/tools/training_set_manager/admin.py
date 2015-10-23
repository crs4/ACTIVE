# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from tools.training_set_manager.models import Instance, EntityModel

admin.site.register(Instance)
admin.site.register(EntityModel)
