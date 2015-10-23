# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL patterns that must be used in order to handle Plugin objects data.
The provided REST API allows to:
    - obtain the list of alla available Plugin objects;
    - handle the data of a specific Plugin object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Plugin objects,
with the provided method and a short description for each one:

GET     /api/plugins/      obtain the list of available Events in JSON.

GET     /api/plugins/12/    obtain the data of the Plugin object with id = 12.

NB: it isn't possible to create, edit or delete plugin data through the API REST
due to the fact that all information are extracted from manifest files.
So if any change is required it must be applied to the manifest file.
"""

from django.conf.urls import url
from core.plugins.plugin.views import PluginDetail, PluginList


urlpatterns = [
    url(r'^$', PluginList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', PluginDetail.as_view()),
]


