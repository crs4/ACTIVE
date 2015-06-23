import os
import sys
import unittest

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.video_face_extractor import VideoFaceExtractor


class TestVideoFaceExtractor(unittest.TestCase):

    def test_analyze_video(self):
        resource_path = 'fic.02.mpg'

        resource_id = 'fic.02.mpg'

        params = {c.VIDEO_INDEXING_PATH_KEY: r'C:\Users\Maurizio\Documents\Face summarization\Test\Caption recognition'}

        fe = VideoFaceExtractor(resource_path, resource_id, params)

        fe.analyze_video()

    def test_add_keyfaces_to_models(self):

        self.test_analyze_video()

        resource_path = 'fic.02.mpg'

        resource_id = 'fic.02'

        fe = VideoFaceExtractor(resource_path, resource_id)

        people = fe.get_people()

        for person_dict in people:
            person_id = person_dict[c.PERSON_COUNTER_KEY]

            tag = str(person_id)

            fe.add_keyface_to_models(tag, person_id)

    def test_delete_analysis_results(self):

        self.test_analyze_video()

        resource_path = 'fic.02.mpg'

        resource_id = 'fic.02'

        fe = VideoFaceExtractor(resource_path, resource_id)

        fe.delete_analysis_results()

        exists = os.path.exists(fe.video_path)

        self.assertFalse(exists)

    def test_delete_rec_results(self):

        self.test_analyze_video()

        resource_path = 'fic.02.mpg'

        resource_id = 'fic.02'

        fe = VideoFaceExtractor(resource_path, resource_id)

        fe.delete_recognition_results()

        exists = os.path.exists(fe.video_path)

        self.assertTrue(exists)

        exists = os.path.exists(fe.rec_path)

        self.assertFalse(exists)

    def test_merge_consecutive_segments(self):

        params = {c.MIN_SEGMENT_DURATION_KEY: 1}

        fe = VideoFaceExtractor('path', 'id', params)

        segments = [{c.SEGMENT_START_KEY: 0,
                     c.SEGMENT_DURATION_KEY: 10000,
                     c.SEGMENT_COUNTER_KEY: 0,
                     c.FRAMES_KEY: [0, 1, 2, 3]},
                    {c.SEGMENT_START_KEY: 10500,
                     c.SEGMENT_DURATION_KEY: 4500,
                     c.SEGMENT_COUNTER_KEY: 1,
                     c.FRAMES_KEY: [4, 5]},
                    {c.SEGMENT_START_KEY: 15900,
                     c.SEGMENT_DURATION_KEY: 14100,
                     c.SEGMENT_COUNTER_KEY: 2,
                      c.FRAMES_KEY: [6]},
                    {c.SEGMENT_START_KEY: 32000,
                     c.SEGMENT_DURATION_KEY: 8000,
                     c.SEGMENT_COUNTER_KEY: 3,
                      c.FRAMES_KEY: [7, 8, 9]},
                    {c.SEGMENT_START_KEY: 45000,
                     c.SEGMENT_DURATION_KEY: 5000,
                     c.SEGMENT_COUNTER_KEY: 4,
                     c.FRAMES_KEY: [10, 11, 12, 13, 14, 15]},
                    {c.SEGMENT_START_KEY: 50000,
                     c.SEGMENT_DURATION_KEY: 5000,
                     c.SEGMENT_COUNTER_KEY: 5,
                     c.FRAMES_KEY: [16, 17]}]

        fe.recognized_faces = [{c.ASSIGNED_LABEL_KEY: 1,
                               c.SEGMENTS_KEY: segments}]

        fe.merge_consecutive_segments()

        segments = fe.recognized_faces[0][c.SEGMENTS_KEY]

        self.assertEqual(len(segments), 3)

        self.assertEqual(segments[0][c.SEGMENT_DURATION_KEY], 30000)

        self.assertEqual(len(segments[0][c.FRAMES_KEY]), 7)

    def test_merge_labels(self):

        fe = VideoFaceExtractor('path', 'id')

        segments_1 = ['1a', '1b', '1c']
        segments_2 = ['2a', '2b', '2c']
        segments_3 = ['3a', '3b', '3c']

        fe.recognized_faces = [{c.ASSIGNED_LABEL_KEY: 1,
                                c.SEGMENTS_KEY: segments_1},
                               {c.ASSIGNED_LABEL_KEY: 2,
                                c.SEGMENTS_KEY: segments_2},
                               {c.ASSIGNED_LABEL_KEY: 1,
                                c.SEGMENTS_KEY: segments_1},
                               {c.ASSIGNED_LABEL_KEY: 3,
                                c.SEGMENTS_KEY: segments_3},
                               {c.ASSIGNED_LABEL_KEY: 1,
                                c.SEGMENTS_KEY: segments_1},
                               {c.ASSIGNED_LABEL_KEY: 2,
                                c.SEGMENTS_KEY: segments_2}]

        fe.merge_labels()

        self.assertEqual(len(fe.recognized_faces), 3)

        self.assertEqual(len(fe.recognized_faces[0][c.SEGMENTS_KEY]), 9)

if __name__ == '__main__':
    unittest.main()
