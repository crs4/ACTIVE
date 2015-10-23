# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL patterns that must be used in order to handle DynamicTag objects data.
The provided REST API allows to:
    - obtain the list of alla available DynamicTag objects;
    - handle the data of a specific DynamicTag object through CRUD operations;
    - retrieve all items based on item type and dtag associated to them.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle DynamicTag objects,
with the provided method and a short description for each one:

GET     /api/dtags/	   obtain the list of available DynamicTag objects in JSON

POST    /api/dtags/	   create a new DynamicTag object with provided serialized data


GET     /api/dtags/12/   obtain the data of the DynamicTag object with id = 12

PUT     /api/dtags/12/   edit the data of the DynamicTag object with id = 12

DELETE  /api/dtags/12/   delete all data related to the DynamicTag object with id = 12

"""

from core.tags.dynamic_tags.views import DynamicTagDetail, DynamicTagList
from core.tags.dynamic_tags.views import MergeUniformDynamicTag
from django.conf.urls import url


urlpatterns = (
    url(r'^$', DynamicTagList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DynamicTagDetail.as_view()),   
    url(r'^merge/(?P<pk>[0-9]+)/$', MergeUniformDynamicTag.as_view()),
)

