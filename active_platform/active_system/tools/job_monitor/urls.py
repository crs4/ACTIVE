# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines all URL patterns necessary to interact with the
API REST developed for the Job Monitor. 
It is possibile to retrive all data associated to jobs or cluster nodes.
"""

from django.conf.urls import patterns, include, url
from tools.job_monitor.views import JobsList, JobsDelete, JobGetDetails, JobStopDetails, JobGetResult


urlpatterns = patterns('tools.job_monitor.views',
        url(r'^$', 'index', name="index"),
	url(r'^list/$', JobsList.as_view()),
        url(r'^get/(?P<pk>[A-Za-z0-9\-]+)/$', JobGetDetails.as_view()),
        url(r'^stop/(?P<pk>[A-Za-z0-9\-]+)/$', JobStopDetails.as_view()),
	url(r'^clean/$', JobsDelete.as_view()),
	url(r'^result/$', JobGetResult.as_view()),
	
        url(r'^cluster/list/$', 'list_nodes', name="list_nodes"),
        url(r'^cluster/start/$', 'start_cluster', name="start_cluster"),
	url(r'^cluster/stop/$', 'stop_cluster', name="stop_cluster"),
	url(r'^cluster/restart/$', 'restart_cluster', name="restart_cluster"),
        url(r'^cluster/node/(?P<id>[a-zA-Z0-9\@\-]+)/$', 'get_node', name="get_node"),
)

