from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from cluster_manager.views import ClusterDetail, NodeDetail

urlpatterns = [
    url(r'^node/(?P<id>[a-zA-Z0-9\@]+)/$', NodeDetail.as_view()),
    url(r'^cluster/$', ClusterDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
