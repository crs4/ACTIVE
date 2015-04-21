from django.conf.urls import patterns, include, url
from core.items.image.views import ImageItemDetail, ImageItemList

"""
This module defines the URL patterns that must be used in order
to handle Image  objects data.
The provided REST API allows to:
- obtain the list of alla available Image item objects;
- handle the data of a specific Image object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Image objects,
with the provided method and a short description for each one:

GET     /api/items/image/	   obtain the list of available Image in JSON
POST    /api/items/image/	   create a new Image object with provided serialized data

GET     /api/items/image/12/   obtain the data of the Image object with id = 12
PUT     /api/items/image/12/   edit the data of the Image object with id = 12
DELETE  /api/items/image/12/   delete all data related to the Image object with id = 12 
"""

urlpatterns = (
    url(r'^$', ImageItemList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ImageItemDetail.as_view()),
)

