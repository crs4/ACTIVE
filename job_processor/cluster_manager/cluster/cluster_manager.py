"""
This module is used to define all methods necessary to handle the
distributed nodes in the cluster.
A generic ClusterManager is provided in order to establish a finite
number of methods and interfaces for node managing.
Then a specific Manager has been defined to handle a cluster of
Celery nodes.
"""

from abc import ABCMeta, abstractmethod
from job_processor.celery import app
import logging

# variable used for logging purposes
logger = logging.getLogger('job_processor')


class ClusterManager:
    """
    This class has beed defined in order to provide an abstraction
    from the technology used for the distributed computation.
    So it exposes the main features provided by a generic cluster.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """
        This method is used to start the cluster (its nodes).
        So for each node in the cluster it should be able to start
        the client application.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Method used to stop the execution of the entire cluster.
        It should be able to stop the execution of the client
        application in every node of the cluster.
        """
        pass

    @abstractmethod
    def restart(self):
        """
        Method used to restart the cluster. It should restart the
        client application installed in every node of the cluster.
        """
        pass

    @abstractmethod
    def list_nodes(self):
        """
        Method used to list the names (IDs) of all cluster nodes.
        """
        pass

    @abstractmethod
    def get_node(self, id):
        """
        Method used to obtain some information about a specific node of the cluster.
        It is necessary to provide the name (ID) of the cluster node.

        @param id: The name used to identify a specific node of the cluster.
        @type id: string
        @return: A dictionary with all informations associated to the specified node. None in case of error.
        @rtype: dictionary
        """
        pass


class CeleryManager(ClusterManager):
    """
    These class inherits and implements all abstract methods
    defined by the base class. It allows handling a cluster of
    Celery nodes. So Celery framework and its primitives will be used
    to simplify methods definition.
    """

    def start(self):
        # unfortunately there is no way to start
        # celery nodes programmatically but they must be
        # started by command line or in deamon mode on each node
        logger.error('Error during cluster startup')
        return False

    def stop(self):
        try:
            logger.debug('Starting cluster nodes')
            app.control.broadcast("shutdown")
        except Exception as e:
            logger.error('Error during cluster shutdown')
            return False

        logger.debug('Cluster shutdown successfully')
        return True

    def restart(self):
        try:
            logger.debug('Restarting cluster nodes')
            app.control.broadcast("pool_restart", arguments = {'reload': True})
        except Exception as e:
            logger.error('Error during cluster restart')
            return False

        logger.debug('Cluster restarted successfully')
        return True

    def list_nodes(self):
        try:
            logger.debug('Detecting available cluster nodes')
            stats = app.control.inspect().stats()
            if stats:
                return [{"id": k, "status": "pong", "max_concurrency":stats[k]['pool']['max-concurrency']} for k in stats.keys()]
            return []
        except Exception as e:
            logger.error('Error during node detection')
            return None

    def get_node(self, id):
        try:
            logger.debug('Retrieving details for cluster node ' + str(id))
            return app.control.inspect().stats()[id]
        except Exception as e:
            logger.error('Error during cluster node ' + str(id) + ' details retrieving')
            return None