# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used in order to include the available data
models on the Django admin interface.
"""

from django.contrib import admin
from core.tags.models import Tag,Entity
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.person.models import Person
from core.tags.keywords.models import Keyword


# adding the models.py that will be available on Django interface
admin.site.register(Tag)
admin.site.register(DynamicTag)
admin.site.register(Entity)
admin.site.register(Person)
admin.site.register(Keyword)

