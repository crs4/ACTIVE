from django.conf.urls import patterns, include, url
from core.plugins.plugin.views import PluginDetail, PluginList

urlpatterns = [
    url(r'^plugins/$', PluginList.as_view()),
    url(r'^plugins/(?P<pk>[0-9]+)/$', PluginDetail.as_view()),
]


