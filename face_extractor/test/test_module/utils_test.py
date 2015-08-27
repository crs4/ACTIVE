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

    def test_get_time_intervals(self):
        time_list = [1, 2, 4, 5, 6, 8, 10, 11, 12, 13, 13.5, 20]
        min_sep = 1.2
        intervals = utils.get_time_intervals(time_list, min_sep)
        self.assertEqual(len(intervals), 3)
        self.assertEqual(intervals[2][0], 10)
        self.assertEqual(intervals[2][1], 3.5)

    def test_is_rect_similar(self):
        rect1 = (0, 0, 100, 100)
        rect2 = (25, 25, 50, 50)
        (similar, int_area, int_area_pct) = utils.is_rect_similar(
            rect1, rect2, 0)
        self.assertTrue(similar)
        self.assertEqual(int_area, 50 * 50)
        self.assertEqual(int_area_pct, 0.25)

        rect1 = (25, 25, 50, 50)
        rect2 = (0, 0, 100, 100)
        (similar, int_area, int_area_pct) = utils.is_rect_similar(
            rect1, rect2, 0)
        self.assertTrue(similar)
        self.assertEqual(int_area, 50 * 50)
