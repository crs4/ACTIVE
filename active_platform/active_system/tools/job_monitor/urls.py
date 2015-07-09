"""
This module defines all URL patterns necessary to interact with the
API REST developed for the Job Monitor. 
It is possibile to retrive all data associated to jobs or cluster nodes.
"""

from django.conf.urls import patterns, include, url


urlpatterns = patterns('tools.job_monitor.views',
        url(r'^$', 'index', name="index"),
        url(r'^list/$', 'list_jobs', name="list_jobs"),
        url(r'^get/(?P<job_id>[A-Za-z0-9\-]+)/$', 'get_job', name="get_job"),
        url(r'^stop/(?P<job_id>[A-Za-z0-9\-]+)/$', 'stop_job',  name="stop_job"),
	url(r'^clean/$', 'clean_jobs', name="clean_jobs"),
	url(r'^result/$', 'get_job_result', name="get_job_result"),

	
        url(r'^cluster/list/$', 'list_nodes', name="list_nodes"),
        url(r'^cluster/start/$', 'start_cluster', name="start_cluster"),
	url(r'^cluster/stop/$', 'stop_cluster', name="stop_cluster"),
	url(r'^cluster/restart/$', 'restart_cluster', name="restart_cluster"),
        url(r'^cluster/node/(?P<id>[a-zA-Z0-9\@\-]+)/$', 'get_node', name="get_node"),
)

