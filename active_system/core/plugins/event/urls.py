"""
This module defines the URL patterns that must be used in order to handle Event objects data.
The provided REST API allows to:
    - obtain the list of alla available Event objects;
    - handle the data of a specific Event object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Event objects,
with the provided method and a short description for each one:

GET     /api/events/      obtain the list of available Events in JSON.

POST    /api/events/      create a new Event object with provided serialized data.


GET     /api/events/12/   obtain the data of the Event object with id = 12.

PUT     /api/events/12/   edit the data of the Event object with id = 12.

DELETE  /api/events/12/   delete all data related to the Event object with id = 12.
"""

from django.conf.urls import url
from core.plugins.event.views import EventDetail, EventList


urlpatterns = [
    url(r'^$', EventList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', EventDetail.as_view()),
]

