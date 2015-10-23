# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL patterns that must be used in order
to handle Audio  objects data.
The provided REST API allows to:
    - obtain the list of alla available Audio item objects;
    - handle the data of a specific Audio object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Audio objects,
with the provided method and a short description for each one:

GET     /api/items/audio/	   obtain the list of available Audio in JSON.

POST    /api/items/audio/	   create a new Audio object with provided serialized data.


GET     /api/items/audio/12/   obtain the data of the Audio object with id = 12.

PUT     /api/items/audio/12/   edit the data of the Audio object with id = 12.

DELETE  /api/items/audio/12/   delete all data related to the Audio object with id = 12.
"""


from django.conf.urls import url
from core.items.audio.views import AudioItemDetail, AudioItemList

urlpatterns = (
    url(r'^$', AudioItemList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', AudioItemDetail.as_view())
)
