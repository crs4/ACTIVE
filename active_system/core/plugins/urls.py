from django.conf.urls import patterns, include, url
#from rest_framework.urlpatterns import format_suffix_patterns

from core.plugins.views import EventTrigger, EventExec

import core.plugins.event.urls
import core.plugins.plugin.urls
import core.plugins.action.urls
import core.plugins.script.urls 


"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (plugin, script, event, action).
Moreover it is possible to trigger events and scripts by id.
"""

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


urlpatterns = [
    url(r'^triggers/event/(?P<event_id>[0-9]+)/$', EventTrigger.as_view()),
    url(r'^triggers/script/(?P<script_id>[0-9]+)/$', EventExec.as_view()),
    url(r'plugins/', include(core.plugins.plugin.urls)),
    url(r'events/', include(core.plugins.event.urls)),
    url(r'scripts/', include(core.plugins.script.urls)),
    url(r'actions/', include(core.plugins.action.urls)),
]


#urlpatterns = format_suffix_patterns(urlpatterns)
