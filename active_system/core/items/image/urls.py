"""
This module defines the URL patterns that must be used in order
to handle ImageItem objects data.
The provided REST API allows to:
    - obtain the list of alla available ImageItem objects;
    - handle the data of a specific ImageItem object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle ImageItem objects,
with the provided method and a short description for each one:

GET     /api/items/image/	   obtain the list of available ImageItem objects in JSON.

POST    /api/items/image/	   create a new ImageItem object with provided serialized data.


GET     /api/items/image/12/   obtain the data of the ImageItem object with id = 12.

PUT     /api/items/image/12/   edit the data of the ImageItem object with id = 12.

DELETE  /api/items/image/12/   delete all data of ImageItem object with id = 12.
"""

from django.conf.urls import url
from core.items.image.views import ImageItemDetail, ImageItemList


urlpatterns = (
    url(r'^$', ImageItemList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ImageItemDetail.as_view()),
)

