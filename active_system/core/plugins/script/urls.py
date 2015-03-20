from django.conf.urls import patterns, include, url

#from rest_framework.urlpatterns import format_suffix_patterns
from core.plugins.script.views import ScriptDetail, ScriptList


urlpatterns = [
    url(r'^scripts/$', ScriptList.as_view()),
    url(r'^scripts/(?P<pk>[0-9]+)/$', ScriptDetail.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)


