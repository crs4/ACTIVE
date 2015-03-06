from django.http import HttpResponse
from clustermanager.cluster_manager import CeleryManager
import json

"""
These views are used to provide a simple REST API
that could be used by an HTTP client to get informations
about the state of each job.
Most of these views are simple wrappers for the main 
functionalities provided by the cluster manager module.
"""

# associare una qualche forma di login degli utenti?
# global variable used to store cluster nodes information
nodes = None
# global variable used to handle the cluster
cm = CeleryManager()

def start(request):
	"""
	This view is used to start all available cluster nodes.
	"""
	res = cm.start()
	return HttpResponse(json.dumps({"res" : res}))

def stop(request):
	"""
	this view is used to stop all cluster nodes.
	"""
	res = cm.stop()
	return HttpResponse(json.dumps({"res": res}))

def restart(request):
	"""
	This view is used to restart all available cluster nodes.
	It is useful for code update.
	"""
	res = cm.restart()
	return HttpResponse(json.dumps({"res" : res}))

def list(request):
	"""
	This view is used to obtain a list of all available
	cluster nodes. For each node only its id is returned.
	"""
	list = cm.list_nodes()
	global nodes
	if(not nodes):
		nodes = list
	else: 
		for node in nodes:
			if(node['id'] not in map(lambda x: x['id'], list)):
				node['status'] = 'ping'
				list.append(node) 
		nodes = list
	return HttpResponse(json.dumps(list))

def get(request, node_id):
	"""
	This view is used to obtain detailed informations
	about a specific cluster node, providing its id.
	"""
	node = cm.get_node(node_id)
	node['id'] = node_id

	node = print_dict(node)
	return HttpResponse(json.dumps(node))

def print_dict(d):
	"""
	Replace (recursively) minus characters with underscore for 
	all dict keys. Needed by AngularJS.
	"""
	new = {}
	for k, v in d.iteritems():
		if isinstance(v, dict):
			v = print_dict(v)
		new[k.replace('-', '_')] = v
	return new

