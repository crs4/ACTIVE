from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.plugins.plugin.urls import urlpatterns as plugin_patterns
from core.plugins.event.urls  import urlpatterns as event_patterns
from core.plugins.script.urls import urlpatterns as script_patterns
from core.plugins.action.urls import urlpatterns as action_patterns


urlpatterns = plugin_patterns + event_patterns + script_patterns + action_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
