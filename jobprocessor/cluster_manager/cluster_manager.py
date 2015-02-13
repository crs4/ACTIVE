from abc import ABCMeta, abstractmethod
from jobprocessor.celery import app # dipendenza dal progetto principale....OK!


class ClusterManager:
	"""
	This class has beed defined in order to provide an abstraction
	from the technology used for the distributed computation.
	So it exposes the main funcionalities provided by a generic cluster.
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
        def purge(self):
                """
                Method used to delete all task previously submitted to the cluster. 
		It should stop and delete all activities executed by every node of the cluster.
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
		:param id: The name used to identify a specific node of the cluster.
		:returns: A dictionary with all informations associated to the specified node. None in case of error.
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
		# TODO!!!!!!!!!!!
		print("... What the fuck!!!")
		return False

	def stop(self):
		try:
			app.control.broadcast("shutdown")
		except:
			return False
		return True

	def restart(self):
		try:
			app.control.broadcast("pool_restart", arguments = {'reload': True})
		except:
			return False
		return True

	def purge(self):
		# TODO !!!!!!!!!!!!
		# app.control.broadcast("revoke", arguments={'terminate' = True, 'task_id' = 'val'})
		return False

	def list_nodes(self):
		try:
			nodes = app.control.inspect().ping()
			if(nodes):
				return nodes.keys()
			else:
				return {}
		except:
			return None

	def get_node(self, id):
		try:
			return app.control.inspect().stats()[id]
		except:
			return None
