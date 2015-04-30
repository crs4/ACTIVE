"""
This module defines the URL patterns that must be used in order to handle Script objects data.
The provided REST API allows to:
- obtain the list of alla available Script objects;
- handle the data of a specific Script object through CRUD operations.
All provided data is returned in a JSON format.

These are the relative paths that could be used to handle Script objects,
with the provided method and a short description for each one:

    - GET     /api/scripts/      obtain the list of available Script in JSON
    - GET     /api/scripts/12/    obtain the data of the Script object with id = 12

NB: it isn't possible to create, edit or delete script data through the API REST
due to the fact that all information are extracted from plugin manifest files.
So if any change is required it must be applied to the proper manifest file.
"""

from django.conf.urls import url
from core.plugins.script.views import ScriptDetail, ScriptList


urlpatterns = [
    url(r'^$', ScriptList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ScriptDetail.as_view()),	
]
