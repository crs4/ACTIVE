from django.conf.urls import patterns, include, url

urlpatterns = patterns('jobmanager.views',
	# start a job asynchronously based on its (full) name
        url(r'^start/$', 'start_job', name="start_job"),
	# stop job execution by its ID
        url(r'^stop/$', 'stop_job',  name="stop_job"),
	# clean all information about completed or failed jobs
	url(r'^clean/$', 'clean_jobs', name="clean_jobs"),
	# get main job information
        url(r'^get/$', 'get_job', name="get_job"),
	# get the job result if it is available
	url(r'^result/$', 'get_job_result', name="get_job_result"),
	# get the info of jobs handled by the job monitor
        url(r'^list/$', 'list_jobs', name="list_jobs"),
)
