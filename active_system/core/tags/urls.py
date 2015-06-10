"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (person, tags, dynamic tags and keywords).
From this module it is possible to access directly to generic Tags views (and HTTP methods).
Tags objects are returned in a JSON serialized format.

For each module it will be possible to obtain more information about
the available REST API inside the respective urls.py module.

GET     /api/tags/          obtain all stored Tags objects

POST    /api/tags/          create a new Tag object with the provided data


GET     /api/tags/12/       obtain stored data for Tag object with id = 12

PUT     /api/tags/12/       edit stored data for Tag object with id = 12

DELETE  /api/tags/12/       delete stored data for Tag object with id = 12


GET     /api/tags/search/item/12/  obtain Tag objects associated to item with id = 12

GET     /api/tags/search/person/12/  obtain Tag objects associated to person with id = 12
"""

from django.conf.urls import include, url
from core.tags.views import TagList, TagDetail
from core.tags.views import SearchTagItem, SearchTagPerson

import core.tags.person.urls
import core.tags.dynamic_tags.urls
import core.tags.keywords.urls


urlpatterns = (
    url(r'^tags/$', TagList.as_view()),
    url(r'^tags/(?P<pk>[0-9]+)/$', TagDetail.as_view()),
    url(r'^tags/search/item/(?P<pk>[0-9]+)/$', SearchTagItem.as_view()),
    url(r'^tags/search/person/(?P<pk>[0-9]+)/$', SearchTagPerson.as_view()),
    url(r'^people/', include(core.tags.person.urls)),
    url(r'^dtags/', include(core.tags.dynamic_tags.urls)),
    url(r'^keywords/', include(core.tags.keywords.urls)),
)
