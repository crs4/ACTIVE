"""
This module defines all URL patterns defined for the provided REST API.
Two main endpoints has been defined, one for cluster managing and the other
for retrieving node details.

In order to use the function provided by the cluster module the following
URL must e used with the specified HTTP method and parameters:

GET     /api/node/NODE1     retrieve details for the cluster node with id = NODE1


GET     /api/cluster        retrieve data about available cluster nodes

POST    /api/cluster        start all cluster nodes

PUT     /api/cluster        restart all cluster nodes

DELETE  /api/cluster        stop all cluster nodes
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from cluster_manager.views import ClusterDetail, NodeDetail

urlpatterns = [
    url(r'^node/(?P<id>[a-zA-Z0-9\@]+)/$', NodeDetail.as_view()),
    url(r'^cluster/$', ClusterDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
