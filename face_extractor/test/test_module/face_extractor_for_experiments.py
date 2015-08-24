import cv2
import math
import numpy as np
import os
import pickle
import sys
import time

import constants_for_experiments as ce
from face_recognition import recognize_face
from utils_for_experiments import track_faces_with_LBP

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_detection import detect_faces_in_image

from tools.utils import aggregate_frame_results


class FaceExtractor(object):
    """
    Tool for detecting and recognizing faces in images and video.
    Used for face extraction experiments.
    The configuration parameters define
    and customize the face extraction algorithm.
    If any of the configuration parameters
    is not provided a default value is used.

    :type  face_models: a FaceModels object
    :param face_models: the face models data structure

    :type  params: dictionary
    :param params: configuration parameters to be used for the face extraction
                   (see table)

    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    eye_detection_classifier                      Classifier for eye detection              'haarcascade_mcs_lefteye.xml'
    face_detection_algorithm                      Classifier for face detection             'HaarCascadeFrontalFaceAlt2'
                                                  ('HaarCascadeFrontalFaceAlt',
                                                  'HaarCascadeFrontalFaceAltTree',
                                                  'HaarCascadeFrontalFaceAlt2',
                                                  'HaarCascadeFrontalFaceDefault',
                                                  'HaarCascadeProfileFace',
                                                  'HaarCascadeFrontalAndProfileFaces',
                                                  'HaarCascadeFrontalAndProfileFaces2',
                                                  'LBPCascadeFrontalface',
                                                  'LBPCascadeProfileFace' or
                                                  'LBPCascadeFrontalAndProfileFaces')
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch')
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    aligned_faces_path                            Default path of directory
                                                  for aligned faces
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    db_name                                       Name of single file
                                                  containing face models
    db_models_path                                Path of directory containing face models
    face_model_algorithm                          Algorithm for face recognition            'LBP'
                                                  ('Eigenfaces', 'Fisherfaces' or 'LBP')
    LBP_grid_x                                    Number of columns in grid                 4
                                                  used for calculating LBP
    LBP_grid_y                                    Number of columns in grid                 8
                                                  used for calculating LBP
    LBP_neighbors                                 Number of neighbors                       8
                                                  used for calculating LBP
    LBP_radius                                    Radius used                               1
                                                  for calculating LBP (in pixels)
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    use_eye_detection                             If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  test images
    use_eye_detection_in_training                 If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  training images
    use_eyes_position                             If True, align faces in test images       True
                                                  by using eye positions
    use_eyes_position_in_training                 If True, align faces in training images   True
                                                  by using eye positions
    use_face_detection_in_training                If True, use face detection               False
                                                  for images in training set
    use_NBNN                                      If True,                                  False
                                                  use Naive Bayes Nearest Neighbor
    use_one_file_for_face_models                  If True, use one file for face models     True
    use_resizing                                  If True, resize images                    True
    use_weighted_regions                          If True, use weighted LBP                 False
    ============================================  ========================================  ==============
    """

    def __init__(self, face_models=None, params=None):
        """
        Initialize the face extractor.
        The configuration parameters define
        and customize the face extraction algorithm.
        If any of the configuration parameters
        is not provided a default value is used.

        :type  face_models: a FaceModels object
        :param face_models: the face models data structure

        :type  params: dictionary
        :param params: configuration parameters (see table)
        """

        self.params = params

        self.face_models = face_models

        self.progress = 0

        self.db_result4image = {}

    def extract_faces_from_image(self, resource_path):
        """
        Launch the face extractor on one image resource.
        This method returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path

        :rtype: float
        :returns: handle for getting results
        """
        # Save processing time
        start_time = cv2.getTickCount()

        error = None

        # Face detection
        align_path = c.ALIGNED_FACES_PATH
        if ((self.params is not None) and
                (c.ALIGNED_FACES_PATH_KEY in self.params)):
            align_path = self.params[c.ALIGNED_FACES_PATH_KEY]

        detection_result = detect_faces_in_image(resource_path, align_path,
                                                 self.params, False)

        detection_error = detection_result[c.ERROR_KEY]

        if not detection_error:

            face_images = detection_result[c.FACES_KEY]

            detected_faces = detection_result[c.FACES_KEY]

            # Face recognition

            faces = []
            # face=cv2.imread(resource_path,cv2.IMREAD_GRAYSCALE);
            # face_images=[face]
            for det_face_dict in face_images:

                face_dict = {}

                face = det_face_dict[c.FACE_KEY]
                bbox = det_face_dict[c.BBOX_KEY]

                # Resize face
                resize_face = ce.USE_RESIZING

                if ((self.params is not None) and
                        (ce.USE_RESIZING_KEY in self.params)):
                    resize_face = self.params[ce.USE_RESIZING_KEY]

                if resize_face:

                    face_width = c.CROPPED_FACE_WIDTH
                    face_height = c.CROPPED_FACE_HEIGHT

                    if ((self.params is not None) and
                            (c.CROPPED_FACE_WIDTH_KEY in self.params) and
                            (c.CROPPED_FACE_HEIGHT_KEY in self.params)):
                        face_width = self.params[c.CROPPED_FACE_WIDTH_KEY]
                        face_height = self.params[c.CROPPED_FACE_HEIGHT_KEY]

                    new_size = (face_width, face_height)
                    face = cv2.resize(face, new_size)

                rec_result = recognize_face(
                    face, self.face_models, self.params, False)

                tag = rec_result[c.ASSIGNED_TAG_KEY]
                confidence = rec_result[c.CONFIDENCE_KEY]
                face_dict[c.ASSIGNED_TAG_KEY] = tag
                face_dict[c.CONFIDENCE_KEY] = confidence
                face_dict[c.BBOX_KEY] = bbox
                face_dict[c.FACE_KEY] = face
                faces.append(face_dict)

            processing_time_in_clocks = cv2.getTickCount() - start_time
            processing_time_in_seconds = (
                processing_time_in_clocks / cv2.getTickFrequency())

            # Populate dictionary with results
            results = {c.ELAPSED_CPU_TIME_KEY: processing_time_in_seconds,
                       c.ERROR_KEY: error, c.FACES_KEY: faces}

        else:

            results = {c.ERROR_KEY: detection_error}

        self.progress = 100
        handle = time.time()
        self.db_result4image[handle] = results

        return handle

    def extract_faces_from_video(self, resource):
        """
        Launch the face extractor on one video resource.
        This method returns a task handle.

        :type  resource: string
        :param resource: resource file path

        :rtype: float
        :returns: handle for getting results
        """

        # Set parameters
        load_ind_frame_results = ce.LOAD_IND_FRAMES_RESULTS
        sim_tracking = ce.SIM_TRACKING
        sliding_window_size = ce.SLIDING_WINDOW_SIZE
        used_fps = c.USED_FPS
        use_or_fps = c.USE_ORIGINAL_FPS
        use_sliding_window = ce.USE_SLIDING_WINDOW
        use_tracking = ce.USE_TRACKING
        if self.params is not None:
            if ce.LOAD_IND_FRAMES_RESULTS_KEY in self.params:
                load_ind_frame_results = (
                    self.params[ce.LOAD_IND_FRAMES_RESULTS_KEY])
            if ce.SIM_TRACKING_KEY in self.params:
                sim_tracking = self.params[ce.SIM_TRACKING_KEY]
            if ce.SLIDING_WINDOW_SIZE in self.params:
                sliding_window_size = self.params[ce.SLIDING_WINDOW_SIZE_KEY]
            if c.USED_FPS_KEY in self.params:
                used_fps = self.params[c.USED_FPS_KEY]
            if c.USE_ORIGINAL_FPS_KEY in self.params:
                use_or_fps = self.params[c.USE_ORIGINAL_FPS_KEY]
            if ce.USE_SLIDING_WINDOW_KEY in self.params:
                use_sliding_window = self.params[ce.USE_SLIDING_WINDOW_KEY]
            if ce.USE_TRACKING_KEY in self.params:
                use_tracking = self.params[ce.USE_TRACKING_KEY]

        # Save processing time
        start_time = cv2.getTickCount()

        error = None
        frames = None
        segments = None

        capture = cv2.VideoCapture(resource)

        # Counter for all frames
        frame_counter = 0

        # Counter for analyzed frames
        anal_frame_counter = 0

        # Value of frame_counter for last analyzed frame
        last_anal_frame = 0

        if capture is None or not capture.isOpened():

            error = 'Error in opening video file'

        else:

            frames = []

            if ((use_tracking or sim_tracking or use_sliding_window)
                    and load_ind_frame_results):

                # Load frames by using pickle

                print 'Loading frames'

                resource_name = os.path.basename(resource)

                file_name = resource_name + '.pickle'

                file_path = os.path.join(ce.FRAMES_FILES_PATH, file_name)

                with open(file_path) as f:

                    frames = pickle.load(f)

                    anal_frame_counter = len(frames)

            else:

                video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)

                tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

                while True:

                    frame_dict = {}

                    ret, frame = capture.read()

                    if not ret:
                        break

                    # Next frame to be analyzed
                    next_frame = last_anal_frame + (video_fps / used_fps) - 1

                    if use_or_fps or (frame_counter > next_frame):

                        # Frame position in video in seconds
                        elapsed_video_ms = capture.get(
                            cv2.cv.CV_CAP_PROP_POS_MSEC)
                        elapsed_video_s = elapsed_video_ms / 1000

                        self.progress = 100 * (frame_counter / tot_frames)

                        # TEST ONLY
                        print('progress: ' + str(self.progress) + '%')

                        cv2.imwrite(ce.TMP_FRAME_FILE_PATH, frame)

                        handle = self.extract_faces_from_image(
                            ce.TMP_FRAME_FILE_PATH)

                        frame_results = self.get_results(handle)

                        frame_error = frame_results[c.ERROR_KEY]

                        if frame_error:

                            error = frame_results[c.ERROR_KEY]

                            break

                        else:

                            frame_dict[c.ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                            frame_dict[c.FACES_KEY] = frame_results[c.FACES_KEY]

                            frame_dict[c.FRAME_COUNTER_KEY] = frame_counter

                            frames.append(frame_dict)

                        anal_frame_counter += 1

                        last_anal_frame = frame_counter

                    frame_counter += 1

                frames_dict = {c.FRAMES_KEY: frames}

                # Save frames by using pickle

                resource_name = os.path.basename(resource)

                file_name = resource_name + '.pickle'

                file_path = os.path.join(ce.FRAMES_FILES_PATH, file_name)

                with open(file_path, 'w') as f:

                    pickle.dump(frames, f)

            if use_tracking and (frames is not None):

                segments = track_faces_with_LBP(frames, self.face_models)

            elif use_sliding_window and (frames is not None):

                frame_rate = capture.get(cv2.cv.CV_CAP_PROP_FPS)

                frame_nr_in_window = frame_rate * sliding_window_size

                frame_nr_half_window = int(math.floor(frame_nr_in_window / 2))

                sl_window_frame_counter = 0

                for frame in frames:

                    # Get faces from frame results
                    faces = frame[c.FACES_KEY]

                    if len(faces) != 0:

                        # Select frames to be included in window

                        first_frame_in_window = (
                            sl_window_frame_counter - frame_nr_half_window)
                        # First frame in window is first frame
                        # of all video if window exceeds video
                        if first_frame_in_window < 0:
                            first_frame_in_window = 0

                        last_frame_in_window = (
                            sl_window_frame_counter + frame_nr_half_window)

                        if last_frame_in_window > (len(frames) - 1):
                            last_frame_in_window = len(frames) - 1

                        window_frames = frames[first_frame_in_window: (
                            last_frame_in_window + 1)]

                        window_frames_list = []

                        for window_frame in window_frames:

                            # Get tag from first face
                            faces = window_frame[c.FACES_KEY]

                            if len(faces) != 0:
                                first_face = faces[0]

                                assigned_tag = first_face[c.ASSIGNED_TAG_KEY]

                                confidence = first_face[c.CONFIDENCE_KEY]

                                window_frame_dict = {
                                    c.ASSIGNED_TAG_KEY: assigned_tag,
                                    c.CONFIDENCE_KEY: confidence}

                                window_frames_list.append(window_frame_dict)

                        # Final tag for each frame depends
                        # on assigned tags on all frames in window

                        [frame_final_tag,
                         frame_final_confidence] = aggregate_frame_results(
                            window_frames_list, self.face_models)

                        print('frame_final_tag: ', frame_final_tag)

                        frame[c.FACES_KEY][0][c.ASSIGNED_TAG_KEY] = frame_final_tag

                        frame[c.FACES_KEY][0][
                            c.CONFIDENCE_KEY] = frame_final_confidence

                    sl_window_frame_counter += 1

        processing_time_in_clocks = cv2.getTickCount() - start_time
        processing_time_in_seconds = (
            processing_time_in_clocks / cv2.getTickFrequency())

        # Populate dictionary with results
        results = {c.ELAPSED_CPU_TIME_KEY: processing_time_in_seconds,
                   c.ERROR_KEY: error, ce.TOT_FRAMES_NR_KEY: anal_frame_counter}

        if use_tracking:

            results[c.SEGMENTS_KEY] = segments

        else:

            results[c.FRAMES_KEY] = frames

        self.progress = 100
        handle = time.time()
        self.db_result4image[handle] = results

        return handle

    def get_results(self, handle):
        """
        Return the results of the face extraction process.
        If the handle was returned by extractFacesFromImage(), a dictionary
        is returned with the following entries:

        =====================================  ========================================
        Key                                    Value
        =====================================  ========================================
        elapsed_cpu_time                       The elapsed CPU time in seconds
        error                                  A string specifying an error condition,
                                               or None if no errors occurred
        faces                                  A list of tags
                                               with associated bounding boxes
        =====================================  ========================================

        Example:
            results = {'elapsed_cpu_time':  0.011,
                       'error': None,
                       'faces': [{'tag': 'Barack Obama', 'confidence': 60,
                                  'bbox':(100,210, 50, 50)},
                                 {'tag': 'Betty White', 'confidence': 30,
                                  'bbox':(30, 250, 40, 45)}
                                ]
                      }

        For extractFacesFromVideo(), if no tracking is used,
        a dictionary is returned with the following entries:

        =====================================  ========================================
        Key                                    Value
        =====================================  ========================================
        elapsed_cpu_time                       The elapsed CPU time in seconds
        error                                  A string specifying an error condition,
                                               or None if no errors occurred
        frames                                 A list of frames,
                                               each containing a list of faces
        =====================================  ========================================

        Example:
            results = {'elapsed_cpu_time': 11.1,
                       'error':None,
                       'tot_frames_nr':299,
                       'frames': [{'elapsed_video_time': 0,
                                   'frame_counter': 0,
                                   'faces': [{'tag': 'Barack Obama',
                                              'confidence':60,
                                              'bbox':(100,210, 50, 50)},
                                             {'tag': 'Betty White',
                                              'confidence':30,
                                              'bbox':(30, 250, 40, 40)}
                                            ]
                                  {'elapsed_video_time':0.04,
                                   'frame_counter': 1,
                                   'faces': [{'tag': 'Barack Obama',
                                              'confidence':55,
                                              'bbox':(110,220, 50, 50)},
                                             {'tag': 'Betty White',
                                              'confidence':35,
                                              'bbox':(40, 270, 40, 40)}
                                              ]
                                 ]
                      }
        For extractFacesFromVideo(), if tracking is used,
        a dictionary is returned with the following entries:

        =====================================  ========================================
        Key                                    Value
        =====================================  ========================================
        elapsed_cpu_time                       The elapsed CPU time in seconds
        error                                  A string specifying an error condition,
                                               or None if no errors occurred
        segments                               A list of face tracks,
                                               each associated to a person
        =====================================  ========================================

        Example:
            results = {'elapsed_cpu_time': 11.1,
                       'error':None,
                       'tot_frames_nr':299,
                       'segments': [{'tag': 'Barack Obama'
                                     'confidence': 40,
                                     'frames': [{'elapsed_video_time': 0,
                                                 'frame_counter': 0,
                                                 'tag': 'Barack Obama',
                                                 'confidence': 60,
                                                 'bbox':(100,210, 50, 50)},
                                                {'elapsed_video_time':0.04},
                                                 'frame_counter': 1,
                                                 'tag': 'Barack Obama',
                                                 'confidence': 20,
                                                 'bbox':(110,220, 50, 50)}
                                                ]
                                    ]
                      }

        :type  handle: float
        :param handle: the task handle

        :rtype: dictionary
        :returns: dictionary with results
        """
        return self.db_result4image[handle]
