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


GET     /api/keywords/search/image/landscape          retrieve all images with keyword 'landscape'

GET     /api/keywords/search/video/landscape,lake     retrieve all videos objects with both keywords
                                                        'landscape' and 'lake' associated
"""

from django.conf.urls import url
from core.tags.keywords.views import KeywordDetail, KeywordList, KeywordSearch


urlpatterns = (
    url(r'^$', KeywordList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', KeywordDetail.as_view()),
    url(r'^search/(?P<item_type>[0-9A-Za-z]+)/(?P<keyword_list>[\w,]+)/$', KeywordSearch.as_view()),
)