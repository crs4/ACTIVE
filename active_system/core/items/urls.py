from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.items.routers import routerDetail, routerList, routerRendition

# items are redirect to a properly handler
urlpatterns = [
    url(r'^items/(?P<pk>[0-9]+)/$', routerDetail),
    url(r'^items/files/(?P<pk>[0-9]+)/$', routerRendition),
    url(r'^items/$', routerList),


]

urlpatterns = format_suffix_patterns(urlpatterns)
