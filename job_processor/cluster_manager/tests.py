"""
Module defined to test the ClusterManager functionalities.
It is necessary to have a cluster already running for test execution.
NB: if the cluster is stopped before other test execution the latter will fail.
NB: tests have been executed using only one cluster node in a Celery cluster.
"""

from django.test import TestCase
from cluster_manager.cluster.cluster_manager import CeleryManager
from time import sleep

class TestCluster(TestCase):
    """
    Class containing the main test for a Clustetr Manager.
    """
    def test_start(self):
        """
        Test the init of a cluster.
        """
        cm = CeleryManager()
        res = cm.start()
        self.assertEqual(True, res)

    def test_restart(self):
        """
        Test the restart of a cluster.
        """
        cm = CeleryManager()
        res = cm.restart()
        self.assertEqual(True, res)

    def test_list(self):
        """
        Test the listing of all cluster nodes (one expected).
        """
        cm = CeleryManager()
        list = cm.list_nodes()
        self.assertEqual(1, len(list))

    def test_get(self):
        """
        Test the retrieving of cluster node data.
        """
        cm = CeleryManager()
        node_name = cm.list_nodes()[0]['id']
        node = cm.get_node(node_name)
        self.assertNotEqual(None, node)

    def test_stop(self):
        """
        Test used to stop the execution of all cluster nodes.
        """
        cm = CeleryManager()
        cm.stop()
        sleep(1)
        list = cm.list_nodes()
        self.assertEqual(0, len(list))
