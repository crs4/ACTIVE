"""
This module defines the URL patterns that must be used in order
to handle Action  objects data.
The provided REST API allows to:
    - obtain the list of alla available Action objects;
    - handle the data of a specific Action object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Action objects,
with the provided method and a short description for each one:

GET     /api/actions/	   obtain the list of available Actions in JSON.

POST    /api/actions/	   create a new Action object with provided serialized data.


GET     /api/actions/12/   obtain the data of the Action object with id = 12.

PUT     /api/actions/12/   edit the data of the Action object with id = 12.

DELETE  /api/actions/12/   delete all data related to the Action object with id = 12.
"""

from django.conf.urls import url
from core.plugins.action.views import ActionDetail, ActionList

urlpatterns = [
    url(r'^$', ActionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ActionDetail.as_view()),
]