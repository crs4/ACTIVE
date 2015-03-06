from django.conf.urls import patterns, url

urlpatterns = patterns('clustermanager.views',
	# start all nodes in the cluster
        url(r'^start/$', 'start', name="start"),
	# stop all nodes in the cluster
        url(r'^stop/$', 'stop',  name="stop"),
	# restart all nodes in the cluster
        url(r'^restart/$', 'restart', name="restart"),
	# get main information about a node of the cluster
        url(r'^get/(?P<node_id>[a-zA-Z0-9\@]+)/$', 'get', name="get"),
	# get the list of nodes id available in the cluster
        url(r'^list/$', 'list', name="list"),
)
