# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL pattern that must be used to handle
information about the installed ACTIVE tools.

ACTIVE Tool data is returned in a JSON format and it is not possible to
write or change any type of information about an existing ACTIVE Tool.

This is the URL path that could be used to handle ACTIVE Tools data:

GET     /api/tools/	   obtain the list of available ACTIVE Tools in JSON
"""

from core.active_tools.views import ActiveToolsList
from django.conf.urls import url


urlpatterns = (
    url(r'^$', ActiveToolsList.as_view()),
)
