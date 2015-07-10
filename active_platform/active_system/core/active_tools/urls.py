"""
This module defines the URL pattern that must be used to handle
information about the installed ACTIVE tools.

ACTIVE Tool data is returned in a JSON format and it is not possible to
write or change any type of information about an existing ACTIVE Tool.

This is the URL path that could be used to handle ACTIVE Tools data:

GET     /api/tools/	   obtain the list of available ACTIVE Tools in JSON

"""

from django.conf.urls import url
from core.active_tools.views import ActiveToolsList


urlpatterns = (
    url(r'^$', ActiveToolsList.as_view()),
)