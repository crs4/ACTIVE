from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.items.routers import routerDetail
from core.items.routers import routerList

# items are redirect to a properly handler

urlpatterns = [
    url(r'^items/$', routerList),
    url(r'^items/(?P<pk>[0-9]+)/$', routerDetail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
