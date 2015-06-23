"""
This module defines the URL patterns that must be used in order
to handle VideoItem objects data.
The provided REST API allows to:
    - obtain the list of alla available VideoItem objects;
    - handle the data of a specific Video object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Video objects,
with the provided method and a short description for each one:

GET     /api/items/video/	   obtain the list of available VideoItem objects in JSON

POST    /api/items/video/	   create a new VideoItem object with provided serialized data


GET     /api/items/video/12/   obtain the data of the VideoItem object with id = 12

PUT     /api/items/video/12/   edit the data of the VideoItem object with id = 12

DELETE  /api/items/video/12/   delete all data of VideoItem object with id = 12
"""

from django.conf.urls import url
from core.items.video.views import VideoItemDetail, VideoItemList


urlpatterns = (
    url(r'^$', VideoItemList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', VideoItemDetail.as_view()),
)
