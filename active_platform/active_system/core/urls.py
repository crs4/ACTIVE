# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module includes all URL patterns which define the REST API of the platform core.
"""

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
import core.items.urls
import core.plugins.urls
import core.tags.urls
import core.users.urls
import core.active_tools.urls


urlpatterns = [
    url(r'^items/', include(core.items.urls)),
    url(r'', include(core.plugins.urls)),
    url(r'', include(core.tags.urls)),
    url(r'users/', include(core.users.urls)),
    url(r'tools/', include(core.active_tools.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
