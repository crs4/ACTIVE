from django.conf.urls import patterns, include, url
from core.plugins.event.views import EventDetail, EventList



urlpatterns = [
    url(r'^events/$', EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', EventDetail.as_view()),
]

