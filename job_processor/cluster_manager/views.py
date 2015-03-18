from django.shortcuts import render
from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cluster_manager.cluster.cluster_manager import CeleryManager
import json


"""
This module contains two class used to provide the cluster manager API.
There are two levels of information: cluster level and node level.
"""

# global variable used to store cluster nodes information
nodes = None

# global variable used to handle the cluster
cm = CeleryManager()


class ClusterDetail(APIView):
    """
    Class used to generate all views necessary to start, stop, restart
    and retrieve data about the cluster.
    """

    def get(self, request):
	"""
	Method used to get information about the cluster.
	:param request: HTTP input request.
	:returns: A JSON representation of needed information is returned.
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

    def post(self, request):
        """
        Method used to get information about the cluster.
	:param request: HTTP input request.
        :returns: A JSON representation of needed information is returned.
        """
	print "Cluster startup..."
        res = cm.start()
        return HttpResponse(json.dumps({"res" : res}))


    def put(self, request):
        """
        Method used to update user information providing
        serialized data.
       	:param request: HTTP input request.
        :returns:
        """
	print "Cluster restart..."
	res = cm.restart()
        return HttpResponse(json.dumps({"res" : res}))

    def delete(self, request):
        """
        Method used to delete user information providing his ID.
        :param request: HTTP input request.
        :returns: User data deletion status.
        """
	print "Cluster shutdown"
	res = cm.stop()
        return HttpResponse(json.dumps({"res": res}))


class NodeDetail(APIView):
    """
    Class used to generate all views necessary to start, stop, restart
    and retrieve data for each node of a cluster.
    """

    def get(self, request, id):
        """
        Method used to get information about the cluster.
        :param request: HTTP input request.
	:param id: The node id used to extract its data.
        :returns: A JSON representation of retrieved node data.
        """
	print 'Node details ', id
        node = cm.get_node(id)
	if node:
        	node['id'] = id
	        node = self.__print_dict(node)
        	return HttpResponse(json.dumps(node))

	return HttpResponse(json.dumps({'error' : 'No node found'}))

    def __print_dict(d):
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
