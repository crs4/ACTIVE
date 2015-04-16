from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.plugins.views import EventTrigger, EventExec

from core.plugins.plugin.urls import urlpatterns as plugin_patterns
from core.plugins.event.urls  import urlpatterns as event_patterns
from core.plugins.script.urls import urlpatterns as script_patterns
from core.plugins.action.urls import urlpatterns as action_patterns


"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (plugin, script, event, action).
Moreover it is possible to trigger events and scripts by id.
"""

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


trigger_pattern = [
    url(r'^triggers/event/(?P<event_id>[0-9]+)/$', EventTrigger.as_view()),
    url(r'^triggers/script/(?P<script_id>[0-9]+)/$', EventExec.as_view()),
    #url(r'', include(core.plugins.plugin.urls)),
    #url(r'', include(core.plugins.event.urls)),
    #url(r'', include(core.plugins.script.urls)),
    #url(r'', include(core.plugins.action.urls)),
]

urlpatterns = plugin_patterns + event_patterns + script_patterns + action_patterns + trigger_pattern
urlpatterns = format_suffix_patterns(urlpatterns)


