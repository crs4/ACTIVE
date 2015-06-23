import cv2
import numpy as np
import os
import sys

import constants_for_experiments as ce

path_to_be_appended = ".." + os.sep + '..'
sys.path.append(path_to_be_appended)

import tools.constants as c
import tools.utils as utils


def load_experiment_results(file_path):
    """
    Load file with results of all experiments

    :type file_path: string
    :param file_path: file to be loaded

    :rtype: list
    :returns list with experiments
    """
    
    data = utils.load_YAML_file(file_path)
    experiments = data[ce.EXPERIMENTS_KEY]
    return experiments


def load_image_annotations(file_path):
    """
    Load YAML file with image .

    :type file_path: string
    :param file_path: path of YAML file to be loaded

    :rtype: list
    :returns: a list of dictionaries with the annotated images
    """
    
    data = utils.load_YAML_file(file_path)
    
    if data:
        
        images = data[c.ANNOTATIONS_FRAMES_KEY]
        return images
        
    else:
        
        print 'Unable to open', file_path
        return None
 

def save_model_file(X, y, params=None, db_file_name=None):
    """
    Save face model

    :type X: OpenCV image
    :param X: face image

    :type y: list
    :param y: labels of face model

    :type params: dictionary
    :param params: used parameters (see table)

    :type db_file_name: string
    :param db_file_name: path of directory where models are saved

    ========================  =========================================
    Key                       Value
    ========================  =========================================
    FACE_MODEL_ALGORITHM_KEY  Algorithm (it can be 'Eigenfaces',
                              'Fisherfaces' or 'LBP')
    LBP_RADIUS_KEY            Radius (used only if algorithm is 'LBP')
    LBP_NEIGHBORS_KEY         Number of neighbors
                              (used only if algorithm is 'LBP')
    LBP_GRID_X_KEY            Number of columns in LBP grid
                              (used only if algorithm is 'LBP')
    LBP_GRID_Y_KEY            Number of rows in LBP grid
                              (used only if algorithm is 'LBP')
    DB_MODELS_PATH_KEY        Path of directory where models are saved
                              (used if db_file_name is not provided)
    ========================  =========================================
    """

    if len(y) > 0:

        algorithm = ce.FACE_MODEL_ALGORITHM

        if((params is not None)
                and (ce.FACE_MODEL_ALGORITHM_KEY in params)):
            algorihtm = params[ce.FACE_MODEL_ALGORITHM_KEY]

        model = None

        if algorithm == 'Eigenfaces':

            model = cv2.createEigenFaceRecognizer()

        elif algorithm == 'Fisherfaces':

            model = cv2.createFisherFaceRecognizer()

        elif algorithm == 'LBP':

            radius = c.LBP_RADIUS
            neighbors = c.LBP_NEIGHBORS
            grid_x = c.LBP_GRID_X
            grid_y = c.LBP_GRID_Y

            if params is not None:

                if c.LBP_RADIUS_KEY in params:
                    radius = params[c.LBP_RADIUS_KEY]

                if c.LBP_NEIGHBORS_KEY in params:
                    neighbors = params[c.LBP_NEIGHBORS_KEY]

                if c.LBP_GRID_X_KEY in params:
                    grid_x = params[c.LBP_GRID_X_KEY]

                if c.LBP_GRID_Y_KEY in params:
                    grid_y = params[c.LBP_GRID_Y_KEY]

            model = cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)

        models_path = ce.DB_MODELS_PATH

        if((params is not None)
                and (c.DB_MODELS_PATH_KEY in params)):
            models_path = params[c.DB_MODELS_PATH_KEY]

        model.train(np.asarray(X), np.asarray(y))
        model_folder = models_path

        if db_file_name is not None:

            model_folder = db_file_name
            if not os.path.exists(model_folder):
                os.makedirs(model_folder)

        model_file = model_folder + os.sep + str(y[0])
        model.save(model_file)


def track_faces(frames, fm):
    """
    Track faces

    :type frames: list
    :param frames: list of frames

    :type fm: LBPHFaceRecognizer
    :param fm: face model

    :rtype: list
    :returns: list of segments
    """
    
    segments = []

    track_frame_counter = 0
    
    for frame in frames:

        faces = frame[c.FACES_KEY]

        elapsed_video_s = frame[c.ELAPSED_VIDEO_TIME_KEY]

        if len(faces) != 0:

            face_counter = 0
            for face in faces:

                segment_dict = {}

                segment_frame_counter = 1

                prev_bbox = face[c.BBOX_KEY]

                segment_frames_list = []

                segment_frame_dict = {c.ELAPSED_VIDEO_TIME_KEY: elapsed_video_s,
                                      c.FRAME_COUNTER_KEY: track_frame_counter,
                                      c.ASSIGNED_TAG_KEY: face[
                                          c.ASSIGNED_TAG_KEY],
                                      c.CONFIDENCE_KEY: face[c.CONFIDENCE_KEY],
                                      c.BBOX_KEY: prev_bbox}

                segment_frames_list.append(segment_frame_dict)

                del frames[track_frame_counter][c.FACES_KEY][face_counter]

                sub_frame_counter = track_frame_counter + 1

                prev_frame_counter = track_frame_counter

                # Search face in subsequent frames
                # and add good bounding boxes to segment
                # Bounding boxes included in this segment
                # must not be considered by other segments

                for subsequent_frame in frames[sub_frame_counter:]:

                    # Consider only successive frames
                    # or frames whose maximum distance is
                    # MAX_FRAMES_WITH_MISSED_DETECTION + 1
                    if(
                            sub_frame_counter > (
                                prev_frame_counter +
                                c.MAX_FR_WITH_MISSED_DET + 1)):

                        segment_frame_counter = (
                            segment_frame_counter -
                            c.MAX_FR_WITH_MISSED_DET - 1)

                        break

                    sub_faces = subsequent_frame[c.FACES_KEY]

                    elapsed_video_s = subsequent_frame[c.ELAPSED_VIDEO_TIME_KEY]

                    if len(sub_faces) != 0:

                        sub_face_counter = 0
                        for sub_face in sub_faces:

                            # Calculate differences between the two detections
                    
                            prev_bbox_x = prev_bbox[0]
                            prev_bbox_y = prev_bbox[1]
                            prev_bbox_w = prev_bbox[2]

                            bbox = sub_face[c.BBOX_KEY]

                            bbox_x = bbox[0]
                            bbox_y = bbox[1]
                            bbox_w = bbox[2]

                            delta_x = (abs(bbox_x - prev_bbox_x) /
                                       float(prev_bbox_w))
                            delta_y = (abs(bbox_y - prev_bbox_y) /
                                       float(prev_bbox_w))
                            delta_w = (abs(bbox_w - prev_bbox_w) /
                                       float(prev_bbox_w))

                            # Check if delta is small enough
                            if ((delta_x < ce.MAX_DELTA_PCT_X)
                                    and (delta_y < ce.MAX_DELTA_PCT_Y)
                                    and (delta_w < ce.MAX_DELTA_PCT_W)):

                                prev_bbox = bbox

                                segment_frame_dict = {
                                c.ELAPSED_VIDEO_TIME_KEY: elapsed_video_s,
                                c.FRAME_COUNTER_KEY: sub_frame_counter,
                                c.ASSIGNED_TAG_KEY: sub_face[
                                    c.ASSIGNED_TAG_KEY],
                                c.CONFIDENCE_KEY: sub_face[c.CONFIDENCE_KEY],
                                c.BBOX_KEY: bbox}

                                segment_frames_list.append(segment_frame_dict)

                                del frames[sub_frame_counter][c.FACES_KEY][sub_face_counter]

                                prev_frame_counter = sub_frame_counter

                                consecutive_frames_with_missed_detection = 0
                                # Do not consider other faces in the same frame
                                break

                        sub_face_counter += 1

                    sub_frame_counter += 1

                    segment_frame_counter += 1

                # Aggregate results from all frames in segment
                [final_tag, final_confidence] = utils.aggregate_frame_results(
                    segment_frames_list, fm)

                segment_dict[c.ASSIGNED_TAG_KEY] = final_tag

                segment_dict[c.CONFIDENCE_KEY] = final_confidence

                segment_dict[c.FRAMES_KEY] = segment_frames_list

                print('segment_frame_counter: ', segment_frame_counter)

                segment_dict[c.SEGMENT_TOT_FRAMES_NR_KEY] = segment_frame_counter

                segments.append(segment_dict)

                face_counter += 1

        track_frame_counter += 1

    return segments


def track_faces_with_LBP(frames, fm):
    """
    Track faces by using LBP

    :type frames: list
    :param frames: list of frames

    :type fm: FaceModels
    :param fm: face models to be used for tracking

    :rtype: list
    :returns: list of face tracks
    """

    segments = []

    tracking_frame_counter = 0

    for frame in frames:

        faces = frame[c.FACES_KEY]

        elapsed_video_s = frame[c.ELAPSED_VIDEO_TIME_KEY]

        if len(faces) != 0:

            face_counter = 0
            for face in faces:

                segment_dict = {}

                segment_frame_counter = 1

                prev_face = face[c.FACE_KEY]

                prev_bbox = face[c.BBOX_KEY]

                segment_frames_list = []

                segment_frame_dict = {
                c.ELAPSED_VIDEO_TIME_KEY: elapsed_video_s,
                c.FRAME_COUNTER_KEY: tracking_frame_counter,
                c.ASSIGNED_TAG_KEY: face[c.ASSIGNED_TAG_KEY],
                c.CONFIDENCE_KEY: face[c.CONFIDENCE_KEY],
                c.BBOX_KEY: prev_bbox}

                segment_frames_list.append(segment_frame_dict)

                del frames[tracking_frame_counter][c.FACES_KEY][face_counter]

                # Calculate LBP histograms from face
                X = [np.asarray(prev_face, dtype=np.uint8)]
                l = [0]
                model = cv2.createLBPHFaceRecognizer(
                c.LBP_RADIUS,
                c.LBP_NEIGHBORS,
                c.LBP_GRID_X,
                c.LBP_GRID_Y)
                model.train(np.asarray(X), np.asarray(l))

                sub_frame_counter = tracking_frame_counter + 1

                prev_frame_counter = tracking_frame_counter

                # Search face in subsequent frames
                # and add good bounding boxes to segment
                # Bounding boxes included in this segment
                # must not be considered by other segments

                continue_tracking = True

                for subsequent_frame in frames[sub_frame_counter:]:

                    # Consider only successive frames or frames whose
                    # maximum distance is MAX_FRAMES_WITH_MISSED_DETECTION + 1
                    if sub_frame_counter > (
                            prev_frame_counter +
                            ce.MAX_FR_WITH_MISSED_DET + 1):

                        segment_frame_counter = (
                            segment_frame_counter -
                            ce.MAX_FR_WITH_MISSED_DET_KEY - 1)

                        break

                    sub_faces = subsequent_frame[c.FACES_KEY]

                    elapsed_video_s = subsequent_frame[c.ELAPSED_VIDEO_TIME_KEY]

                    if len(sub_faces) != 0:

                        sub_face_counter = 0
                        continue_tracking = False
                        for sub_face in sub_faces:

                            # Calculate differences between the two detections

                            this_face = sub_face[c.FACE_KEY]

                            [lbl, conf] = model.predict(
                                np.asarray(this_face, dtype=np.uint8))

                            print 'conf =', conf  # TEST ONLY

                            # Check if confidence is low enough
                            if conf < ce.STOP_TRACKING_THRESHOLD:

                                # Calculate LBP histograms from face
                                X = [np.asarray(this_face, dtype=np.uint8)]
                                l = [0]
                                model = cv2.createLBPHFaceRecognizer(
                                c.LBP_RADIUS,
                                c.LBP_NEIGHBORS,
                                c.LBP_GRID_X,
                                c.LBP_GRID_Y)
                                model.train(np.asarray(X), np.asarray(l))

                                continue_tracking = True

                                segment_frame_dict = {
                                c.ELAPSED_VIDEO_TIME_KEY: elapsed_video_s,
                                c.FRAME_COUNTER_KEY: sub_frame_counter,
                                c.ASSIGNED_TAG_KEY: sub_face[
                                    c.ASSIGNED_TAG_KEY],
                                c.CONFIDENCE_KEY: sub_face[c.CONFIDENCE_KEY],
                                c.BBOX_KEY: sub_face[c.BBOX_KEY]}

                                segment_frames_list.append(segment_frame_dict)

                                del frames[sub_frame_counter][c.FACES_KEY][sub_face_counter]

                                prev_frame_counter = sub_frame_counter

                                consecutive_frames_with_missed_detection = 0

                                # Do not consider other faces in the same frame
                                break

                        sub_face_counter += 1

                    sub_frame_counter += 1

                    segment_frame_counter += 1

                    if not continue_tracking:

                        break

                # Aggregate results from all frames in segment
                [final_tag, final_confidence] = utils.aggregate_frame_results(
                    segment_frames_list, fm)

                segment_dict[c.ASSIGNED_TAG_KEY] = final_tag

                segment_dict[c.CONFIDENCE_KEY] = final_confidence

                segment_dict[c.FRAMES_KEY] = segment_frames_list

                segment_dict[c.SEGMENT_TOT_FRAMES_NR_KEY] = segment_frame_counter

                segments.append(segment_dict)

                face_counter += 1

        tracking_frame_counter += 1

    return segments
