import cv2
import os
import person_tracking as pt
import sys
import unittest

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_detection import detect_faces_in_image

class TestPersonTracking(unittest.TestCase):
    """
    Execute software test on person_tracking module
    """

    def test_find_person_by_clothes(self):

        # TODO CHANGE AFTER HAVING MOVED CODE
        # image_path = ('..' + os.sep + 'test_files' + os.sep +
        #               'person_tracking' + os.sep + 'Test.jpg')
        image_path = ('test_files' + os.sep +
                      'person_tracking' + os.sep + 'Test.jpg')
        # ref_image_path = ('..' + os.sep + 'test_files' + os.sep +
        #                   'person_tracking' + os.sep + 'Reference.jpg')
        ref_image_path = ('test_files' + os.sep +
                          'person_tracking' + os.sep + 'Reference.jpg')

        align_path = c.ALIGNED_FACES_PATH

        # Detect faces in image and take first result

        result_dict = detect_faces_in_image(
            ref_image_path, align_path, None, False)

        if c.FACES_KEY in result_dict:
            faces = result_dict[c.FACES_KEY]
            if len(faces) > 0:
                face_dict = faces[0]
                bbox = face_dict[c.BBOX_KEY]

                params = None
                show_results = True

                bbox = pt.find_person_by_clothes(
                    image_path, ref_image_path, bbox, params, show_results)

                if bbox:
                    x0 = bbox[0]
                    y0 = bbox[1]
                    width = bbox[2]
                    height = bbox[3]
                    x1 = x0 + width
                    y1 = y0 + height
                    im = cv2.imread(ref_image_path, cv2.IMREAD_COLOR)
                    im_height, im_width, channels = im.shape
                    self.assertGreaterEqual(x0, 0)
                    self.assertGreaterEqual(y0, 0)
                    self.assertLessEqual(x1, im_width)
                    self.assertLessEqual(y1, im_height)