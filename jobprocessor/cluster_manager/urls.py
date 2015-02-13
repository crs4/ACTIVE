from django.conf.urls import patterns, include, url

urlpatterns = patterns('cluster_manager.views',
	# start all nodes in the cluster
        url(r'^start/$', 'start', name="start"),
	# stop all nodes in the cluster
        url(r'^stop/$', 'stop',  name="stop"),
	# restart all nodes in the cluster
        url(r'^restart/$', 'restart', name="restart"),
	# remove all activities from each node of the cluster
	url(r'^purge/$', 'purge', name="purge"),
	# get main information about a node of the cluster
        url(r'^get/$', 'get', name="get"),
	# get the list of nodes id available in the cluster
        url(r'^list/$', 'list', name="list"),
)
