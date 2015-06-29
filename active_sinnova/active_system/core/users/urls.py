"""
This module defines the URL patterns that must be used in order to handle User objects data.
The provided REST API allows to:
    - obtain the list of alla available User objects;
    - handle the data of a specific User object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle User objects,
with the provided method and a short description for each one:

GET     /api/users/	   obtain the list of available User in JSON

POST    /api/users/	   create a new Person object with provided serialized data


GET     /api/users/12/   obtain the data of the User object with id = 12

PUT     /api/users/12/   edit the data of the User object with id = 12

DELETE  /api/users/12/   delete all data related to the User object with id = 12
"""

from django.conf.urls import url
from core.users.views import ActiveUserList, ActiveUserDetail


urlpatterns = [
    url(r'^$', ActiveUserList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ActiveUserDetail.as_view()),
]
