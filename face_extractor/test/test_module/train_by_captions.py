import cv2
import numpy as np
import os
import sys

import constants_for_experiments as ce
from utils_for_experiments import save_model_file

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.caption_recognition import get_tag_from_image
from tools.face_detection import get_detected_cropped_face
from tools.utils import save_YAML_file

ASSIGNED_LABEL_KEY = 'assigned_label'


def analyze_image(image_path, params=None):
    """
    Execute caption recognition on given image

    :type image_path: string
    :param image_path: path of image to be analyzed

    :type params: dictionary
    :param params: dictionary with configuration parameters

    :rtype: list
    :returns: a [label, tag, face] list,
    where label is the assigned label,
    tag the assigned tag
    and face the detected face in image (as an OpenCV image)
    """
    
    label = -1
    
    tag = -1

    align_path = c.ALIGNED_FACES_PATH
    if (params is not None) and (c.ALIGNED_FACES_PATH_KEY in params):
        align_path = params[c.ALIGNED_FACES_PATH_KEY]

    # Face detection
    face = get_detected_cropped_face(image_path, align_path, params)
    
    if face is not None:
            
        cap_rec_res = get_tag_from_image(image_path, params)
        
        label = cap_rec_res[c.ASSIGNED_LABEL_KEY]
        
        tag = cap_rec_res[c.ASSIGNED_TAG_KEY]

    return [label, tag, face]


def train_by_captions(video_path, db_file_name, params=None):
    """
    Train an LBP face recognizer by using the captions in given video

    :type video_path: string
    :param video_path: path of video with captions

    :type db_file_name: string
    :param db_file_name: path of file that will contain the face models

    :type params: dictionary
    :param params: dictionary with configuration parameters

    :rytpe: list
    :return: a [model, tags] list, where model is an LBPHFaceRecognizer
    and tags is the list of found tags
    """

    # Set parameters
    lbp_radius = c.LBP_RADIUS
    lbp_neighbors = c.LBP_NEIGHBORS
    lbp_grid_x = c.LBP_GRID_X
    lbp_grid_y = c.LBP_GRID_Y
    use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS
    use_or_fps = ce.USE_ORIGINAL_FPS_IN_TRAINING
    used_fps_in_training = ce.USED_FPS_IN_TRAINING
    if params:
        if c.LBP_RADIUS_KEY in params:
            lbp_radius = params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY in params:
            lbp_radius = params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY in params:
            lbp_radius = params[c.LBP_GRID_X]
        if c.LBP_GRID_Y_KEY in params:
            lbp_radius = params[c.LBP_GRID_Y_KEY]
        if ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY in params:
            use_one_file = params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY]
        if ce.USE_ORIGINAL_FPS_IN_TRAINING_KEY in params:
            use_or_fps = params[ce.USE_ORIGINAL_FPS_IN_TRAINING_KEY]
        if ce.USED_FPS_IN_TRAINING_KEY in params:
            used_fps_in_training = params[ce.USED_FPS_IN_TRAINING_KEY]


    # Save processing time
    start_time = cv2.getTickCount()

    model = None

    tags = {}

    capture = cv2.VideoCapture(video_path)

    print(video_path)

    # Counter for all frames
    frame_counter = 0

    # Counter for analyzed frames
    anal_frame_counter = 0

    # Value of frame_counter for last analyzed frame
    last_anal_frame = 0

    if capture is None or not capture.isOpened():

        error = 'Error in opening video file'

        print error

    else:

        video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)

        tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

        X, y = [], []

        while True:

            ret, frame = capture.read()

            if not ret:

                break

            # Next frame to be analyzed
            next_frame = last_anal_frame + (
                video_fps / used_fps_in_training) - 1
            if use_or_fps or (frame_counter > next_frame):

                progress = 100 * (frame_counter / tot_frames)

                print('progress: ' + str(progress) + '%')

                cv2.imwrite(ce.TMP_FRAME_FILE_PATH, frame)

                [label, tag, face] = analyze_image(ce.TMP_FRAME_FILE_PATH)

                if label != -1:

                    print('label', label)
                    print('tag', tag)

                    X.append(np.asarray(face, dtype=np.uint8))
                    y.append(label)
                    tags[label] = tag

                anal_frame_counter += 1

                last_anal_frame = frame_counter

            frame_counter += 1

            # Save file with face models

        if use_one_file:

            model = cv2.createLBPHFaceRecognizer(
            lbp_radius,
            lbp_neighbors,
            lbp_grid_x,
            lbp_grid_y)
            model.train(np.asarray(X), np.asarray(y))
            model.save(db_file_name)

        else:

            y_set = set(y)

            for label in y_set:

                person_X = []
                person_y = []

                for i in range(0, len(y)):

                    if y[i] == label:

                        person_X.append(X[i])
                        person_y.append(label)

                save_model_file(person_X, person_y, params, db_file_name)

        # Save labels in YAML file
        save_YAML_file(db_file_name + "-Tags", tags)

    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()

    print('Creation time: ' + str(time_in_s) + ' s\n')

    return [model, tags]


def train_by_images(path, db_file_name, params=None):
    """
    Train an LBP face recognizer by using captions in images

    :type path: string
    :param path: path of directory with images

    :type db_file_name: string
    :param db_file_name: path of file that will contain the face models

    :type params: dictionary
    :param params: dictionary with configuration parameters

    :rytpe: list
    :return: a [model, tags] list, where model is an LBPHFaceRecognizer
    and tags is the list of found tags
    """

    # Set parameters
    lbp_radius = c.LBP_RADIUS
    lbp_neighbors = c.LBP_NEIGHBORS
    lbp_grid_x = c.LBP_GRID_X
    lbp_grid_y = c.LBP_GRID_Y
    use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS
    if params:
        if c.LBP_RADIUS_KEY in params:
            lbp_radius = params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY in params:
            lbp_radius = params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY in params:
            lbp_radius = params[c.LBP_GRID_X]
        if c.LBP_GRID_Y_KEY in params:
            lbp_radius = params[c.LBP_GRID_Y_KEY]
        if ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY in params:
            use_one_file = params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY]

    # Save processing time
    start_time = cv2.getTickCount()
    
    model = None
    
    X, y = [], []
    tags = {}
    
    image_counter = 0
     
    for image in os.listdir(path):
    
        image_complete_path = path + os.sep + image
                
        [label, tag, face] = analyze_image(image_complete_path, params)
        
        if label != -1:
            
            X.append(np.asarray(face, dtype=np.uint8))
            y.append(label)
            tags[label] = tag

            image_counter += 1
    
    # Save file with face models
    
    if use_one_file:
            
        model = cv2.createLBPHFaceRecognizer(
        lbp_radius,
        lbp_neighbors,
        lbp_grid_x,
        lbp_grid_y)
        model.train(np.asarray(X), np.asarray(y))
        model.save(db_file_name)
        
    else:
        
        y_set = set(y)
            
        for label in y_set:
            
            person_X = []
            person_y = []
            
            for i in range(0, len(y)):
                
                if y[i] == label:
                    
                    person_X.append(X[i])
                    person_y.append(label)
                       
            save_model_file(person_X, person_y, params, db_file_name)
    
    # Save labels in YAML file
    save_YAML_file(db_file_name + "-Tags", tags)     
        
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Creation time: ' + str(time_in_s) + ' s\n')
    
    return [model, tags]
