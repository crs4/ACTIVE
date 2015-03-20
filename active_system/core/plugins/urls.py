from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns
from core.plugins.views import EventDetail, EventList


urlpatterns = [
    url(r'^events/$', EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', EventDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


