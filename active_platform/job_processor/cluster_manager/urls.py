# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines all URL patterns used to define the REST API
for the cluster manager module.

These are the relative paths that could be used to handle the cluster of distributed nodes,
using the provided REST API.
A short description for each URL pattern is defined:

GET	/api/cluster/		retrieve information about the entire cluster

POST	/api/cluster/		startup the cluster (all its nodes)

PUT	/api/cluster/		restart the cluster (all its nodes)

DELETE	/api/cluster/		stop the cluster (all its nodes)


GET     /api/node/aBc12/	retrieve the aBc12 cluster node information

"""

from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from cluster_manager.views import ClusterDetail, NodeDetail

urlpatterns = [
    url(r'^node/(?P<id>[a-zA-Z0-9\@]+)/$', NodeDetail.as_view()),
    url(r'^cluster/$', ClusterDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
