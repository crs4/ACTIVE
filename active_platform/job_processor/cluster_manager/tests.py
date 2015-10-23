# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from cluster_manager import CeleryManager
from django.test import TestCase
from time import sleep

# test the base cluster manager methods
# for these tests a local instance with the following charateristics has been used:
# num_nodes = 1
# nodename  = "celery@LANTANIO"
# max_conc  = 12
#
# NB: a celery cluster must be executed during tests execution

class TestCluster(TestCase):
        def test_start(self):
                # TODO
                cm = CeleryManager()
                res = cm.start()
                self.assertEqual(True, res)

        def test_restart(self):
                cm = CeleryManager()
                res = cm.restart()
                self.assertEqual(True, res)

        def test_list(self):
                cm = CeleryManager()
                list = cm.list_nodes()
                self.assertEqual(1, len(list))

        def test_get(self):
                cm = CeleryManager()
                node = cm.get_node("celery@LANTANIO")
                self.assertNotEqual(None, node)

        def test_stop(self):
                cm = CeleryManager()
                cm.stop()
                sleep(1)
                list = cm.list_nodes()
                self.assertEqual(0, len(list))
