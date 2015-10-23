# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL patterns that must be used in order
to handle generic Item objects data.
The provided REST API allows to:
    - obtain the list of all available Item objects;
    - handle the data of a specific Item object through CRUD operations;
    - access to specific digital item data through a dedicated API;
    - obtain the resource corresponding to the digital item.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle generic Item objects,
for the API REST on each specific digital item see the respective urls.py file.
with the provided method and a short description for each one:

GET     /api/items/    obtain the list of available Items in JSON.

POST    /api/items/	   create a new Item object with provided serialized data.


GET     /api/items/12/   obtain the data of the Item object with id = 12.

PUT     /api/items/12/   edit the data of the Item object with id = 12.

DELETE  /api/items/12/   delete all data related to the Item object with id = 12.


GET     /api/items/file/12                  obtain the preview resource associated to Item with id = 12.

GET     /api/items/file/12?type=preview     obtain the preview resource associated to Item with id = 12.

GET     /api/items/file/12?type=original    obtain the original resource associated to Item with id = 12.

GET     /api/items/file/12?type=thumb       obtain the thumbnail resource associated to Item with id = 12.
"""

from django.conf.urls import include, url
from core.items.views import ItemList, ItemDetail, ItemFile

import core.items.video.urls
import core.items.image.urls
import core.items.audio.urls


# items are redirect to a properly handler
urlpatterns = [
    url(r'^$', ItemList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ItemDetail.as_view()),
    url(r'^file/(?P<pk>[0-9]+)/$', ItemFile.as_view()),
    url(r'^video/', include(core.items.video.urls)),
    url(r'^image/', include(core.items.image.urls)),
    url(r'^audio/', include(core.items.audio.urls))]


