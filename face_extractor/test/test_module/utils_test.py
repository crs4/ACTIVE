import os
import unittest
import sys

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.utils as utils


class TestFaceModels(unittest.TestCase):
    """
    Execute software test on utils module
    """

    def get_time_intervals_test(self):
        time_list = [1, 2, 4, 5, 6, 8, 10, 11, 12, 13, 13.5, 20]
        min_sep = 1.2
        intervals = utils.get_time_intervals(time_list, min_sep)
        self.assertEqual(len(intervals), 3)
        self.assertEqual(intervals[2][0], 10)
        self.assertEqual(intervals[2][1], 3.5)
