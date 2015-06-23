"""
This module contains classes and module necessary to implement the REST API
for the managing of cluster of nodes.
For cluster nodes it is possible to retrieved detailed information while
for cluster it is possible to start, restart, stop all nodes.
"""

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import status

from cluster_manager.cluster.cluster_manager import CeleryManager
import json
import logging

# variable used for logging purposes
logger = logging.getLogger('job_processor')


# global variable used to store cluster nodes information
nodes = None # TODO move as class field

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

        @param request: HttpRequest used to retrieve cluster main information.
        @type request: HttpRequest
        @return: A JSON representation of cluster information.
        @rtype: HttpResponse containing the serialized cluster data.
        """
        logger.debug('Requested cluster node information')
        list = cm.list_nodes()
        global nodes
        if not nodes:
            nodes = list
        else:
            for node in nodes:
                if node['id'] not in map(lambda x: x['id'], list):
                    node['status'] = 'ping'
                    list.append(node)
            nodes = list
        return HttpResponse(json.dumps(list))

    def post(self, request):
        """
        Method used to startup the cluster (its nodes).

        @param request: HttpRequest used to startup cluster nodes.
        @type request: HttpRequest
        @return: HttpResponse embedding the result of cluster startup.
        @rtype: HttpResponse
        """
        logger.debug('starting up all cluster nodes')
        res = cm.start()
        return HttpResponse(json.dumps({'res': res}))

    def put(self, request):
        """
        Method used to restart the cluster (its nodes).

        @param request: HttpRequest used to restart all cluster nodes.
        @type request: HttpRequest
        @return: HttpResponse containing the restart status.
        @rtype: HttpResponse
        """
        logger.debug('Restarting all cluster nodes')
        res = cm.restart()
        return HttpResponse(json.dumps({'res': res}))

    def delete(self, request):
        """
        Method used to stop the cluster (its nodes).

        @param request: HttpRequest used to stop the cluster.
        @type request: HttpRequest
        @return: HttpResponse containing the result of the cluster stop.
        @rtype: HttpResponse
        """
        logger.debug('Shutting down all cluster nodes')
        res = cm.stop()
        return HttpResponse(json.dumps({'res': res}))


class NodeDetail(APIView):
    """
    Class used to generate all views necessary to start, stop, restart
    and retrieve data for each node of a cluster.
    """

    def get(self, request, id):
        """
        Method used to get information about the cluster.

        @param request: HttpRequest used to retrieve cluster node data.
        @type request: HttpRequest
        @param id: The node id used to extract serialized data of a cluster node.
        @type id: int
        @return: HttpResponse containing the serialized cluster data.
        @rtype: HttpResponse
        """
        logger.debug('Requested details for node ' + str(id))
        node = cm.get_node(id)
        if node:
            node['id'] = id
            node = self.__print_dict(node)
            return HttpResponse(json.dumps(node))

        return HttpResponse(json.dumps({'error': 'No node found'}), status=status.HTTP_404_NOT_FOUND)

    def __print_dict(self, d):
        """
        Replace (recursively) minus characters with underscore for
        all dict keys. Needed by AngularJS.

        @param d: Data that must be converted in a dictionary.
        @type d: string
        @return: HttpResponse containing the serialized cluster data.
        @rtype: dictionary
        """
        new = {}
        for k, v in d.iteritems():
            if isinstance(v, dict):
                    v = self.__print_dict(v)
            new[k.replace('-', '_')] = v
        return new
