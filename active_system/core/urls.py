"""
This module includes all URL patterns which define the REST API of the platform core.
"""

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

import core.items.urls
import core.plugins.urls
import core.tags.urls
import core.users.urls


urlpatterns = [
    url(r'^items/', include(core.items.urls)),
    url(r'', include(core.plugins.urls)),
    url(r'', include(core.tags.urls)),
    url(r'users/', include(core.users.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
