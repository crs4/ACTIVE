from django.conf.urls import patterns, include, url


from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tools.job_monitor.views import JobDetail, JobList, ClusterList, NodeDetail, index


urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^jobs/$',   JobList.as_view()),
    url(r'^jobs/(?P<pk>[A-Za-z0-9\-]+)/$',   JobDetail.as_view()),
    url(r'^cluster/$',   ClusterList.as_view()),
    url(r'^cluster/node/(?P<pk>[a-zA-Z0-9\@\-]+)/$', NodeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

"""
urlpatterns = patterns('jobmonitor.views',
	url(r'^$', 'index', name="index"),
	# start a job asynchronously based on its (full) name
        url(r'^start/$', 'start_job', name="start_job"),
	# stop job execution by its ID
        url(r'^stop/(?P<job_id>[A-Za-z0-9\-]+)/$', 'stop_job',  name="stop_job"),
	# clean all information about completed or failed jobs
	url(r'^clean/$', 'clean_jobs', name="clean_jobs"),
	# get main job information
        url(r'^get/(?P<job_id>[A-Za-z0-9\-]+)/$', 'get_job', name="get_job"),
	# get the job result if it is available
	url(r'^result/$', 'get_job_result', name="get_job_result"),
	# get the info of jobs handled by the job monitor
        url(r'^list/$', 'list_jobs', name="list_jobs"),
)


urlpatterns = patterns('tools.job_monitor.views',
    url(r'^$', 'index', name="index"),
    # get the info of jobs handled by the job monitor
    url(r'^list/$', 'list_jobs', name="list_jobs"),
    # get main job information
    url(r'^get/(?P<job_id>[A-Za-z0-9\-]+)/$', 'get_job', name="get_job"),
    # stop job execution by its ID
    url(r'^stop/(?P<job_id>[A-Za-z0-9\-]+)/$', 'stop_job',  name="stop_job"),
    # clean all information about completed or failed jobs
    url(r'^clean/$', 'clean_jobs', name="clean_jobs"),
    # get the job result if it is available
    url(r'^result/$', 'get_job_result', name="get_job_result"),


    url(r'^cluster/list/$', 'list_nodes', name="list_nodes"),
    url(r'^cluster/start/$', 'start_cluster', name="start_cluster"),
    url(r'^cluster/stop/$', 'stop_cluster', name="stop_cluster"),
    url(r'^cluster/restart/$', 'restart_cluster', name="restart_cluster"),
    url(r'^cluster/node/(?P<id>[a-zA-Z0-9\@\-]+)/$', 'get_node', name="get_node"),
)

"""
