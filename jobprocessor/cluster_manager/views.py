from django.shortcuts import render
from cluster_manager import CeleryManager
import json

"""
These views are used to provide a simple REST API
that could be used by an HTTP client to get informations
about the state of each job.
Most of these views are simple wrappers for the main 
functionalities provided by the cluster manager module.
"""

# associare una qualche forma di login degli utenti?

# one and shared cluster manager for Celery nodes
cm = CeleryManager


def start(request):
	"""
	This view is used to start all available cluster nodes.
	"""
	res = cm.start()
	return HttpResponse(json.dumps({'res' : res})

def stop(request):
	"""
	this view is used to stop all cluster nodes.
	"""
	res = cm.stop()
	return HttpResponse(json.dumps({'res': res})

def restart(request):
	"""
	This view is used to restart all available cluster nodes.
	It is useful for code update.
	"""
	res = cm.restart()
	return HttpResponse(json.dumps({'res' : res})

def purge(request):
	"""
	This view is useful to remove all activities
	that are currently executed on cluster nodes.
	"""
	res = cm.purge()
	return HttpResponse(json.dumps({'res' : res})

def list(request):
	"""
	This view is used to obtain a list of all available
	cluster nodes. For each node only its id is returned.
	"""
	list = cm.list_nodes()
	return HttpResponse(json.dumps({'nodes' : list})

def get(request, id):
	"""
	This view is used to obtain detailed informations
	about a specific cluster node, providing its id.
	"""
	node = cm.get(id)
	return HttpResponse(json.dumps({'node' : node})

