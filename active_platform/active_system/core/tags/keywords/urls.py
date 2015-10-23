# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the URL patterns that must be used in order to handle Keyword objects data.
The provided REST API allows to:
    - obtain the list of alla available Keyword objects;
    - handle the data of a specific Keyword object through CRUD operations;
    - retrieve all items based on item type and keyword associated to them.

All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Keyword objects,
with the provided method and a short description for each one:

GET     /api/keywords/	   obtain the list of available Keyword objects in JSON

POST    /api/keywords/	   create a new Keyword object with provided serialized data


GET     /api/keywords/12/   obtain the data of the Keyword object with id = 12

PUT     /api/keywords/12/   edit the data of the Keyword object with id = 12

DELETE  /api/keywords/12/   delete all data related to the Keyword object with id = 12


GET     /api/keywords/item/12          retrieve all the keywords associated with item with id = 12
"""

from django.conf.urls import url
from core.tags.keywords.views import KeywordDetail, KeywordList, KeywordsItem


urlpatterns = (
    url(r'^$', KeywordList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', KeywordDetail.as_view()),
    url(r'^item/(?P<pk>[0-9]+)/$', KeywordsItem.as_view()),
)
