import constants as c

import copy

import cv2

import cv2.cv as cv

import face_detection as fd

import yaml

import logging

import math

import numpy as np

import os

import pickle as pk

import shutil

import sys

import utils

from caption_recognition import get_tag_from_image

from face_models import FaceModels

if c.USE_SKELETONS:
    from skeleton.skeletons import Farm, Seq
    from skeleton.visitors import Executor

# variable used for logging purposes
logger = logging.getLogger('face_recog')


class VideoFaceExtractor(object):
    """
    Tool for detecting and recognizing faces in video
    """

    def __init__(self, resource_path, resource_id, params=None):
        """
        Initialize the face extractor.
        The configuration parameters define
        and customize the face extraction algorithm.
        If any of the configuration parameters
        is not provided a default value is used.

        :type resource_path: string
        :param resource_path: file path of resource

        :type resource_id: string
        :param resource_id: identifier of resource

        :type  params: dictionary
        :param params: configuration parameters (see table)
        """
        # TODO: ADD TABLE WITH PARAMETERS
        self.anal_results = {}  # Dictionary with analysis results

        self.anal_times = {}  # Dictionary with times for analysis

        self.cloth_threshold = 0  # Threshold for clothing recognition

        self.cut_idxs = []  # List of frame indexes where new shots begin

        self.detected_faces = []  # List of detected faces

        # List of tracked faces not considered
        self.disc_tracked_faces = []

        self.faces_nr = {}  # Number of faces for each frame

        self.frame_list = []  # List of frame paths

        self.frames_in_models = {}  # Frames used in face models

        self.fps = 0  # Frame rate of video in frames per second

        self.hist_diffs = []  # List with histogram differences

        self.nose_pos_list = []  # List with nose positions

        self.params = params

        self.progress = 0  # Progress in analyzing video

        self.recognized_faces = []  # List of recognized faces

        self.resource_id = resource_id  # Id of resource being analyzed

        # Name of resource being analyzed
        self.resource_name = os.path.basename(resource_path)

        # Path of resource being analyzed
        self.resource_path = resource_path

        self.saved_frames = 0  # Number of saved and analyzed frames

        self.track_threshold = 0  # Threshold for tracking interruption

        self.tracked_faces = []  # List of tracked faces

        self.video_frames = 0  # Number of original frames in video

        # Setup directories and files with results

        file_name = self.resource_id + '.YAML'

        # Directory for this video     
        video_indexing_path = c.VIDEO_INDEXING_PATH

        if (params is not None) and (c.VIDEO_INDEXING_PATH_KEY in params):
            video_indexing_path = params[c.VIDEO_INDEXING_PATH_KEY]

        self.video_path = os.path.join(
            video_indexing_path, resource_id, c.FACE_EXTRACTION_DIR)

        # Directory for frame_list
        self.frames_path = os.path.join(self.video_path, c.FRAMES_DIR)

        # File with frame list
        self.frames_file_path = os.path.join(self.frames_path, file_name)

        # Directory for detection results
        self.det_path = os.path.join(self.video_path, c.FACE_DETECTION_DIR)

        # Directory for aligned faces
        self.align_path = os.path.join(
            self.det_path, c.ALIGNED_FACES_DIR)

        # File with detection results
        self.det_file_path = os.path.join(self.det_path, file_name)

        # Directory for tracking results
        self.track_path = os.path.join(self.video_path, c.FACE_TRACKING_DIR)

        # File with tracking results
        self.track_file_path = os.path.join(self.track_path, file_name)

        # Directory for face models
        self.face_models_path = os.path.join(
            self.video_path, c.FACE_MODELS_DIR)

        # Directory for cloth models
        self.cloth_models_path = os.path.join(
            self.video_path, c.CLOTH_MODELS_DIR)

        # File with list of frames in models
        self.frames_in_models_file_path = os.path.join(
            self.video_path, c.FRAMES_IN_MODELS_FILE)

        # File with nose positions
        self.nose_pos_file_path = os.path.join(
            self.video_path, c.NOSE_POSITIONS_FILE)

        # Directory for clustering results
        self.cluster_path = os.path.join(
            self.video_path, c.PEOPLE_CLUSTERING_DIR)

        # File with clustering results
        self.cluster_file_path = os.path.join(
            self.cluster_path, file_name)

        # File with number of faces in each frame
        self.faces_nr_path = os.path.join(
            self.video_path, c.FACES_NR_IN_FRAMES_FILE)

        # Directory for recognition results
        self.rec_path = os.path.join(self.video_path, c.FACE_RECOGNITION_DIR)

        # File with recognition results
        self.rec_file_path = os.path.join(self.rec_path, file_name)

        # Directory with complete annotations
        self.compl_ann_path = os.path.join(
            self.video_path, c.FACE_ANNOTATION_DIR)

        # Directory with simple annotations
        self.simple_ann_path = os.path.join(
            self.video_path, c.FACE_SIMPLE_ANNOTATION_DIR)

        # File with parameters
        params_file_name = self.resource_id + '_parameters.YAML'

        self.params_file_path = os.path.join(self.video_path, params_file_name)

        # File with times used for analysis
        analysis_file_name = self.resource_id + '_analysis_times.YAML'

        self.analysis_file_path = os.path.join(
            self.video_path, analysis_file_name)

    def add_keyface_to_models(self, label, person_counter, tag):
        """
        Add keyface of one cluster to global face models

        :type label: integer
        :param label: identifier of person in database

        :type person_counter: integer
        :param person_counter: identifier of person in video

        :type tag: string
        :param tag: tag of person whom keyface belong to

        :rtype: boolean
        :returns: True if keyface has been added to face models,
        False otherwise
        """

        logger.debug(
            'Adding key face for person with id '
            + str(label) + ' to global models')

        added = False

        try:

            # Check existence of recognition results
            if len(self.recognized_faces) == 0:

                # Try to load YAML file
                if os.path.exists(self.rec_file_path):

                    print 'Loading YAML file with recognition results'
                    logger.debug('Loading YAML file with recognition results')

                    with open(self.rec_file_path) as f:

                        self.recognized_faces = yaml.load(f)

                    print 'YAML file with recognition results loaded'
                    logger.debug('YAML file with recognition results loaded')

                else:

                    print 'Warning! No recognition results found!'
                    logger.warning('No recognition results found!')

                    return

            for person_dict in self.recognized_faces:

                p_counter = person_dict[c.PERSON_COUNTER_KEY]

                if person_counter == p_counter:

                    keyframe = person_dict[c.MEDOID_FRAME_NAME_KEY]

                    segment_list = person_dict[c.SEGMENTS_KEY]

                    for segment_dict in segment_list:

                        frame_list = segment_dict[c.FRAMES_KEY]

                        for frame_dict in frame_list:

                            frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                            if frame_name == keyframe:
                                frame_path = os.path.join(
                                    self.frames_path, frame_name)

                                aligned_name = frame_dict[
                                    c.ALIGNED_FACE_FILE_NAME_KEY]

                                complete_file_name = (
                                    aligned_name +
                                    c.ALIGNED_FACE_GRAY_SUFFIX + '.png')

                                aligned_file_path = os.path.join(
                                    self.align_path, complete_file_name)

                                aligned_face = cv2.imread(
                                    aligned_file_path, cv2.IMREAD_GRAYSCALE)

                                left_eye_pos = frame_dict[c.LEFT_EYE_POS_KEY]

                                right_eye_pos = frame_dict[c.RIGHT_EYE_POS_KEY]

                                eye_pos = (
                                    left_eye_pos[0],
                                    left_eye_pos[1],
                                    right_eye_pos[0],
                                    right_eye_pos[1])

                                bbox = frame_dict[c.DETECTION_BBOX_KEY]

                                fm = FaceModels(self.params)

                                added = fm.add_face(label, tag, frame_path,
                                                    aligned_face, eye_pos, bbox)

                                return added

        except IOError as e:
            error_str = "I/O error({0}): {1}".format(e.errno, e.strerror)
            print error_str
            logger.debug(error_str)

        except KeyError as e:
            error_str = "KeyError({0})".format(str(e))
            print error_str
            logger.debug(error_str)

        except:
            error_str = "Unexpected error:", sys.exc_info()[0]
            print error_str
            logger.debug(error_str)

            raise

        return added

    def analyze_video(self):
        """
        Analyze video
        """

        logger.debug('Analyzing video')

        # Try to load YAML file with video parameters
        if os.path.exists(self.params_file_path):

            print 'Loading YAML file with video parameters'
            logger.debug('Loading YAML file with video parameters')

            param_dict = utils.load_YAML_file(self.params_file_path)

            if param_dict:
                self.fps = param_dict[c.VIDEO_FPS_KEY]

                saved_frames = param_dict[c.VIDEO_SAVED_FRAMES_KEY]

                self.saved_frames = float(saved_frames)

                tot_frames = param_dict[c.VIDEO_TOT_FRAMES_KEY]

                self.video_frames = float(tot_frames)

                print 'YAML file with video parameters loaded'
                logger.debug('YAML file with video parameters loaded')

        # Try to load YAML file with times for analysis
        if os.path.exists(self.analysis_file_path):

            print 'Loading YAML file with analysis times'
            logger.debug('Loading YAML file with analysis times')
            anal_dict = utils.load_YAML_file(self.analysis_file_path)

            if anal_dict:
                self.anal_times = anal_dict

                print 'YAML file with analysis times loaded'
                logger.debug('YAML file with analysis times loaded')

        self.get_frame_list()

        self.detect_faces_in_video()

        self.track_faces_in_video()

        self.cluster_faces_in_video()

        self.recognize_people_in_video()

        self.show_keyframes()

        # TODO UNCOMMENT FOR EXPERIMENTS
        self.save_people_files()

        self.save_analysis_results()

    def calc_hist_diff(self):
        """
        Calculate histogram differences between consecutive frames,
        storing shot cuts in self.cut_idxs.
        """

        logger.debug(
            'Calculating histogram differences between consecutive frames')

        half_window_size = c.HALF_WINDOW_SIZE

        std_mult_frame = c.STD_MULTIPLIER_FRAME

        if self.params is not None:

            if c.HALF_WINDOW_SIZE_KEY in self.params:
                half_window_size = self.params[c.HALF_WINDOW_SIZE_KEY]

            if c.STD_MULTIPLIER_FRAME_KEY in self.params:
                std_mult_frame = self.params[c.STD_MULTIPLIER_FRAME_KEY]

        # Check existence of frame list
        if len(self.frame_list) == 0:

            # Try to load YAML file
            if os.path.exists(self.frames_file_path):

                print 'Loading YAML file with frame list'
                logger.debug('Loading YAML file with frame list')

                with open(self.frames_file_path) as f:

                    self.frame_list = yaml.load(f)

                print 'YAML file with frame list loaded'
                logger.debug('YAML file with frame list loaded')

            else:

                print 'Warning! No frame list found!'
                logger.warning('No frame list found!')

                return

        print '\n\n### Calculating histogram differences ###\n'
        logger.debug('\n\n### Calculating histogram differences ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        # List with histogram differences (all frames)
        self.hist_diffs = []

        prev_hists = None

        counter = 0

        # Iterate through all frames
        for frame_dict in self.frame_list:

            self.progress = 100 * (counter / self.saved_frames)

            print('progress: ' + str(self.progress) + ' %          \r'),

            frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

            frame_path = os.path.join(self.frames_path, frame_name)

            image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

            # Calculate difference between histograms
            [tot_diff, prev_hists] = utils.get_hist_difference(
                image, prev_hists)

            if tot_diff is not None:
                self.hist_diffs.append(tot_diff)

            del image

            counter += 1

        # Calculate shot cuts

        if len(self.hist_diffs) > 0:
            self.cut_idxs = utils.get_shot_changes(
                self.hist_diffs, half_window_size, std_mult_frame)

            # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        seconds = time_in_clocks / cv2.getTickFrequency()

        print 'Time for calculation of histogram differences: ', seconds, 's\n'
        logger.debug(
            'Time for calculation of histogram differences: ', seconds, 's\n')

        self.anal_times[c.SHOT_CUT_DETECTION_TIME_KEY] = seconds

        utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def calculate_medoids(self):
        """
        Calculate cluster medoids
        """

        logger.debug('Calculating cluster medoids')

        if len(self.recognized_faces) == 0:

            # Try to load YAML file with clustering results
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'
                logger.debug('Loading YAML file with recognition results')

                with open(self.rec_file_path) as f:

                    self.recognized_faces = yaml.load(f)

                print 'YAML file with recognition results loaded'
                logger.debug('YAML file with recognition results loaded')

            else:

                print 'Warning! No recognition results found!'
                logger.warning('No recognition results found!')

                return

        print '\n\n### Calculating cluster medoids ###\n'
        logger.debug('\n\n### Calculating cluster medoids ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        keys = self.frames_in_models.keys()

        if len(keys) == 0:

            # Try to load YAML file with list of frames in models

            if os.path.exists(self.frames_in_models_file_path):

                print 'Loading YAML file with frames in models'
                logger.debug('Loading YAML file with frames in models')

                with open(self.frames_in_models_file_path) as f:

                    self.frames_in_models = yaml.load(f)

                print 'YAML file with frames in models loaded'
                logger.debug('YAML file with frames in models loaded')

            else:

                print 'Warning! No YAML file with frames in models found'
                logger.warning('No YAML file with frames in models found')
                return

        p_counter = 0

        clusters_nr = float(len(self.recognized_faces))

        # Iterate through people clusters
        for person_dict in self.recognized_faces:

            self.progress = 100 * (p_counter / clusters_nr)

            print('progress: ' + str(self.progress) + ' %          \r'),

            segment_list = person_dict[c.SEGMENTS_KEY]

            models_list = []

            frames_in_models_list = []

            # Iterate through segments related to this person
            for segment_dict in segment_list:

                segment_counter = segment_dict[c.SEGMENT_COUNTER_KEY]

                # Get face model from this segment
                db_path = os.path.join(
                    self.face_models_path, str(segment_counter))

                if os.path.isfile(db_path):

                    model = cv2.createLBPHFaceRecognizer()

                    model.load(db_path)

                    if model:
                        # Get histograms from model

                        hists = model.getMatVector("histograms")

                        models_list.extend(hists)

                        frames_in_model = self.frames_in_models[segment_counter]

                        frames_in_models_list.extend(frames_in_model)

            min_sum = sys.maxint

            min_idx = 0

            for i in range(0, len(models_list)):

                sum_i = 0

                hist_i = models_list[i][0]

                # Compare histograms to other histograms in models
                for j in range(0, len(models_list)):

                    if i != j:

                        hist_j = models_list[j][0]

                        diff = cv2.compareHist(
                            hist_i, hist_j, cv.CV_COMP_CHISQR)

                        sum_i = sum_i + diff

                        if sum_i > min_sum:
                            continue

                if sum_i < min_sum:
                    min_sum = sum_i

                    min_idx = i

            medoid_frame = frames_in_models_list[min_idx]

            self.recognized_faces[p_counter][
                c.MEDOID_FRAME_NAME_KEY] = medoid_frame

            p_counter += 1

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()

        print 'Time for calculating cluster medoids:', time_in_seconds, 's\n'
        logger.debug('Time for calculating cluster medoids:', time_in_seconds, 's\n')

    def cluster_faces_in_video(self):
        """
        Cluster face tracks on analyzed video,
        assigning a generic tag to each cluster (person).
        """

        logger.debug('Executing people clustering')

        rec_loaded = False

        # Try to load YAML file with recognition results
        if os.path.exists(self.cluster_file_path):

            print 'Loading YAML file with clustering results'
            logger.debug('Loading YAML file with clustering results')

            rec_faces = utils.load_YAML_file(self.cluster_file_path)

            if rec_faces:
                self.recognized_faces = rec_faces

                print 'YAML file with clustering results loaded'
                logger.debug('YAML file with clustering results loaded')

                rec_loaded = True

        if not rec_loaded:

            if len(self.tracked_faces) == 0:

                # Try to load YAML file
                if os.path.exists(self.track_file_path):

                    print 'Loading YAML file with tracking results'
                    logger.debug('Loading YAML file with tracking results')

                    with open(self.track_file_path) as f:

                        self.tracked_faces = yaml.load(f)

                    print 'YAML file with tracking results loaded'
                    logger.debug('YAML file with tracking results loaded')

                else:

                    print 'Warning! No tracking results found!'
                    logger.warning('No tracking results found!')
                    return

                    # Make copy of tracked faces
            tracking_list = list(self.tracked_faces)

            # Save face models
            self.save_face_models(tracking_list)

            use_clothing_rec = c.USE_CLOTHING_RECOGNITION

            if ((self.params is not None) and
                    (c.USE_CLOTHING_RECOGNITION_KEY in self.params)):
                use_clothing_rec = self.params[c.USE_CLOTHING_RECOGNITION_KEY]

            if use_clothing_rec:
                # Save cloth models
                self.save_cloth_models(tracking_list)

            print '\n\n### People clustering ###\n'
            logger.debug('\n\n### People clustering ###\n')

            # Save processing time
            start_time = cv2.getTickCount()

            self.recognized_faces = []

            # List of segments already analyzed and annotated
            ann_segments = []

            # Iterate through tracked faces

            person_counter = 0

            segment_counter = 0

            tracked_faces_nr = float(len(tracking_list))

            model = None

            for tracking_segment_dict in tracking_list:

                self.progress = 100 * (segment_counter / tracked_faces_nr)

                print('progress: ' + str(self.progress) + ' %          \r'),

                if segment_counter not in ann_segments:

                    # Save all segments relative
                    # to one person in person_dict
                    person_dict = {c.PERSON_COUNTER_KEY: person_counter,
                                   c.ASSIGNED_LABEL_KEY: c.UNDEFINED_LABEL,
                                   c.ASSIGNED_TAG_KEY: c.UNDEFINED_TAG}

                    segment_list = []

                    segment_dict = {}

                    segment_frame_list = tracking_segment_dict[c.FRAMES_KEY]

                    segment_dict[c.FRAMES_KEY] = segment_frame_list

                    segment_dict[c.ASSIGNED_TAG_KEY] = c.UNDEFINED_TAG

                    segment_dict[c.CONFIDENCE_KEY] = 0

                    segment_dict[c.SEGMENT_COUNTER_KEY] = segment_counter

                    # Start of segment in milliseconds
                    # of elapsed time in video

                    start = tracking_segment_dict[c.SEGMENT_START_KEY]

                    segment_dict[c.SEGMENT_START_KEY] = start

                    # Duration of segment in milliseconds

                    duration = tracking_segment_dict[c.SEGMENT_DURATION_KEY]

                    segment_dict[c.SEGMENT_DURATION_KEY] = duration

                    segment_list.append(segment_dict)

                    ann_segments.append(segment_counter)

                    db_path = os.path.join(
                        self.face_models_path, str(segment_counter))

                    if os.path.isfile(db_path):

                        model = cv2.createLBPHFaceRecognizer()

                        model.load(db_path)

                        if model:
                            # Use model of this segment
                            # to recognize faces of remaining segments

                            ann_segments = self.search_face(ann_segments,
                                                            segment_list, model,
                                                            segment_counter)

                            # Add segments to person dictionary

                            person_dict[c.SEGMENTS_KEY] = segment_list

                            # Save total duration of video in milliseconds

                            tot_duration = (
                                self.video_frames * 1000.0 / self.fps)

                            person_dict[c.VIDEO_DURATION_KEY] = tot_duration

                            self.recognized_faces.append(person_dict)

                    person_counter += 1

                segment_counter += 1

            del model

            if not (os.path.exists(self.cluster_path)):
                # Create directory for people clustering
                os.makedirs(self.cluster_path)

            # Save clustering result in YAML file
            utils.save_YAML_file(
                self.cluster_file_path, self.recognized_faces)

            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for people clustering:', time_in_seconds, 's\n'
            logger.debug('Time for people clustering:', time_in_seconds, 's\n')

            self.anal_times[c.PEOPLE_CLUSTERING_TIME_KEY] = time_in_seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def create_cloth_model(self, segment_dict):
        """
        Create cloth model for one face track.

        :type segment_dict: dictionary
        :param segment_dict: video segment relative to face track

        :rtype: list
        :returns: list of color histograms
        """

        # List of color histograms
        model = []

        # Extract list of frames from dictionary
        frame_list = segment_dict[c.FRAMES_KEY]

        all_bboxes_in_frames = c.ALL_CLOTH_BBOXES_IN_FRAMES
        cl_pct_height = c.CLOTHES_BBOX_HEIGHT
        cl_pct_width = c.CLOTHES_BBOX_WIDTH
        hsv_channels = c.CLOTHING_REC_HSV_CHANNELS_NR
        min_size = c.MIN_CLOTH_MODEL_SIZE
        neck_pct_height = c.NECK_HEIGHT
        use_dom_color = c.CLOTHING_REC_USE_DOMINANT_COLOR
        use_mean_x = c.CLOTHING_REC_USE_MEAN_X_OF_FACES
        use_3_bboxes = c.CLOTHING_REC_USE_3_BBOXES
        kernel_size = c.HIST_SMOOTHING_KERNEL_SIZE

        if self.params is not None:
            if c.ALL_CLOTH_BBOXES_IN_FRAMES in self.params:
                all_bboxes_in_frames = self.params[
                    c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY]
            if c.CLOTHES_BBOX_HEIGHT_KEY in self.params:
                cl_pct_height = self.params[c.CLOTHES_BBOX_HEIGHT_KEY]
            if c.CLOTHES_BBOX_WIDTH_KEY in self.params:
                cl_pct_width = self.params[c.CLOTHES_BBOX_WIDTH_KEY]
            if c.CLOTHING_REC_HSV_CHANNELS_NR_KEY in self.params:
                hsv_channels = self.params[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]
            if c.MIN_CLOTH_MODEL_SIZE in self.params:
                min_size = self.params[c.MIN_CLOTH_MODEL_SIZE_KEY]
            if c.NECK_HEIGHT_KEY in self.params:
                neck_pct_height = self.params[c.NECK_HEIGHT_KEY]
            if c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY in self.params:
                use_dom_color = self.params[
                    c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY]
            if c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY in self.params:
                use_mean_x = self.params[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]
            if c.CLOTHING_REC_USE_3_BBOXES_KEY in self.params:
                use_3_bboxes = self.params[c.CLOTHING_REC_USE_3_BBOXES_KEY]
            if c.HIST_SMOOTHING_KERNEL_SIZE_KEY in self.params:
                kernel_size = self.params[c.HIST_SMOOTHING_KERNEL_SIZE_KEY]

        min_x = sys.maxint
        max_x = 0
        mean_x = 0
        if use_mean_x:

            # Calculate mean position of face in x axis
            for frame_dict in frame_list:

                detected = frame_dict[c.DETECTED_KEY]

                if detected:

                    face_bbox = frame_dict[c.DETECTION_BBOX_KEY]
                    face_x = face_bbox[0]

                    if face_x < min_x:
                        min_x = face_x

                    if face_x > max_x:
                        max_x = face_x

            mean_x = int((max_x + min_x) / 2.0)

        for frame_dict in frame_list:

            detected = frame_dict[c.DETECTED_KEY]

            # Consider only detected faces
            if detected:

                frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                frame_path = os.path.join(self.frames_path, frame_name)

                face_bbox = frame_dict[c.DETECTION_BBOX_KEY]

                face_x = face_bbox[0]
                face_y = face_bbox[1]
                face_width = face_bbox[2]
                face_height = face_bbox[3]

                if use_3_bboxes:

                    frame_hists = []

                    im = cv2.imread(frame_path)

                    # Width of whole bounding box
                    clothes_whole_width = (face_width * cl_pct_width)

                    # Width of single cell
                    clothes_width = int(clothes_whole_width / 3.0)
                    clothes_height = int(face_height * cl_pct_height)

                    # Leftmost bounding box for clothes
                    clothes_x0 = int(
                        face_x + face_width / 2.0 - 1.5 * clothes_width)

                    # Bounding box cannot start out of image
                    if clothes_x0 < 0:
                        if all_bboxes_in_frames:
                            return None
                        else:
                            continue

                    clothes_y0 = int(
                        face_y + face_height + (
                            face_height * neck_pct_height))

                    clothes_y1 = clothes_y0 + clothes_height

                    # Clothing bounding box must be
                    # entirely contained by the frame
                    height, width, depth = im.shape

                    if ((clothes_y1 > height) or
                            ((clothes_x0 + clothes_whole_width) > width)):
                        if all_bboxes_in_frames:
                            return None
                        else:
                            continue

                    for i in range(0, 3):

                        if i == 1:
                            # Central bounding box for clothes
                            clothes_x0 += clothes_width

                        elif i == 2:
                            # Rightmost bounding box for clothes
                            clothes_x0 += clothes_width

                        clothes_x1 = clothes_x0 + clothes_width

                        # Get region of interest for clothes

                        roi = im[clothes_y0:clothes_y1, clothes_x0:clothes_x1]

                        # TODO DELETE - TEST ONLY
                        # cv2.rectangle(im, (clothes_x0, clothes_y0),
                        #               (clothes_x1, clothes_y1), (0, 0, 255))
                        # cv2.imshow('im', im)
                        # cv2.waitKey(0)

                        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                        hists = []

                        mask = None

                        if use_dom_color:

                            mask = utils.get_dominant_color(
                                roi_hsv, kernel_size)

                        else:

                            mask = cv2.inRange(roi_hsv,
                                               np.array((0., 60., 32.)),
                                               np.array((180., 255., 255.)))

                        for ch in range(0, hsv_channels):
                            hist = cv2.calcHist(
                                [roi_hsv], [ch], mask, [256], [0, 255])

                            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

                            hists.append(hist)

                        frame_hists.append(hists)

                    model.append(frame_hists)

                    del im

                else:

                    # Get region of interest for clothes
                    clothes_width = int(face_width * cl_pct_width)
                    clothes_height = int(face_height * cl_pct_height)
                    clothes_x0 = int(
                        face_x + face_width / 2.0 - clothes_width / 2.0)

                    if use_mean_x:
                        # Bounding box for clothes
                        # has fixed position in x axis
                        clothes_x0 = int(
                            mean_x + face_width / 2.0 - clothes_width / 2.0)

                    clothes_y0 = int(
                        face_y + face_height + (face_height * neck_pct_height))
                    clothes_x1 = clothes_x0 + clothes_width
                    clothes_y1 = clothes_y0 + clothes_height

                    # Bounding box cannot start out of image
                    if clothes_x0 < 0:
                        if all_bboxes_in_frames:
                            return None
                        else:
                            continue

                    im = cv2.imread(frame_path)

                    # Clothing bounding box must be
                    # entirely contained by the frame
                    height, width, depth = im.shape

                    if (clothes_y1 > height) or (clothes_x1 > width):
                        if all_bboxes_in_frames:
                            return None
                        else:
                            continue

                    roi = im[clothes_y0:clothes_y1, clothes_x0:clothes_x1]

                    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                    hists = []

                    if use_dom_color:

                        mask = utils.get_dominant_color(
                            roi_hsv, kernel_size)

                    else:

                        mask = cv2.inRange(roi_hsv,
                                           np.array((0., 60., 32.)),
                                           np.array((180., 255., 255.)))

                    for ch in range(0, hsv_channels):
                        hist = cv2.calcHist(
                            [roi_hsv], [ch], mask, [256], [0, 255])

                        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

                        hists.append(hist)

                    model.append(hists)

                    del im

        # Check model size
        model_size = len(model)

        if model_size >= min_size:
            return model
        else:
            return None

    def create_face_model(self, segment_dict, counter):
        """
        Create face model for one face track.

        :type segment_dict: dictionary
        :param segment_dict: video segment relative to face track

        :type counter: integer
        :param counter: counter for this model

        :rtype: FaceRecognizer
        :returns: face model
        """

        # Extract list of frames from dictionary
        frame_list = segment_dict[c.FRAMES_KEY]

        images, labels = [], []

        use_nose_pos_in_rec = c.USE_NOSE_POS_IN_RECOGNITION

        max_faces_in_model = c.MAX_FACES_IN_MODEL

        lbp_radius = c.LBP_RADIUS
        lbp_neighbors = c.LBP_NEIGHBORS
        lbp_grid_x = c.LBP_GRID_X
        lbp_grid_y = c.LBP_GRID_Y

        if self.params is not None:

            if c.USE_NOSE_POS_IN_RECOGNITION_KEY in self.params:
                use_nose_pos_in_rec = self.params[
                    c.USE_NOSE_POS_IN_RECOGNITION_KEY]

            if c.MAX_FACES_IN_MODEL_KEY in self.params:
                max_faces_in_model = self.params[c.MAX_FACES_IN_MODEL_KEY]

            if c.LBP_RADIUS_KEY in self.params:
                lbp_radius = self.params[c.LBP_RADIUS_KEY]

            if c.LBP_NEIGHBORS_KEY in self.params:
                lbp_neighbors = self.params[c.LBP_NEIGHBORS_KEY]

            if c.LBP_GRID_X_KEY in self.params:
                lbp_grid_x = self.params[c.LBP_GRID_X_KEY]

            if c.LBP_GRID_Y_KEY in self.params:
                lbp_grid_y = self.params[c.LBP_GRID_Y_KEY]

                # Check if directory with aligned faces exists
        if not (os.path.exists(self.align_path)):
            return None

            # Iterate through list of frames
        face_counter = 0
        segment_nose_pos_dict = {}
        frames_in_model = []
        for frame_dict in frame_list:

            # Check if face was detected
            detected = frame_dict[c.DETECTED_KEY]

            if detected:

                file_name = frame_dict[c.ALIGNED_FACE_FILE_NAME_KEY]
                complete_file_name = (
                    file_name + c.ALIGNED_FACE_GRAY_SUFFIX + '.png')
                aligned_file_path = os.path.join(
                    self.align_path, complete_file_name)

                face = cv2.imread(aligned_file_path, cv2.IMREAD_GRAYSCALE)

                if face is not None:

                    images.append(np.asarray(face, dtype=np.uint8))
                    labels.append(face_counter)

                    frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                    frames_in_model.append(frame_name)

                    if use_nose_pos_in_rec:
                        # Save nose position in segment dictionary
                        nose_pos = frame_dict[c.NOSE_POSITION_KEY]
                        segment_nose_pos_dict[face_counter] = nose_pos

                    face_counter += 1

                # If maximum number of faces is reached, stop adding them
                if face_counter >= max_faces_in_model:
                    print 'Warning! Maximum number of faces in model reached'
                    logger.debug(
                        'Warning! Maximum number of faces in model reached '
                        'for model with counter ' + str(counter))
                    break

        model = cv2.createLBPHFaceRecognizer(
            lbp_radius, lbp_neighbors, lbp_grid_x, lbp_grid_y)

        model.train(np.asarray(images), np.asarray(labels))

        self.frames_in_models[counter] = frames_in_model

        if use_nose_pos_in_rec:
            # Save nose positions for this segment in dictionary
            self.nose_pos_list.append(segment_nose_pos_dict)

        return model

    def delete_analysis_results(self):
        """
        Delete directory with the results of the analysis on video.
        """

        logger.debug('Deleting analysis results')

        try:

            shutil.rmtree(self.video_path)

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)
            logger.debug("I/O error({0}): {1}".format(errno, strerror))

    def delete_recognition_results(self):
        """
        Delete directory with the results of people recognition on video.
        """

        logger.debug('deleting recognition results')

        try:
            if os.path.exists(self.rec_path):
                shutil.rmtree(self.rec_path)

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)
            logger.debug("I/O error({0}): {1}".format(errno, strerror))

    def detect_faces_in_video(self):
        """
        Detect faces on analyzed video.
        It works by using list of extracted frames.
        """
        logger.debug('Executing face detection')

        use_skeletons = c.USE_SKELETONS

        if (self.params is not None) and (c.USE_SKELETONS_KEY in self.params):
            use_skeletons = self.params[c.USE_SKELETONS_KEY]

        det_loaded = False

        # Try to load YAML file with detection results
        if os.path.exists(self.det_file_path):

            print 'Loading YAML file with detection results'
            logger.debug('Loading YAML file with detection results')

            det_faces = utils.load_YAML_file(self.det_file_path)

            if det_faces:
                self.detected_faces = det_faces

                print 'YAML file with detection results loaded'
                logger.debug('YAML file with detection results loaded')

                det_loaded = True

        if not det_loaded:

            # Check existence of frame list
            if len(self.frame_list) == 0:

                # Try to load YAML file with frame list
                if os.path.exists(self.frames_file_path):

                    print 'Loading YAML file with frame list'
                    logger.debug('Loading YAML file with frame list')

                    f_list = utils.load_YAML_file(self.frames_file_path)

                    if f_list:

                        self.frame_list = f_list

                        print 'YAML file with frame list loaded'
                        logger.debug('YAML file with frame list loaded')

                    else:

                        print 'Warning! Error in loading file!'
                        logger.warning('Error in loading file!')

                else:

                    print 'Warning! No frame list found!'
                    logger.warning('No frame list found!')

                    return

            print '\n\n### Face detection ###\n'
            logger.debug('\n\n### Face detection ###\n')

            # Save processing time
            start_time = cv2.getTickCount()

            if not (os.path.exists(self.det_path)):
                # Create directory for this video

                os.makedirs(self.det_path)

            if not (os.path.exists(self.align_path)):
                # Create directory with aligned faces

                os.makedirs(self.align_path)
                os.chmod(self.align_path, 0o777)  # TODO TO BE DELETED?

            frame_counter = 0
            self.detected_faces = []

            detection_results = []

            # Build list of frame names, frame paths and elapsed time
            frame_name_list = []

            frame_path_list = []

            elapsed_s_list = []

            for frame_dict in self.frame_list:
                frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                frame_name_list.append(frame_name)

                frame_path = os.path.join(self.frames_path, frame_name)

                frame_path_list.append(frame_path)

                elapsed_s = frame_dict[c.ELAPSED_VIDEO_TIME_KEY]

                elapsed_s_list.append(elapsed_s)

            if use_skeletons:

                # TODO REVIEW
                params = zip(frame_path_list,
                             (self.align_path,) * len(frame_path_list),
                             (self.params,) * len(frame_path_list),
                             (False,) * len(frame_path_list))

                print params

                # seq = Seq(fd._detect_faces_in_image)
                # farm = Farm(seq)
                # detection_results = Executor().eval(farm, params)

            else:

                # Iterate through frame paths in list
                for frame_path in frame_path_list:
                    self.progress = 100 * (frame_counter / self.saved_frames)

                    print('progress: ' + str(self.progress) + ' %          \r'),

                    detection_result = fd.detect_faces_in_image(
                        frame_path, self.align_path, self.params, False)

                    detection_results.append(detection_result)

                    frame_counter += 1

            frame_counter = 0

            # Iterate through detection results
            for detection_result in detection_results:

                detection_error = detection_result[c.ERROR_KEY]

                detection_dict = {
                    c.SAVED_FRAME_NAME_KEY: frame_name_list[frame_counter],
                    c.FRAME_COUNTER_KEY: frame_counter}

                elapsed_s = elapsed_s_list[frame_counter]

                detection_dict[c.ELAPSED_VIDEO_TIME_KEY] = elapsed_s

                faces = []
                if not detection_error:

                    det_faces = detection_result[c.FACES_KEY]

                    for det_face in det_faces:

                        face_dict = {c.BBOX_KEY: det_face[c.BBOX_KEY],
                                     c.LEFT_EYE_POS_KEY: (
                                         det_face[c.LEFT_EYE_POS_KEY]),
                                     c.RIGHT_EYE_POS_KEY: (
                                         det_face[c.RIGHT_EYE_POS_KEY]),
                                     c.NOSE_POSITION_KEY: (
                                         det_face[c.NOSE_POSITION_KEY]),
                                     c.ALIGNED_FACE_FILE_NAME_KEY: (
                                         det_face[c.ALIGNED_FACE_FILE_NAME_KEY])}

                        faces.append(face_dict)

                detection_dict[c.FACES_KEY] = faces

                self.detected_faces.append(detection_dict)

                frame_counter += 1

            # Save detection results in YAML file

            utils.save_YAML_file(self.det_file_path, self.detected_faces)

            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for face detection: ', time_in_seconds, 's\n'
            logger.debug('Time for face detection: ', time_in_seconds, 's\n')

            self.anal_times[c.FACE_DETECTION_TIME_KEY] = time_in_seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def divide_segment_by_face(self, segment_frame_list):
        """
        Divide segment accordingly to face change

        :type segment_frame_list: list
        :param segment_frame_list: list of frames in segment

        :rtype: list
        :returns: new segments
        """

        # List with histogram differences between consecutive frames
        diff_list = []

        # List with histogram differences between consecutive detections
        det_diff_list = []

        # List that will contain new lists of frames
        sub_segment_list = []

        prev_hists = None

        frame_counter = 0

        det_counter = 0

        # Dictionary for storing correspondence between counter
        counter_dict = {}

        for frame_dict in segment_frame_list:

            sim = frame_dict[c.DETECTED_KEY]

            if sim:

                # Tracking window corresponds to detected face
                frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                frame_path = os.path.join(self.frames_path, frame_name)

                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                bbox = frame_dict[c.DETECTION_BBOX_KEY]

                x0 = bbox[0]
                y0 = bbox[1]
                w = bbox[2]
                h = bbox[3]
                x1 = x0 + w
                y1 = y0 + h

                face = image[y0:y1, x0:x1]

                [tot_diff, prev_hists] = utils.get_hist_difference(
                    face, prev_hists)

                if tot_diff is not None:

                    det_diff_list.append(tot_diff)

                    diff_list.append(tot_diff)

                    counter_dict[det_counter] = frame_counter

                    det_counter += 1

                else:

                    diff_list.append(-1)

                del image

            else:

                diff_list.append(-1)

            frame_counter += 1

        segment_divided = False

        if len(det_diff_list) > 0:

            half_window_size = c.HALF_WINDOW_SIZE

            std_mult_face = c.STD_MULTIPLIER_FACE

            if self.params is not None:

                if c.HALF_WINDOW_SIZE_KEY in self.params:
                    half_window_size = self.params[c.HALF_WINDOW_SIZE_KEY]

                if c.STD_MULTIPLIER_FACE_KEY in self.params:
                    std_mult_face = self.params[c.STD_MULTIPLIER_FACE_KEY]

            face_cut_idxs_temp = utils.get_shot_changes(
                det_diff_list, half_window_size, std_mult_face)

            if len(face_cut_idxs_temp) > 0:

                segment_divided = True

                # Get real counters
                face_cut_idxs = []

                for idx_temp in face_cut_idxs_temp:
                    face_cut_idxs.append(counter_dict[idx_temp])

                # Counter for all frames in original segment
                counter = 0

                sub_frame_list = []

                for frame_dict in segment_frame_list:

                    if counter in face_cut_idxs:
                        sub_segment_list.append(sub_frame_list)

                        sub_frame_list = []

                    sub_frame_list.append(frame_dict)

                    counter += 1

                if len(sub_frame_list) > 0:
                    sub_segment_list.append(sub_frame_list)

        # If segment has not been divided,
        # list will contain only original segment

        if not segment_divided:
            sub_segment_list.append(segment_frame_list)

        new_segments = []

        use_or_fps = c.USE_ORIGINAL_FPS
        used_fps = c.USED_FPS
        min_detection_pct = c.MIN_DETECTION_PCT
        min_segment_duration = c.MIN_SEGMENT_DURATION

        if self.params is not None:

            if c.USE_ORIGINAL_FPS_KEY in self.params:
                use_or_fps = self.params[c.USE_ORIGINAL_FPS_KEY]

            if c.USED_FPS_KEY in self.params:
                used_fps = self.params[c.USED_FPS_KEY]

            if c.MIN_DETECTION_PCT_KEY in self.params:
                min_detection_pct = self.params[c.MIN_DETECTION_PCT_KEY]

            if c.MIN_SEGMENT_DURATION_KEY in self.params:
                min_segment_duration = self.params[c.MIN_SEGMENT_DURATION_KEY]

                # Minimum duration of a segment in frames
        min_segment_frames = int(
            math.ceil(self.fps * min_segment_duration))

        # If a reduced frame rate is used, frames are less
        if not use_or_fps:
            min_segment_frames = int(
                math.ceil((used_fps + 1) * min_segment_duration))

            # Iterate through new sub segments
        for sub_frame_list in sub_segment_list:

            frame_counter = len(sub_frame_list)

            segment_dict = {c.FRAMES_KEY: sub_frame_list,
                            c.SEGMENT_TOT_FRAMES_NR_KEY: frame_counter}

            # Segment duration in milliseconds

            duration = frame_counter * 1000.0 / self.fps

            # If a reduced frame rate is used, frames are less

            if not use_or_fps:
                duration = frame_counter * 1000.0 / (used_fps + 1)

            segment_dict[c.SEGMENT_DURATION_KEY] = duration

            segment_dict[c.ASSIGNED_TAG_KEY] = c.UNDEFINED_TAG

            segment_dict[c.CONFIDENCE_KEY] = -1

            # Segment must be considered only if its number
            # of frames is greater or equals than a minimum
            if frame_counter >= min_segment_frames:

                # Start of segment in millisecond
                first_frame_dict = sub_frame_list[0]

                segment_start = first_frame_dict[c.ELAPSED_VIDEO_TIME_KEY]

                segment_dict[c.SEGMENT_START_KEY] = segment_start

                # Counter for frames with detections in new segment
                det_counter = 0

                for frame_dict in sub_frame_list:

                    sim = frame_dict[c.DETECTED_KEY]

                    if sim:
                        det_counter += 1

                # Check percentage of detection
                det_pct = (float(det_counter) / frame_counter)

                # print('det_pct', det_pct)

                if det_pct >= min_detection_pct:

                    new_segments.append(segment_dict)

                else:

                    self.disc_tracked_faces.append(segment_dict)
            else:

                self.disc_tracked_faces.append(segment_dict)

        return new_segments

    def get_faces_nr(self):
        """
        Get number of faces in each frame,
        saving results in self.faces_nr.
        It works by using list of tracked faces.
        """

        logger.debug('Getting number of faces in each frame')

        if len(self.tracked_faces) == 0:

            # Try to load YAML file

            if os.path.exists(self.track_path):

                print 'Loading YAML file with tracking results'
                logger.debug('Loading YAML file with tracking results')

                with open(self.track_path) as f:

                    self.tracked_faces = yaml.load(f)

                print 'YAML file with tracking results loaded'
                logger.debug('YAML file with tracking results loaded')

            else:

                print 'Warning! No tracking results found!'
                logger.warning('No tracking results found!')

                return

        self.faces_nr = {}

        for segment_dict in self.tracked_faces:

            frame_list = segment_dict[c.FRAMES_KEY]

            for frame_dict in frame_list:

                frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                if frame_name in self.faces_nr:

                    self.faces_nr[frame_name] += 1

                else:

                    self.faces_nr[frame_name] = 1

                    # Save YAML file

        utils.save_YAML_file(self.faces_nr_path, self.faces_nr)

    def get_frame_list(self):
        """
        Get and save frames from the video resource.
        """

        logger.debug('Executing frame extraction')

        frames_loaded = False

        # Try to load YAML file with frame list
        if os.path.exists(self.frames_file_path):

            print 'Loading YAML file with frame list'
            logger.debug('Loading YAML file with frame list')

            f_list = utils.load_YAML_file(self.frames_file_path)

            if f_list:
                self.frame_list = f_list

                print 'YAML file with frame_list loaded'
                logger.debug('YAML file with frame_list loaded')

                frames_loaded = True

        if not frames_loaded:

            print '\n\n### Frame extraction ###\n'
            logger.debug('\n\n### Frame extraction ###\n')

            # Save processing time
            start_time = cv2.getTickCount()

            if not (os.path.exists(self.frames_path)):
                os.makedirs(self.frames_path)

                # Counter for all frames
            frame_counter = 0

            # Value of frame_counter for last analyzed frame
            last_anal_frame = 0

            # Open video file
            capture = cv2.VideoCapture(self.resource_path)

            self.frame_list = []

            # Save parameters for this video
            param_dict = {}

            if capture is None or not capture.isOpened():

                error = 'Error in opening video file'

                print error
                logger.debug(error)

                return

            else:

                video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)

                param_dict[c.VIDEO_FPS_KEY] = video_fps

                # Original number of frames
                tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

                param_dict[c.VIDEO_TOT_FRAMES_KEY] = tot_frames

                self.fps = video_fps

                self.video_frames = float(tot_frames)

                # Saved frames
                saved_frames = 0

                # Set parameters
                used_fps = c.USED_FPS
                use_or_fps = c.USE_ORIGINAL_FPS
                use_or_res = c.USE_ORIGINAL_RES
                used_res_scale_factor = c.USED_RES_SCALE_FACTOR

                if self.params is not None:
                    if c.USED_FPS_KEY in self.params:
                        used_fps = self.params[c.USED_FPS_KEY]
                    if c.USE_ORIGINAL_FPS_KEY in self.params:
                        use_or_fps = self.params[c.USE_ORIGINAL_FPS_KEY]
                    if c.USE_ORIGINAL_RES_KEY in self.params:
                        use_or_res = self.params[c.USE_ORIGINAL_RES_KEY]
                    if c.USED_RES_SCALE_FACTOR_KEY in self.params:
                        used_res_scale_factor = self.params[
                            c.USED_RES_SCALE_FACTOR_KEY]

                if used_fps == 0:
                    print('Warning! Frame rate cannot be zero!')
                    logger.warning('Frame rate cannot be zero')
                    return

                while True:

                    # Read frame
                    ret, frame = capture.read()

                    # If no frame is read, abort
                    if not ret:
                        break

                    # Next frame to be analyzed
                    next_frame = last_anal_frame + (video_fps / used_fps) - 1

                    if use_or_fps or (frame_counter > next_frame):

                        # Frame position in video in milliseconds
                        elapsed_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)

                        # print 'elapsed video s =', elapsed_video_s

                        fr_name = '%07d.png' % frame_counter

                        frame_path = os.path.join(self.frames_path, fr_name)

                        # Resize frame
                        if not use_or_res:
                            fx = used_res_scale_factor

                            fy = used_res_scale_factor

                            interp = cv2.INTER_AREA

                            frame = cv2.resize(src=frame, dsize=(0, 0),
                                               fx=fx, fy=fy,
                                               interpolation=interp)

                        cv2.imwrite(frame_path, frame,
                                    [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                        frame_dict = {c.SAVED_FRAME_NAME_KEY: fr_name,
                                      c.ELAPSED_VIDEO_TIME_KEY: int(elapsed_ms)}

                        self.frame_list.append(frame_dict)

                        last_anal_frame = frame_counter

                        saved_frames += 1

                    frame_counter += 1

                    self.progress = 100 * (frame_counter / self.video_frames)

                    print('progress: ' + str(self.progress) + ' %      \r'),

            del capture

            self.saved_frames = float(saved_frames)

            param_dict[c.VIDEO_SAVED_FRAMES_KEY] = self.saved_frames

            # Save frame list in YAML file
            utils.save_YAML_file(self.frames_file_path, self.frame_list)

            # Save video parameters in YAML file

            utils.save_YAML_file(self.params_file_path, param_dict)

            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for frame extraction:', str(time_in_seconds), 's\n'
            logger.debug(
                'Time for frame extraction:', str(time_in_seconds), 's\n')

            self.anal_times[c.FRAME_EXTRACTION_TIME_KEY] = time_in_seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def get_people(self):
        """
        Get list of people detected in video

        :rtype: list
        :returns: list of people detected in video
        """

        logger.debug('Getting list of people detected in video')

        result = self.recognized_faces

        if len(result) == 0:

            # Try to load YAML file with recognition results
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'
                logger.debug('Loading YAML file with recognition results')

                rec_faces = utils.load_YAML_file(self.rec_file_path)

                if rec_faces:
                    print 'YAML file with recognition results loaded'
                    logger.debug('YAML file with recognition results loaded')

                    result = rec_faces

        return result

    def get_person_counter(self, tag_id):
        """
        Get identifier in video of person corresponding to given tag identifier

        :type tag_id: integer
        :param tag_id: tag identifier

        :rtype: integer or None
        :returns: identifier in video of person corresponding to given
        tag identifier
        """

        logger.debug('Getting person counter for tag id ' + str(tag_id))

        person_counter = None

        # Check existence of recognition results
        if len(self.recognized_faces) == 0:

            # Try to load YAML file
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'
                logger.debug('Loading YAML file with recognition results')

                with open(self.rec_file_path) as f:

                    self.recognized_faces = yaml.load(f)

                print 'YAML file with recognition results loaded'
                logger.debug('YAML file with recognition results loaded')

            else:

                print 'Warning! No recognition results found!'
                logger.warning('No recognition results found!')

                return

        for person_dict in self.recognized_faces:

            person_tag_id = person_dict[c.TAG_ID_KEY]

            if person_tag_id == tag_id:
                person_counter = person_dict[c.PERSON_COUNTER_KEY]
                return person_counter

        return person_counter

    def merge_consecutive_segments(self):
        """
        Merge consecutive video segments belonging to the same person
        """

        # Get minimum segment duration
        min_duration = c.MIN_SEGMENT_DURATION

        if ((self.params is not None) and
                (c.MIN_SEGMENT_DURATION_KEY in self.params)):
            min_duration = self.params[c.MIN_SEGMENT_DURATION_KEY]

        for person_dict in self.recognized_faces:

            segments = person_dict[c.SEGMENTS_KEY]

            (merged_segments, tot_dur) = utils.merge_consecutive_segments(
                segments, min_duration)

            person_dict[c.SEGMENTS_KEY] = merged_segments

    def merge_labels(self):
        """
        Merge people with the same label.
        """

        new_faces = []
        while len(self.recognized_faces) > 0:

            idxs_to_be_deleted = [0]  # List of indexes of items to be deleted

            first_label = self.recognized_faces[0][c.ASSIGNED_LABEL_KEY]
            # Iterate through other people clusters

            new_person_dict = copy.deepcopy(self.recognized_faces[0])

            for i in range(1, len(self.recognized_faces)):
                label = self.recognized_faces[i][c.ASSIGNED_LABEL_KEY]

                if label == first_label:
                    # Same label
                    segments = self.recognized_faces[i][c.SEGMENTS_KEY]
                    new_person_dict[c.SEGMENTS_KEY].extend(segments)
                    idxs_to_be_deleted.append(i)

            new_faces.append(new_person_dict)

            # Delete already considered people
            for i in range(0, len(idxs_to_be_deleted)):
                del self.recognized_faces[i]

        # Update list of people
        self.recognized_faces = new_faces

    def recognize_captions_in_video(self):
        """
        Recognize captions on analyzed video,
        assigning tags to faces on the basis of captions.
        It works by using a list of people clusters.
        """

        use_skeletons = c.USE_SKELETONS

        if ((self.params is not None) and
                (c.USE_SKELETONS_KEY in self.params)):
            use_skeletons = self.params[c.USE_SKELETONS_KEY]

        print '\n\n### People recognition - caption recognition ###\n'
        logger.debug('\n\n### People recognition - caption recognition ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        # Load tags
        fm = FaceModels(self.params)

        tgs = list(fm.get_tags())

        if len(tgs) > 0:

            # Try to load YAML file with number of faces in frames
            if os.path.exists(self.faces_nr_path):

                print 'Loading YAML file with number of faces in frames'
                logger.debug('Loading YAML file with number of faces in frames')

                with open(self.faces_nr_path) as f:

                    self.faces_nr = yaml.load(f)

                print 'YAML file with number of faces in frames loaded'
                logger.debug('YAML file with number of faces in frames loaded')

            else:
                # Get number of faces in each frame
                self.get_faces_nr()

            fps = c.USED_FPS
            use_or_fps = c.USE_ORIGINAL_FPS
            fps_for_captions = c.USED_FPS_FOR_CAPTIONS
            min_frames_per_caption = c.MIN_FRAMES_PER_CAPTION

            if self.params is not None:
                if c.USED_FPS_KEY in self.params:
                    fps = self.params[c.USED_FPS_KEY]
                if c.USE_ORIGINAL_FPS_KEY in self.params:
                    use_or_fps = self.params[c.USE_ORIGINAL_FPS_KEY]
                if c.USED_FPS_FOR_CAPTIONS_KEY in self.params:
                    fps_for_captions = self.params[c.USED_FPS_FOR_CAPTIONS_KEY]
                if c.MIN_FRAMES_PER_CAPTION_KEY in self.params:
                    min_frames_per_caption = self.params[
                        c.MIN_FRAMES_PER_CAPTION_KEY]

            if fps_for_captions == 0:
                print('Warning! Frame rate cannot be zero!')
                logger.warning('Frame rate cannot be zero')
                return

            if use_or_fps:
                fps = self.fps

            p_c = 0

            clusters_nr = float(len(self.recognized_faces))

            # Iterate through people clusters
            for person_dict in self.recognized_faces:

                self.progress = 100 * (p_c / clusters_nr)

                print('progress: ' + str(self.progress) + ' %          \r'),

                prev_ass_tag = person_dict[c.ASSIGNED_TAG_KEY]

                # If person is not already recognized,
                # try to recognize him/her
                if prev_ass_tag != c.UNDEFINED_TAG:

                    p_c += 1

                    continue

                frames = []

                caption_rec_results = []

                # Build list of frame paths relative to this person
                frame_path_list = []

                segment_list = person_dict[c.SEGMENTS_KEY]

                # Dictionary for storing elapsed times for each frame
                frames_dict_time = {}

                # Iterate through segments related to this person
                for segment_dict in segment_list:

                    # List of frame paths relative to this segment
                    frame_path_segment_list = []

                    frame_list = segment_dict[c.FRAMES_KEY]

                    frame_counter = 0

                    last_anal_frame = 0

                    for frame_dict in frame_list:

                        # Next frame to be analyzed
                        next_frame = (
                            last_anal_frame + (fps / fps_for_captions) - 1)

                        if frame_counter > next_frame:

                            frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                            frame_path = os.path.join(
                                self.frames_path, frame_name)

                            # Check if there is only one face in this frame
                            if ((frame_name in self.faces_nr) and
                                        (self.faces_nr[frame_name] == 1)):
                                frame_path_segment_list.append(frame_path)
                                # Store elapsed video time in dictionary
                                elapsed_s = frame_dict[c.ELAPSED_VIDEO_TIME_KEY]
                                frames_dict_time[frame_path] = elapsed_s

                            last_anal_frame = frame_counter

                        frame_counter += 1

                    frame_path_list.append(frame_path_segment_list)

                # Execute caption recognition
                if use_skeletons:

                    # TODO REVIEW
                    pass

                else:

                    # Iterate through frame paths in list
                    for frame_path_segment_list in frame_path_list:
                        segment_caption_rec_results = []

                        for frame_path in frame_path_segment_list:
                            result_dict = get_tag_from_image(
                                frame_path, self.params)
                            elapsed_s = frames_dict_time[frame_path]
                            result_dict[c.ELAPSED_VIDEO_TIME_KEY] = elapsed_s
                            segment_caption_rec_results.append(result_dict)

                        caption_rec_results.append(segment_caption_rec_results)

                for segment_caption_rec_results in caption_rec_results:

                    # Dictionary for storing confidences for each found tag
                    tags_dict_conf = {}

                    # Dictionary for storing elapsed times for each found tag
                    tags_dict_time = {}

                    for result_dict in segment_caption_rec_results:

                        ass_tag = result_dict[c.ASSIGNED_TAG_KEY]

                        # TEST ONLY
                        # print('assigned tag', ass_tag)

                        if ass_tag != c.UNDEFINED_TAG:

                            conf = result_dict[c.CONFIDENCE_KEY]
                            elapsed_s = result_dict[c.ELAPSED_VIDEO_TIME_KEY]

                            if ass_tag in tags_dict_conf:
                                tags_dict_conf[ass_tag].append(conf)
                                tags_dict_time[ass_tag].append(elapsed_s)
                            else:
                                tags_dict_conf[ass_tag] = [conf]
                                tags_dict_time[ass_tag] = [elapsed_s]

                    # Iterate through found tags
                    for ass_tag in tags_dict_conf.keys():
                        # Only tags found in at least
                        # min_frames_per_caption frames are considered
                        if (len(tags_dict_conf[ass_tag]) >=
                                min_frames_per_caption):

                            # Iterate through frames in which ass_tag was found
                            for conf in tags_dict_conf[ass_tag]:
                                # Compose frame
                                frame_dict = {c.CONFIDENCE_KEY: conf,
                                              c.ASSIGNED_TAG_KEY: ass_tag}
                                frames.append(frame_dict)

                # Assign final label (and relative tag) to person
                label = c.UNDEFINED_LABEL
                tag = c.UNDEFINED_TAG

                if len(frames) > 0:
                    [final_tag, final_conf, pct] = (
                        utils.aggregate_frame_results(
                            frames, None, tags=tgs, params=self.params))

                    # Get label corresponding to tag
                    # (only tags corresponding to one label are considered)
                    labels = fm.get_labels_for_tag(final_tag)

                    if len(labels) == 1:
                        label = labels[0]
                        tag = final_tag

                        # Get time instants related to this tag
                        time_instants = tags_dict_time[tag]
                        min_sep = 1500.0 / fps_for_captions

                        # Get time intervals when captions
                        # for this tag are shown and save them
                        time_intervals = utils.get_time_intervals(
                            time_instants, min_sep)
                        caption_segments = []
                        for time_interval in time_intervals:
                            start = time_interval[0]
                            duration = time_interval[1]
                            caption_segment_dict = {
                                c.SEGMENT_START_KEY: start,
                                c.SEGMENT_DURATION_KEY: duration}
                            caption_segments.append(caption_segment_dict)
                        self.recognized_faces[p_c][c.CAPTION_SEGMENTS_KEY] = (
                            caption_segments)

                self.recognized_faces[p_c][c.ASSIGNED_LABEL_KEY] = label
                self.recognized_faces[p_c][c.ASSIGNED_TAG_KEY] = tag
                self.recognized_faces[p_c][c.CAPTION_ASSIGNED_LABEL_KEY] = label
                self.recognized_faces[p_c][c.CAPTION_ASSIGNED_TAG_KEY] = tag

                p_c += 1

            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for caption recognition:', seconds, 's\n'
            logger.debug('Time for caption recognition:', seconds, 's\n')

            self.anal_times[c.CAPTION_RECOGNITION_TIME_KEY] = seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def recognize_faces_in_video(self):
        """
        Recognize faces on analyzed video,
        assigning tags to faces on the basis of face features.
        It works by using a list of people clusters.
        """

        use_skeletons = c.USE_SKELETONS

        if ((self.params is not None) and
                (c.USE_SKELETONS_KEY in self.params)):
            use_skeletons = self.params[c.USE_SKELETONS_KEY]

        print '\n\n### People recognition - face recognition ###\n'
        logger.debug('\n\n### People recognition - face recognition ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        # Load face models
        fm = FaceModels(self.params)

        tgs = list(fm.get_labels())

        loaded = fm.load_models()

        if loaded:

            p_counter = 0

            clusters_nr = float(len(self.recognized_faces))

            logger.debug('clusters_nr: ' + str(clusters_nr))

            # Iterate through people clusters
            for person_dict in self.recognized_faces:

                self.progress = 100 * (p_counter / clusters_nr)

                print('progress: ' + str(self.progress) + ' %          \r'),

                prev_ass_label = c.UNDEFINED_LABEL
                if c.ASSIGNED_LABEL_KEY in person_dict:
                    prev_ass_label = person_dict[c.ASSIGNED_LABEL_KEY]

                # If person is not already recognized,
                # try to recognize him/her
                if prev_ass_label != c.UNDEFINED_LABEL:

                    p_counter += 1

                    continue

                frames = []

                face_rec_results = []

                # Build list of image paths
                im_path_list = []

                segment_list = person_dict[c.SEGMENTS_KEY]

                # Iterate through segments related to this person
                for segment_dict in segment_list:

                    frame_list = segment_dict[c.FRAMES_KEY]

                    for frame_dict in frame_list:

                        # Check if face was detected
                        detected = frame_dict[c.DETECTED_KEY]

                        if detected:

                            file_name = frame_dict[c.ALIGNED_FACE_FILE_NAME_KEY]
                            complete_file_name = (
                                file_name + c.ALIGNED_FACE_GRAY_SUFFIX + '.png')
                            aligned_file_path = os.path.join(
                                self.align_path, complete_file_name)

                            im_path_list.append(aligned_file_path)

                # Execute face recognition

                # TEST ONLY
                # print('im_path_list', im_path_list)
                if use_skeletons:

                    # TODO REVIEW
                    pass

                else:

                    # Iterate through frame paths in list
                    for im_path in im_path_list:

                        face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

                        (frame_label, conf) = fm.recognize_face(face)

                        result_dict = {c.ASSIGNED_TAG_KEY: frame_label,
                                       c.CONFIDENCE_KEY: conf}

                        face_rec_results.append(result_dict)

                for result_dict in face_rec_results:

                    ass_label = result_dict[c.ASSIGNED_TAG_KEY]

                    conf = result_dict[c.CONFIDENCE_KEY]

                    logger.debug('assigned label', ass_label)

                    # Compose frame

                    if ass_label != c.UNDEFINED_LABEL:
                        frame_dict = {c.CONFIDENCE_KEY: conf,
                                      c.ASSIGNED_TAG_KEY: ass_label}

                        frames.append(frame_dict)

                # Assign final tag to person

                label = c.UNDEFINED_LABEL
                tag = c.UNDEFINED_TAG

                if len(frames) > 0:
                    [final_label, final_conf, pct] = (
                        utils.aggregate_frame_results(
                            frames, None, tags=tgs, params=self.params))

                    label = final_label
                    tag = fm.get_tag(label)

                print('p_counter', p_counter)
                print('frames', frames)
                print('assigned final tag', tag)
                logger.debug('assigned final tag', tag)

                self.recognized_faces[p_counter][c.ASSIGNED_LABEL_KEY] = label
                self.recognized_faces[p_counter][c.ASSIGNED_TAG_KEY] = tag

                p_counter += 1

            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for face recognition:', seconds, 's\n'
            logger.debug('Time for face recognition:', seconds, 's\n')

            self.anal_times[c.CAPTION_RECOGNITION_TIME_KEY] = seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)


    def recognize_people_in_video(self):
        """
        Recognize people on analyzed video, assigning tags to faces.
        It works by using a list of people clusters.
        """

        logger.debug('Executing people recognition')

        rec_loaded = False

        # Try to load YAML file with recognition results
        if os.path.exists(self.rec_file_path):

            print 'Loading YAML file with recognition results'
            logger.debug('Loading YAML file with recognition results')

            rec_faces = utils.load_YAML_file(self.rec_file_path)

            if rec_faces:
                self.recognized_faces = rec_faces

                print 'YAML file with recognition results loaded'
                logger.debug('YAML file with recognition results loaded')

                rec_loaded = True

        if not rec_loaded:

            # Check existence of clustering results
            if len(self.recognized_faces) == 0:

                # Try to load YAML file with clustering results
                if os.path.exists(self.cluster_file_path):

                    print 'Loading YAML file with clustering results'
                    logger.debug('Loading YAML file with clustering results')

                    with open(self.cluster_file_path) as f:

                        self.recognized_faces = yaml.load(f)

                    print 'YAML file with clustering results loaded'
                    logger.debug('YAML file with clustering results loaded')

                else:

                    print 'Warning! No clustering results found!'
                    logger.warning('No clustering results found!')

                    return

            use_caption_rec = c.USE_CAPTION_RECOGNITION
            use_face_rec = c.USE_FACE_RECOGNITION
            if self.params:
                if c.USE_CAPTION_RECOGNITION_KEY in self.params:
                    use_caption_rec = self.params[c.USE_CAPTION_RECOGNITION_KEY]
                if c.USE_FACE_RECOGNITION_KEY in self.params:
                    use_face_rec = self.params[c.USE_FACE_RECOGNITION_KEY]

            if use_caption_rec:
                # Caption recognition
                self.recognize_captions_in_video()

            if use_face_rec:
                # Face recognition
                self.recognize_faces_in_video()

            # Merge people with the same label
            # self.merge_labels() TODO UNCOMMENT FOR LANTANIO

            # Merge consecutive video segments belonging to the same person
            # self.merge_consecutive_segments() TODO UNCOMMENT FOR LANTANIO

            self.calculate_medoids()

            if not (os.path.exists(self.rec_path)):
                # Create directory for people recognition
                os.makedirs(self.rec_path)

                # Save recognition result in YAML file
            utils.save_YAML_file(self.rec_file_path, self.recognized_faces)

    def save_analysis_results(self):
        """
        Save results of analysis in self.anal_results dictionary
        """

        logger.debug('Saving analysis results')

        segments_nr = len(self.tracked_faces)
        self.anal_results[c.SEGMENTS_NR_KEY] = segments_nr

        people_clusters_nr = len(self.recognized_faces)
        self.anal_results[c.PEOPLE_CLUSTERS_NR_KEY] = people_clusters_nr

        # Count relevant tags
        relevant_people_nr = 0
        for person_dict in self.recognized_faces:

            tag = person_dict[c.ASSIGNED_TAG_KEY]

            if tag != c.UNDEFINED_TAG:
                relevant_people_nr += 1

        self.anal_results[c.RELEVANT_PEOPLE_NR_KEY] = relevant_people_nr

    def save_cloth_models(self, segments):
        """
        Save cloth models for each tracked face

        :type segments: list
        :param segments: list of segments
        """

        print '\n\n### Creating cloth models ###\n'
        logger.debug('\n\n### Creating cloth models ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        if not (os.path.exists(self.cloth_models_path)):
            os.makedirs(self.cloth_models_path)

            # Calculate and save cloth models for each face track

        counter = 0

        for segment_dict in segments:
            model = self.create_cloth_model(segment_dict)

            db_path = os.path.join(self.cloth_models_path, str(counter))

            with open(db_path, 'w') as f:
                pk.dump(model, f)

            counter += 1

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()

        print 'Time for calculating cloth models:', str(time_in_seconds), 's\n'
        logger.debug(
            'Time for calculating cloth models:', str(time_in_seconds), 's\n')

        self.anal_times[c.CLOTH_MODELS_CREATION_TIME_KEY] = time_in_seconds

        utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def save_disc_tracking_segments(self):
        """
        Save frames from discarded tracking segments on disk.
        A folder contains the frames from one segment
        """

        print '\n\n### Saving discarded tracking segments ###\n'
        logger.debug('\n\n### Saving discarded tracking segments ###\n')

        segments_path = os.path.join(
            self.track_path, c.FACE_TRACKING_SEGMENTS_DIR)

        segments_path += '_discarded'

        # Delete already saved files
        if os.path.exists(segments_path):

            images_dirs = os.listdir(segments_path)

            for images_dir in images_dirs:
                images_dir_path = os.path.join(segments_path, images_dir)
                shutil.rmtree(images_dir_path)

        disc_tracked_faces_nr = float(len(self.disc_tracked_faces))

        segment_counter = 0

        for segment_dict in self.disc_tracked_faces:

            self.progress = 100 * (segment_counter / disc_tracked_faces_nr)

            print('progress: ' + str(self.progress) + ' %          \r'),

            segment_frame_list = segment_dict[c.FRAMES_KEY]

            segment_path = os.path.join(
                segments_path, str(segment_counter))

            if not (os.path.exists(segment_path)):
                os.makedirs(segment_path)

            image_counter = 0

            for segment_frame_dict in segment_frame_list:

                frame_name = segment_frame_dict[c.SAVED_FRAME_NAME_KEY]

                frame_path = os.path.join(self.frames_path, frame_name)

                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                # Add tracking window to image as red rectangle
                track_bbox = segment_frame_dict[c.TRACKING_BBOX_KEY]

                x0 = track_bbox[0]
                x1 = x0 + track_bbox[2]
                y0 = track_bbox[1]
                y1 = y0 + track_bbox[3]

                cv2.rectangle(
                    image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                # Add detection bbox to image as blue rectangle
                det_bbox = segment_frame_dict[c.DETECTION_BBOX_KEY]

                if det_bbox is not None:
                    x0 = det_bbox[0]
                    x1 = x0 + det_bbox[2]
                    y0 = det_bbox[1]
                    y1 = y0 + det_bbox[3]

                    cv2.rectangle(
                        image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)

                file_name = '%07d.png' % image_counter

                face_path = os.path.join(segment_path, file_name)

                cv2.imwrite(face_path, image,
                            [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                del image

                image_counter += 1

            segment_counter += 1

    def save_face_models(self, segments):
        """
        Save face models for each tracked face

        :type segments: list
        :param segments: list of segments
        """

        print '\n\n### Creating face models ###\n'
        logger.debug('\n\n### Creating face models ###\n')

        # Save processing time
        start_time = cv2.getTickCount()

        if not (os.path.exists(self.face_models_path)):
            os.makedirs(self.face_models_path)

        counter = 0

        self.nose_pos_list = []

        for segment_dict in segments:
            model = self.create_face_model(segment_dict, counter)

            db_path = os.path.join(self.face_models_path, str(counter))

            model.save(db_path)

            counter += 1

        # Save nose positions
        with open(self.nose_pos_file_path, 'w') as f:

            pk.dump(self.nose_pos_list, f)

            # Save in YAML file list of frames in models
        utils.save_YAML_file(
            self.frames_in_models_file_path, self.frames_in_models)

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()

        print 'Time for calculating face models:', str(time_in_seconds), 's\n'
        logger.debug(
            'Time for calculating face models:', str(time_in_seconds), 's\n')

        self.anal_times[c.FACE_MODELS_CREATION_TIME_KEY] = time_in_seconds

        utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def save_people_files(self):
        """
        Save annotation files for people in this video
        """

        # Check existence of recognition results
        if len(self.recognized_faces) == 0:

            # Try to load YAML file
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'

                with open(self.rec_file_path) as f:

                    self.recognized_faces = yaml.load(f)

                print 'YAML file with recognition results loaded'

            else:

                print 'Warning! No recognition results found!'

                return

        # Delete already saved files
        if os.path.exists(self.compl_ann_path):

            ann_files = os.listdir(self.compl_ann_path)

            for ann_file in ann_files:
                ann_file_path = os.path.join(self.compl_ann_path, ann_file)
                os.remove(ann_file_path)

        else:

            os.makedirs(self.compl_ann_path)

            # Delete already saved files
        if os.path.exists(self.simple_ann_path):

            ann_files = os.listdir(self.simple_ann_path)

            for ann_file in ann_files:
                ann_file_path = os.path.join(self.simple_ann_path, ann_file)
                os.remove(ann_file_path)

        else:

            os.makedirs(self.simple_ann_path)

        # Save unique tags
        tags = []

        for person_dict in self.recognized_faces:

            ann_tag = person_dict[c.ASSIGNED_TAG_KEY]

            if (ann_tag != c.UNDEFINED_TAG) and (ann_tag not in tags):
                tags.append(ann_tag)

        for tag in tags:

            # Create complete annotations
            person_dict = {}

            # Create simple annotations
            simple_dict = {c.ANN_TAG_KEY: tag}

            person_dict[c.ANN_TAG_KEY] = tag

            segment_list = []

            simple_segment_list = []

            cap_segment_list = []

            simple_cap_segment_list = []

            tot_dur = 0
            cap_tot_dur = 0

            # Iterate through all recognized people in video
            for temp_person_dict in self.recognized_faces:

                ann_tag = temp_person_dict[c.ASSIGNED_TAG_KEY]

                if ann_tag == tag:

                    # Save video segments
                    temp_segment_list = temp_person_dict[c.SEGMENTS_KEY]

                    for segment_dict in temp_segment_list:
                        segment_list.append(segment_dict)

                        simple_seg_dict = {}

                        start = segment_dict[c.SEGMENT_START_KEY]

                        simple_seg_dict[c.SEGMENT_START_KEY] = start

                        dur = segment_dict[c.SEGMENT_DURATION_KEY]

                        tot_dur = tot_dur + dur

                        simple_seg_dict[c.SEGMENT_DURATION_KEY] = dur

                        simple_segment_list.append(simple_seg_dict)

                    # Save caption segments
                    temp_cap_segment_list = []
                    if c.CAPTION_SEGMENTS_KEY in temp_person_dict:
                        temp_cap_segment_list = (
                            temp_person_dict[c.CAPTION_SEGMENTS_KEY])

                    for cap_segment_dict in temp_cap_segment_list:

                        cap_segment_list.append(cap_segment_dict)

                        simple_cap_seg_dict = {}

                        start = cap_segment_dict[c.SEGMENT_START_KEY]

                        simple_cap_seg_dict[c.SEGMENT_START_KEY] = start

                        dur = cap_segment_dict[c.SEGMENT_DURATION_KEY]

                        cap_tot_dur = cap_tot_dur + dur

                        simple_cap_seg_dict[c.SEGMENT_DURATION_KEY] = dur

                        simple_cap_segment_list.append(simple_cap_seg_dict)

            # Save video segments
            person_dict[c.SEGMENTS_KEY] = segment_list
            simple_dict[c.SEGMENTS_KEY] = simple_segment_list
            person_dict[c.TOT_SEGMENT_DURATION_KEY] = tot_dur
            simple_dict[c.TOT_SEGMENT_DURATION_KEY] = tot_dur

            # Save caption segments
            person_dict[c.CAPTION_SEGMENTS_KEY] = cap_segment_list
            simple_dict[c.CAPTION_SEGMENTS_KEY] = simple_cap_segment_list
            person_dict[c.TOT_CAPTION_SEGMENT_DURATION_KEY] = cap_tot_dur
            simple_dict[c.TOT_CAPTION_SEGMENT_DURATION_KEY] = cap_tot_dur

            file_name = tag + '.YAML'

            # Save complete annotations

            file_path = os.path.join(self.compl_ann_path, file_name)

            utils.save_YAML_file(file_path, person_dict)

            # Save simple annotations

            file_path = os.path.join(self.simple_ann_path, file_name)

            utils.save_YAML_file(file_path, simple_dict)

    def save_tracking_segments(self):
        """
        Save frames from tracking segments on disk.
        A folder contains the frames from one segment
        """

        print '\n\n### Saving tracking segments ###\n'

        segments_path = os.path.join(
            self.track_path, c.FACE_TRACKING_SEGMENTS_DIR)

        # Delete already saved files
        if os.path.exists(segments_path):

            images_dirs = os.listdir(segments_path)

            for images_dir in images_dirs:
                images_dir_path = os.path.join(segments_path, images_dir)
                shutil.rmtree(images_dir_path)

        tracked_faces_nr = float(len(self.tracked_faces))

        segment_counter = 0

        face_counter = 0

        for segment_dict in self.tracked_faces:

            self.progress = 100 * (segment_counter / tracked_faces_nr)

            print('progress: ' + str(self.progress) + ' %          \r'),

            segment_frame_list = segment_dict[c.FRAMES_KEY]

            segment_path = os.path.join(
                segments_path, str(segment_counter))

            if not (os.path.exists(segment_path)):
                os.makedirs(segment_path)

            image_counter = 0

            for segment_frame_dict in segment_frame_list:

                frame_name = segment_frame_dict[c.SAVED_FRAME_NAME_KEY]

                frame_path = os.path.join(self.frames_path, frame_name)

                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                # Add tracking window to image as red rectangle
                track_bbox = segment_frame_dict[c.TRACKING_BBOX_KEY]

                x0 = track_bbox[0]
                x1 = x0 + track_bbox[2]
                y0 = track_bbox[1]
                y1 = y0 + track_bbox[3]

                # Used to save face images
                image_copy = copy.copy(image)

                cv2.rectangle(
                    image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                # Add detection bbox to image as blue rectangle
                det_bbox = segment_frame_dict[c.DETECTION_BBOX_KEY]

                if det_bbox is not None:
                    x0 = det_bbox[0]
                    x1 = x0 + det_bbox[2]
                    y0 = det_bbox[1]
                    y1 = y0 + det_bbox[3]

                    cv2.rectangle(
                        image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)

                    # Save face image on disk

                    file_name = '%07d.png' % face_counter

                    faces_path = os.path.join(self.track_path, 'Faces')

                    if not (os.path.exists(faces_path)):
                        os.makedirs(faces_path)

                    face_path = os.path.join(faces_path, file_name)

                    face = image_copy[y0:y1, x0:x1]

                    cv2.imwrite(face_path, face,
                                [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                    # Save cloth image on disk

                    clothes_path = os.path.join(self.track_path, 'Clothes')

                    if not (os.path.exists(clothes_path)):
                        os.makedirs(clothes_path)

                    cloth_path = os.path.join(clothes_path, file_name)

                    old_y0 = y0

                    y0 = y1

                    y1 = y1 + (y1 - old_y0)

                    cloth = image_copy[y0:y1, x0:x1]

                    cv2.imwrite(cloth_path, cloth,
                                [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                # Add rectangle for clothes
                cv2.rectangle(
                    image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                file_name = '%07d.png' % image_counter

                face_path = os.path.join(segment_path, file_name)

                cv2.imwrite(face_path, image,
                            [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                del image

                image_counter += 1

                face_counter += 1

            segment_counter += 1

    def save_rec_people(self):
        """
        Save frames for recognized people on disk.
        A folder contains the segments from one person
        """

        print '\n\n### Saving recognized people ###\n'

        people_path = os.path.join(self.rec_path, c.FACE_RECOGNITION_PEOPLE_DIR)

        # Delete already saved files
        if os.path.exists(people_path):

            images_dirs = os.listdir(people_path)

            for images_dir in images_dirs:
                images_dir_path = os.path.join(people_path, images_dir)
                shutil.rmtree(images_dir_path)

        for person_dict in self.recognized_faces:

            tag = person_dict[c.ASSIGNED_TAG_KEY]

            person_path = os.path.join(people_path, str(tag))

            segment_list = person_dict[c.SEGMENTS_KEY]

            segment_counter = 0

            for segment_dict in segment_list:

                segment_frame_list = segment_dict[c.FRAMES_KEY]

                segment_path = os.path.join(
                    person_path, str(segment_counter))

                if not (os.path.exists(segment_path)):
                    os.makedirs(segment_path)

                image_counter = 0

                for segment_frame_dict in segment_frame_list:

                    frame_name = segment_frame_dict[c.SAVED_FRAME_NAME_KEY]

                    frame_path = os.path.join(self.frames_path, frame_name)

                    image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                    # Add tracking window to image as red rectangle
                    track_bbox = segment_frame_dict[c.TRACKING_BBOX_KEY]

                    x0 = track_bbox[0]
                    x1 = x0 + track_bbox[2]
                    y0 = track_bbox[1]
                    y1 = y0 + track_bbox[3]

                    cv2.rectangle(
                        image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                    det = segment_frame_dict[c.DETECTED_KEY]

                    if det:
                        # Add detection bbox to image as blue rectangle
                        det_bbox = segment_frame_dict[c.DETECTION_BBOX_KEY]

                        x0 = det_bbox[0]
                        x1 = x0 + det_bbox[2]
                        y0 = det_bbox[1]
                        y1 = y0 + det_bbox[3]

                        cv2.rectangle(
                            image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)

                    file_name = '%07d.png' % image_counter

                    face_path = os.path.join(segment_path, file_name)

                    cv2.imwrite(face_path, image,
                                [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                    del image

                    image_counter += 1

                segment_counter += 1

    def search_face(self, ann_segments, segment_list, train_model, idx):
        """
        Search tracked faces that are similar to face in model.
        Segments to be checked are treated independently:
        a new segment is merged with reference segment
        if final confidence is below a fixed threshold.

        :type ann_segments: list
        :param ann_segments: list of already checked segments

        :type segment_list: list
        :param segment_list: list of segments related to the same person

        :type train_model: LBPHFaceRecognizer
        :param train_model: model of searched face

        :type idx: int
        :param idx: index of segment used for creating model

        :rtype: list
        :returns: list of already checked segments
        """

        use_aggregation = c.USE_AGGREGATION
        use_nose_pos_in_rec = c.USE_NOSE_POS_IN_RECOGNITION
        max_nose_diff = c.MAX_NOSE_DIFF
        conf_threshold = c.CONF_THRESHOLD

        use_clothing_rec = c.USE_CLOTHING_RECOGNITION

        use_3_bboxes = c.CLOTHING_REC_USE_3_BBOXES

        # Threshold for using clothing recognition
        clothes_conf_th = c.CLOTHES_CONF_THRESH

        if self.params is not None:

            if c.USE_AGGREGATION_KEY in self.params:
                use_aggregation = self.params[c.USE_AGGREGATION_KEY]

            if c.USE_NOSE_POS_IN_RECOGNITION_KEY in self.params:
                use_nose_pos_in_rec = (
                    self.params[c.USE_NOSE_POS_IN_RECOGNITION_KEY])

            if c.MAX_NOSE_DIFF_KEY in self.params:
                max_nose_diff = self.params[c.MAX_NOSE_DIFF_KEY]

            if c.CONF_THRESHOLD_KEY in self.params:
                conf_threshold = self.params[c.CONF_THRESHOLD_KEY]

            if c.USE_CLOTHING_RECOGNITION_KEY in self.params:
                use_clothing_rec = self.params[c.USE_CLOTHING_RECOGNITION_KEY]

            if c.CLOTHING_REC_USE_3_BBOXES_KEY in self.params:
                use_3_bboxes = self.params[c.CLOTHING_REC_USE_3_BBOXES_KEY]

            if c.CLOTHES_CONF_THRESH_KEY in self.params:
                clothes_conf_th = self.params[c.CLOTHES_CONF_THRESH_KEY]

        # Get histograms from model

        train_hists = train_model.getMatVector("histograms")

        # Get labels from model

        train_labels = train_model.getMat("labels")

        intra_dist1 = None

        if use_clothing_rec:

            # Get models for clothing recognition
            db_path_1 = os.path.join(self.cloth_models_path, str(idx))

            if os.path.isfile(db_path_1):

                with open(db_path_1, 'r') as f1:

                    model1 = pk.load(f1)

                    if model1:
                        intra_dist1 = utils.get_mean_intra_distance(
                            model1, use_3_bboxes)

        model = None

        sub_counter = 0
        for sub_segment_dict in self.tracked_faces:

            if sub_counter not in ann_segments:

                # Check that this segment do not overlap in time
                # with the other segments in the list

                seg_start = sub_segment_dict[c.SEGMENT_START_KEY]

                seg_dur = sub_segment_dict[c.SEGMENT_DURATION_KEY]

                seg_end = seg_start + seg_dur

                # If true, segment do overlap
                overlap_seg = False

                for l_segment_dict in segment_list:

                    l_seg_start = l_segment_dict[c.SEGMENT_START_KEY]

                    l_seg_dur = l_segment_dict[c.SEGMENT_DURATION_KEY]

                    l_seg_end = l_seg_start + l_seg_dur

                    if (((seg_start >= l_seg_start) and (
                            seg_start <= l_seg_end)) or
                            ((seg_end >= l_seg_start) and (
                            seg_end <= l_seg_end))):
                        overlap_seg = True
                        break

                if overlap_seg:
                    sub_counter += 1

                    continue

                db_path = os.path.join(
                    self.face_models_path, str(sub_counter))

                if os.path.isfile(db_path):

                    model = cv2.createLBPHFaceRecognizer()

                    model.load(db_path)

                    if model:

                        # Get histograms from model

                        model_hists = model.getMatVector("histograms")

                        # Get labels from model

                        model_labels = model.getMat("labels")

                        # Iterate through models related to this segment

                        final_tag = c.UNDEFINED_TAG

                        final_conf = sys.maxint

                        if use_aggregation:

                            frames = []

                            for i in range(0, len(model_hists)):

                                hist = model_hists[i][0]

                                label = model_labels[i][0]

                                nose_pos = None

                                if use_nose_pos_in_rec:
                                    nose_pos = (
                                        self.nose_pos_list[sub_counter][label])

                                # Confidence value
                                conf = sys.maxint

                                # Iterate through LBP histograms
                                # in training model
                                for t in range(0, len(train_hists)):

                                    train_hist = train_hists[t][0]

                                    train_label = train_labels[t][0]

                                    if use_nose_pos_in_rec:

                                        # Compare only faces with
                                        # similar nose position

                                        train_nose_pos = (
                                            self.nose_pos_list[idx][
                                                train_label])

                                        if ((nose_pos is None) or
                                                (train_nose_pos is None)):
                                            continue

                                        nose_diff_x = (
                                            abs(nose_pos[0] - train_nose_pos[
                                                0]))

                                        nose_diff_y = (
                                            abs(nose_pos[1] - train_nose_pos[
                                                1]))

                                        if ((nose_diff_x > max_nose_diff)or
                                                (nose_diff_y > max_nose_diff)):
                                            continue

                                    diff = cv2.compareHist(
                                        hist, train_hist, cv.CV_COMP_CHISQR)

                                    if diff < conf:
                                        conf = diff

                                frame_dict = {c.CONFIDENCE_KEY: conf}
                                ass_tag = c.UNDEFINED_TAG

                                if conf < conf_threshold:
                                    ass_tag = c.TRACKED_PERSON_TAG

                                frame_dict[c.ASSIGNED_TAG_KEY] = ass_tag

                                frames.append(frame_dict)

                            tgs = [c.TRACKED_PERSON_TAG, c.UNDEFINED_TAG]

                            [final_tag, final_conf, pct] = (
                                utils.aggregate_frame_results(
                                    frames, tags=tgs, params=self.params))

                        else:

                            for i in range(0, len(model_hists)):

                                hist = model_hists[i][0]

                                label = model_labels[i][0]

                                nose_pos = None

                                if use_nose_pos_in_rec:
                                    nose_pos = (
                                        self.nose_pos_list[sub_counter][label])

                                # Iterate through LBP histograms
                                # in training model
                                for t in range(0, len(train_hists)):

                                    train_hist = train_hists[t][0]

                                    train_label = train_labels[t][0]

                                    if use_nose_pos_in_rec:

                                        # Compare only faces with
                                        # similar nose position

                                        train_nose_pos = (
                                            self.nose_pos_list[idx][
                                                train_label])

                                        if ((nose_pos is None) or
                                                (train_nose_pos is None)):
                                            continue

                                        nose_diff_x = (
                                            abs(nose_pos[0] - train_nose_pos[
                                                0]))

                                        nose_diff_y = (
                                            abs(nose_pos[1] - train_nose_pos[
                                                1]))

                                        if ((nose_diff_x > max_nose_diff) or
                                                (nose_diff_y > max_nose_diff)):
                                            continue

                                    diff = cv2.compareHist(
                                        hist, train_hist, cv.CV_COMP_CHISQR)

                                    if diff < final_conf:
                                        final_conf = diff

                            if final_conf < conf_threshold:

                                if use_clothing_rec:

                                    # If final confidence is very low
                                    # do not use clothing recognition
                                    if final_conf < clothes_conf_th:

                                        final_tag = c.TRACKED_PERSON_TAG

                                    else:

                                        # Check clothing similarity

                                        db_path_2 = os.path.join(
                                            self.cloth_models_path,
                                            str(sub_counter))

                                        # noinspection PyUnboundLocalVariable
                                        similar = utils.compare_clothes(
                                            db_path_1, db_path_2, final_conf,
                                            intra_dist1, self.params)

                                        if similar:
                                            final_tag = c.TRACKED_PERSON_TAG

                                else:

                                    final_tag = c.TRACKED_PERSON_TAG

                        # Person in segment is recognized
                        if final_tag == c.TRACKED_PERSON_TAG:
                            segment_dict = {}

                            sub_fr_list = sub_segment_dict[c.FRAMES_KEY]

                            segment_dict[c.FRAMES_KEY] = sub_fr_list

                            segment_dict[c.ASSIGNED_TAG_KEY] = c.UNDEFINED_TAG

                            segment_dict[c.CONFIDENCE_KEY] = final_conf

                            # Start of segment in milliseconds
                            # of elapsed time in video

                            start = sub_segment_dict[c.SEGMENT_START_KEY]

                            segment_dict[c.SEGMENT_START_KEY] = start

                            # Duration of segment in milliseconds

                            duration = sub_segment_dict[c.SEGMENT_DURATION_KEY]

                            segment_dict[c.SEGMENT_DURATION_KEY] = duration

                            segment_dict[c.SEGMENT_COUNTER_KEY] = sub_counter

                            segment_list.append(segment_dict)

                            # Do not consider this segment anymore
                            ann_segments.append(sub_counter)

            sub_counter += 1

        del model

        return ann_segments

    def show_keyframes(self):
        """
        Show and save one image (keyframe)
        for each people cluster found in video.
        """

        logger.debug('Saving keyframes')

        key_frames_path = os.path.join(
            self.rec_path, c.FACE_RECOGNITION_KEY_FRAMES_DIR)

        if not (os.path.exists(key_frames_path)):
            os.makedirs(key_frames_path)

        # Check existence of recognition results
        if len(self.recognized_faces) == 0:

            # Try to load YAML file
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'
                logger.debug('Loading YAML file with recognition results')

                with open(self.rec_file_path) as f:

                    self.recognized_faces = yaml.load(f)

                print 'YAML file with recognition results loaded'
                logger.debug('YAML file with recognition results loaded')

            else:

                print 'Warning! No recognition results found!'
                logger.warning('No recognition results found!')

                return

        p_counter = 0

        for person_dict in self.recognized_faces:

            segment_list = person_dict[c.SEGMENTS_KEY]

            medoid_frame_name = person_dict[c.MEDOID_FRAME_NAME_KEY]

            medoid_found = False

            for segment_dict in segment_list:

                frame_list = segment_dict[c.FRAMES_KEY]

                for frame_dict in frame_list:

                    frame_name = frame_dict[c.SAVED_FRAME_NAME_KEY]

                    if frame_name == medoid_frame_name:
                        # Medoid is found

                        frame_path = os.path.join(self.frames_path, frame_name)

                        image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                        # Add tracking window to image as red rectangle
                        track_bbox = frame_dict[c.TRACKING_BBOX_KEY]

                        x0 = track_bbox[0]
                        x1 = x0 + track_bbox[2]
                        y0 = track_bbox[1]
                        y1 = y0 + track_bbox[3]

                        cv2.rectangle(
                            image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                        # Save image
                        fr_name = '%07d.png' % p_counter

                        fr_path = os.path.join(key_frames_path, fr_name)

                        cv2.imwrite(
                            fr_path, image, [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                        # Store keyframe filename
                        self.recognized_faces[p_counter][
                            c.KEYFRAME_NAME_KEY] = fr_name

                        del image

                        medoid_found = True

                        break

                if medoid_found:
                    # No need to continue iteration
                    break

            p_counter += 1

        # Update YAML file
        self.update_rec_file()

    def store_tag_id(self, person_counter, tag_id):
        """
        Store identifier of tag corresponding to person cluster
        with given person counter

        :type person_counter: integer
        :param person_counter: counter of person for which identifier
        of tag must be stored

        :type tag_id: integer
        :param tag_id: tag identifier
        """

        logger.debug('Storing tag id ' +
                     str(tag_id) + ' associated to person counter ' +
                     str(person_counter))

        # Check existence of recognition results
        if len(self.recognized_faces) == 0:

            # Try to load YAML file
            if os.path.exists(self.rec_file_path):

                print 'Loading YAML file with recognition results'
                logger.debug('Loading YAML file with recognition results')

                with open(self.rec_file_path) as f:

                    self.recognized_faces = yaml.load(f)

                print 'YAML file with recognition results loaded'
                logger.debug('YAML file with recognition results loaded')

            else:

                print 'Warning! No recognition results found!'
                logger.warning('No recognition results found!')

                return

        p_counter = 0

        for person_dict in self.recognized_faces:

            prs_counter = person_dict[c.PERSON_COUNTER_KEY]

            if prs_counter == person_counter:
                self.recognized_faces[p_counter][c.TAG_ID_KEY] = tag_id

            p_counter += 1

    def track_faces_in_video(self):
        """
        Track faces on analyzed video.
        It works by using list of detected faces.
        """

        logger.debug('Executing face tracking')

        track_loaded = False

        # Try to load YAML file with tracking results
        if os.path.exists(self.track_file_path):

            print 'Loading YAML file with tracking results'
            logger.debug('Loading YAML file with tracking results')

            track_faces = utils.load_YAML_file(self.track_file_path)

            if track_faces:
                self.tracked_faces = track_faces

                print 'YAML file with tracking results loaded'
                logger.debug('YAML file with tracking results loaded')

                track_loaded = True

        if not track_loaded:

            # Check existence of detection results

            if len(self.detected_faces) == 0:

                # Try to load YAML file
                if os.path.exists(self.det_file_path):

                    print 'Loading YAML file with detection results'
                    logger.debug('Loading YAML file with detection results')

                    with open(self.det_file_path) as f:

                        self.detected_faces = yaml.load(f)

                    print 'YAML file with detection results loaded'
                    logger.debug('YAML file with detection results loaded')

                else:

                    print 'Warning! No detection results found!'
                    logger.warning('No detection results found!')

                    return

                    # Get shot cuts
            self.calc_hist_diff()

            print '\n\n### Face tracking ###\n'
            logger.debug('\n\n### Face tracking ###\n')

            # Save processing time
            start_time = cv2.getTickCount()

            self.tracked_faces = []

            self.disc_tracked_faces = []

            # Counter for frames with detected faces
            frame_counter = 0

            # If a reduced frame rate is used, frames are less
            use_or_fps = c.USE_ORIGINAL_FPS
            used_fps = c.USED_FPS
            min_segment_duration = c.MIN_SEGMENT_DURATION
            tracking_min_int_area = c.TRACKING_MIN_INT_AREA
            min_size_width = c.FACE_DETECTION_MIN_SIZE_WIDTH
            min_size_height = c.FACE_DETECTION_MIN_SIZE_HEIGHT
            max_fr_with_miss_det = c.MAX_FR_WITH_MISSED_DET
            use_aligned_face = c.USE_ALIGNED_FACE_IN_TRACKING

            if self.params is not None:
                if c.USE_ORIGINAL_FPS_KEY in self.params:
                    use_or_fps = self.params[c.USE_ORIGINAL_FPS_KEY]
                if c.USED_FPS_KEY in self.params:
                    used_fps = self.params[c.USED_FPS_KEY]
                if c.MIN_SEGMENT_DURATION_KEY in self.params:
                    min_segment_duration = self.params[
                        c.MIN_SEGMENT_DURATION_KEY]
                if c.TRACKING_MIN_INT_AREA_KEY in self.params:
                    tracking_min_int_area = self.params[
                        c.TRACKING_MIN_INT_AREA_KEY]
                if c.MIN_SIZE_WIDTH_KEY in self.params:
                    min_size_width = self.params[c.MIN_SIZE_WIDTH_KEY]
                if c.MIN_SIZE_HEIGHT_KEY in self.params:
                    min_size_height = self.params[c.MIN_SIZE_HEIGHT_KEY]
                if c.MAX_FR_WITH_MISSED_DET_KEY in self.params:
                    max_fr_with_miss_det = self.params[
                        c.MAX_FR_WITH_MISSED_DET_KEY]
                if c.USE_ALIGNED_FACE_IN_TRACKING_KEY in self.params:
                    use_aligned_face = self.params[
                        c.USE_ALIGNED_FACE_IN_TRACKING_KEY]

            # Minimum duration of a segment in frames
            min_segment_frames = int(
                math.ceil(self.fps * min_segment_duration))

            if not use_or_fps:
                min_segment_frames = int(
                    math.ceil((used_fps + 1) * min_segment_duration))

                # Make copy of detected faces
            detection_list = list(self.detected_faces)

            # Iterate through frames in detected_faces
            for detection_dict in detection_list:

                self.progress = 100 * (frame_counter / self.saved_frames)

                print('progress: ' + str(self.progress) + ' %          \r'),

                elapsed_s = detection_dict[c.ELAPSED_VIDEO_TIME_KEY]

                frame_name = detection_dict[c.SAVED_FRAME_NAME_KEY]

                faces = detection_dict[c.FACES_KEY]

                face_counter = 0

                # Iterate though faces in frame
                for face_dict in faces:

                    track_window = face_dict[c.BBOX_KEY]

                    left_eye_pos = face_dict[c.LEFT_EYE_POS_KEY]

                    right_eye_pos = face_dict[c.RIGHT_EYE_POS_KEY]

                    nose_pos = face_dict[c.NOSE_POSITION_KEY]

                    file_name = face_dict[c.ALIGNED_FACE_FILE_NAME_KEY]

                    # Counter for faces in segment
                    segment_face_counter = 1

                    segment_frame_list = []

                    # Start new segment
                    segment_frame_dict = {c.FRAME_COUNTER_KEY: frame_counter,
                                          c.ELAPSED_VIDEO_TIME_KEY: elapsed_s,
                                          c.DETECTION_BBOX_KEY: track_window,
                                          c.TRACKING_BBOX_KEY: track_window,
                                          c.LEFT_EYE_POS_KEY: left_eye_pos,
                                          c.RIGHT_EYE_POS_KEY: right_eye_pos,
                                          c.NOSE_POSITION_KEY: nose_pos,
                                          c.ALIGNED_FACE_FILE_NAME_KEY: file_name,
                                          c.DETECTED_KEY: True,
                                          c.SAVED_FRAME_NAME_KEY: frame_name}

                    segment_frame_list.append(segment_frame_dict)

                    rgb_roi = None
                    if use_aligned_face:
                        # Use the aligned face as the
                        # Region of Interest for tracking
                        complete_file_name = file_name + '.png'
                        aligned_file_path = os.path.join(
                            self.align_path, complete_file_name)

                        rgb_roi = cv2.imread(
                            aligned_file_path, cv2.IMREAD_COLOR)

                    else:
                        # Use detected face as the
                        # Region of Interest for tracking
                        x0 = track_window[0]
                        y0 = track_window[1]
                        w = track_window[2]
                        h = track_window[3]
                        x1 = x0 + w
                        y1 = y0 + h

                        frame_path = os.path.join(
                            self.frames_path, frame_name)

                        # Whole frame
                        rgb = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                        # Face
                        rgb_roi = rgb[y0:y1, x0:x1]

                    if rgb_roi is None:
                        print('Warning! Face to be tracked is None')

                        if use_aligned_face:
                            logger.warning(
                                'Face ' + aligned_file_path + ' is None')
                        else:
                            logger.warning(
                                'Face from frame ' + frame_name + ' is None')

                        face_counter += 1

                        continue

                        # Convert image to hsv
                    hsv_roi = cv2.cvtColor(rgb_roi, cv2.COLOR_BGR2HSV)

                    mask_roi = cv2.inRange(
                        hsv_roi, np.array((0., 60., 32.)),
                        np.array((180., 255., 255.)))

                    hist = cv2.calcHist(
                        [hsv_roi], [0], mask_roi, [16], [0, 180])

                    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                    hist = hist.reshape(-1)

                    # Face should not be considered anymore
                    del (detection_list[frame_counter]
                         [c.FACES_KEY][face_counter])

                    sub_frame_counter = frame_counter + 1

                    missed_det_counter = 0

                    # Iterate through subsequent frames
                    for sub_det_dict in detection_list[sub_frame_counter:]:

                        # Check if a new shot begins
                        if sub_frame_counter in self.cut_idxs:
                            break

                        sub_frame_name = sub_det_dict[c.SAVED_FRAME_NAME_KEY]

                        sub_frame_path = os.path.join(
                            self.frames_path, sub_frame_name)

                        # Read image from given path
                        sub_image = cv2.imread(
                            sub_frame_path, cv2.IMREAD_COLOR)

                        if sub_image is None:
                            print('Warning! Image is None')
                            logger.warning(
                                'Image ' + sub_frame_path + ' is None')

                            continue

                        # Convert image to hsv
                        sub_hsv = cv2.cvtColor(sub_image, cv2.COLOR_BGR2HSV)

                        sub_mask = cv2.inRange(sub_hsv,
                                               np.array((0., 60., 32.)),
                                               np.array((180., 255., 255.)))

                        # Apply meanshift to get the new location
                        prob = cv2.calcBackProject(
                            [sub_hsv], [0], hist, [0, 180], 1)
                        prob &= sub_mask
                        term_crit = (cv2.TERM_CRITERIA_EPS
                                     | cv2.TERM_CRITERIA_COUNT, 10, 1)

                        track_box, track_window = cv2.CamShift(
                            prob, track_window, term_crit)

                        track_x0 = track_window[0]
                        track_y0 = track_window[1]
                        track_w = track_window[2]
                        track_h = track_window[3]

                        # Check size of track window
                        if ((track_w <= min_size_width)
                                or (track_h <= min_size_height)):

                            break

                        segment_frame_dict = {}

                        track_list = (
                            int(track_x0), int(track_y0), int(track_w),
                            int(track_h))

                        segment_frame_dict[c.TRACKING_BBOX_KEY] = track_list

                        sub_faces = sub_det_dict[c.FACES_KEY]

                        sub_face_counter = 0

                        sim = False

                        det_bbox = None

                        for sub_face_dict in sub_faces:

                            det_bbox = sub_face_dict[c.BBOX_KEY]

                            # If track window corresponds to 
                            # a detected face, 
                            # delete detection from list

                            sim = utils.is_rect_similar(
                                track_window, det_bbox, tracking_min_int_area)

                            if sim:
                                # det_face_counter = det_face_counter + 1

                                track_window = det_bbox

                                break

                            sub_face_counter += 1

                        t_x0 = track_window[0]
                        t_y0 = track_window[1]
                        t_w = track_window[2]
                        t_h = track_window[3]

                        segment_frame_dict[c.DETECTION_BBOX_KEY] = det_bbox

                        # If a detected face corresponds to track window
                        # delete detected face from detection list

                        if sim:

                            missed_det_counter = 0

                            segment_frame_dict[c.DETECTED_KEY] = True

                            segment_frame_dict[c.LEFT_EYE_POS_KEY] = (
                                sub_face_dict[c.LEFT_EYE_POS_KEY])
                            segment_frame_dict[c.RIGHT_EYE_POS_KEY] = (
                                sub_face_dict[c.RIGHT_EYE_POS_KEY])

                            segment_frame_dict[c.NOSE_POSITION_KEY] = (
                                sub_face_dict[c.NOSE_POSITION_KEY])

                            segment_frame_dict[c.ALIGNED_FACE_FILE_NAME_KEY] = (
                                sub_face_dict[c.ALIGNED_FACE_FILE_NAME_KEY])

                            del (detection_list[sub_frame_counter]
                                 [c.FACES_KEY][sub_face_counter])

                        else:

                            # Check if distance from last detection
                            # is too big
                            missed_det_counter += 1

                            if missed_det_counter > max_fr_with_miss_det:

                                # Remove last frames and 
                                # interrupt tracking
                                for i in range(0, max_fr_with_miss_det):
                                    segment_frame_list.pop()

                                segment_face_counter = (
                                    segment_face_counter - max_fr_with_miss_det)

                                break

                            segment_frame_dict[c.DETECTED_KEY] = False

                        elapsed_ms = sub_det_dict[c.ELAPSED_VIDEO_TIME_KEY]

                        # Update list of frames for segment
                        segment_frame_dict[
                            c.FRAME_COUNTER_KEY] = sub_frame_counter
                        segment_frame_dict[
                            c.ELAPSED_VIDEO_TIME_KEY] = elapsed_ms

                        track_list = (
                            int(t_x0), int(t_y0), int(t_w), int(t_h))

                        segment_frame_dict[c.TRACKING_BBOX_KEY] = track_list
                        segment_frame_dict[
                            c.SAVED_FRAME_NAME_KEY] = sub_frame_name

                        segment_frame_list.append(segment_frame_dict)

                        del sub_image

                        sub_frame_counter += 1

                        segment_face_counter += 1

                    # Segment must be considered only if its number 
                    # of frames is greater or equals than a minimum
                    if segment_face_counter >= min_segment_frames:

                        segments = self.divide_segment_by_face(
                            segment_frame_list)

                        if len(segments) > 0:
                            self.tracked_faces.extend(segments)

                    else:

                        segment_dict = {c.FRAMES_KEY: segment_frame_list}

                        self.disc_tracked_faces.append(segment_dict)

                        # Check histograms of detected faces and 
                        # divide segment accordingly   

                    face_counter += 1

                frame_counter += 1

            # Create directory for this video  

            if not (os.path.exists(self.track_path)):
                os.makedirs(self.track_path)

                # Save tracking result in YAML file
            utils.save_YAML_file(self.track_file_path, self.tracked_faces)

            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()

            print 'Time for face tracking:', time_in_seconds, 's\n'
            logger.debug('Time for face tracking:', time_in_seconds, 's\n')

            self.anal_times[c.FACE_TRACKING_TIME_KEY] = time_in_seconds

            utils.save_YAML_file(self.analysis_file_path, self.anal_times)

    def update_rec_file(self):
        """
        Update YAML file with people recognition results
        """

        logger.debug('Updating YAML file with people recognition results')

        utils.save_YAML_file(self.rec_file_path, self.recognized_faces)
