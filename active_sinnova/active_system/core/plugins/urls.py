"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (plugin, script, event, action).

Some of the following API REST urls are used to trigger events and scripts by id:

POST    /api/triggers/event/12/        start the Event with id = 12

POST    /api/triggers/script/12/       start the Script with id = 12

For each module it will be possible to obtain more information about
the available REST API inside the respective urls.py module.
"""

from django.conf.urls import include, url
from core.plugins.views import EventTrigger, EventExec

import core.plugins.event.urls
import core.plugins.plugin.urls
import core.plugins.action.urls
import core.plugins.script.urls 


urlpatterns = [
    url(r'^triggers/event/(?P<event_id>[0-9]+)/$',   EventTrigger.as_view()),
    url(r'^triggers/script/(?P<script_id>[0-9]+)/$', EventExec.as_view()),
    url(r'plugins/', include(core.plugins.plugin.urls)),
    url(r'events/',  include(core.plugins.event.urls)),
    url(r'scripts/', include(core.plugins.script.urls)),
    url(r'actions/', include(core.plugins.action.urls)),
]
