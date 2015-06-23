"""
This module defines the URL patterns that must be used in order to handle Person objects data.
The provided REST API allows to:
    - obtain the list of alla available Person objects;
    - handle the data of a specific Person object through CRUD operations;
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Person objects,
with the provided method and a short description for each one:

GET     /api/people/	   obtain the list of available Person objects in JSON

POST    /api/people/	   create a new Person object with provided serialized data


GET     /api/people/12/   obtain the data of the Person object with id = 12

PUT     /api/people/12/   edit the data of the Person object with id = 12

DELETE  /api/people/12/   delete all data related to the Person object with id = 12
"""

from django.conf.urls import url
from core.tags.person.views import PersonDetail, PersonList, PersonImage, PersonSearch


urlpatterns = (
    url(r'^$', PersonList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', PersonDetail.as_view()),
    url(r'^file/(?P<pk>[0-9]+)/$', PersonImage.as_view()),
    url(r'^search/(?P<first_name>[\w]+)/(?P<last_name>[\w]+)/$', PersonSearch.as_view()),
)

