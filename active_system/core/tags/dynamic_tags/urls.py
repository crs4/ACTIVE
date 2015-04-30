"""
This module defines the URL patterns that must be used in order to handle DynamicTag objects data.
The provided REST API allows to:
- obtain the list of alla available DynamicTag objects;
- handle the data of a specific DynamicTag object through CRUD operations;
- retrieve all items based on item type and dtag associated to them.

All provided data is returned in a JSON format.

These are the relative paths that could be used to handle DynamicTag objects,
with the provided method and a short description for each one:

    - GET     /api/dtags/	   obtain the list of available DynamicTag objects in JSON
    - POST    /api/dtags/	   create a new DynamicTag object with provided serialized data

    - GET     /api/dtags/12/   obtain the data of the DynamicTag object with id = 12
    - PUT     /api/dtags/12/   edit the data of the DynamicTag object with id = 12
    - DELETE  /api/dtags/12/   delete all data related to the DynamicTag object with id = 12

    - GET     /api/dtags/search/item/12/      obtain all dynamic tags associated to item with id = 12
    - GET     /api/dtags/search/person/12/    obtain all dynamic tags associated to person with id = 12
"""

from django.conf.urls import url
from core.tags.dynamic_tags.views import DynamicTagDetail, DynamicTagList
from core.tags.dynamic_tags.views import SearchDynamicTagItem, SearchDynamicTagPerson


urlpatterns = (
    url(r'^$', DynamicTagList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DynamicTagDetail.as_view()),   
    url(r'^search/item/(?P<pk>[0-9]+)/$', SearchDynamicTagItem.as_view()),
    url(r'^search/person/(?P<pk>[0-9]+)/$', SearchDynamicTagPerson.as_view()),
)

