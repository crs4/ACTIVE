import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import sys
from collections import Counter

import constants_for_experiments as ce
from face_models_for_experiments import FaceModels

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c


def calculate_w_reg_distance(query_hist, train_hist):
    """
    Calculate distance between two images by using weighted LBP

    :type query_hist: list
    :param query_hist: LBP histograms of the first image

    :type train_hist: list
    :param train_hist: LBP histograms of the second image

    :rtype: float
    :returns: distance
    """
    
    nr_regions = c.LBP_GRID_X * c.LBP_GRID_Y
    
    len_reg_hist = 2 ** c.LBP_NEIGHBORS
    
    diff = 0
    
    for r in range(0, nr_regions):
        
        first_idx = r * len_reg_hist
        
        last_idx = (r + 1) * len_reg_hist
        
        query_reg_hist = query_hist[first_idx:last_idx]
        
        train_reg_hist = train_hist[first_idx:last_idx]
        
        reg_diff = 0
        
        if r in ce.WEIGHT_0_REGIONS:
            
            pass
            
        elif r in ce.WEIGHT_2_REGIONS:
            
            reg_diff = 2 * cv2.compareHist(
            query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
            
        elif r in ce.WEIGHT_4_REGIONS:
            
            reg_diff = 4 * cv2.compareHist(
            query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
            
        else:
            
            reg_diff = cv2.compareHist(
            query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
            
        diff = diff + reg_diff
        
    return diff


def recognize_with_NBNN_distance(
        query_hist, train_histograms, train_labels, im_w, im_h, people_nr):
    """
    Recognize face by using Naive Bayes Nearest Neighbor

    :type query_hist: list
    :param query_hist: LBP histograms of the query image

    :type train_histograms: list
    :param train_histograms: LBP histograms of the training set

    :type train_labels: list
    :param train_labels: labels of the training set

    :type im_w: integer
    :param im_w: width of the query image (in pixels)

    :type im_h: integer
    :param im_h: height of the query image (in pixels)

    :type people_nr: integer
    :param people_nr: number of people in the training set

    :rtype: tuple
    :returns: a (label, confidence) tuple,
              where label is the predicted label
              and confidence is the calculated distance
    """
    
    nr_regions = c.LBP_GRID_X * c.LBP_GRID_Y
    
    len_reg_hist = 2 ** c.LBP_NEIGHBORS
    
    reg_w = float(im_w) / c.LBP_GRID_X
    reg_h = float(im_h) / c.LBP_GRID_Y
    
    # List with minimum differences for all query regions
    diff_list = [] 
    
    for p in range(0, people_nr):
        
        min_diff_list = []
    
        for r in range(0, nr_regions):
            
            # Calculate region position for query image
    
            reg_x_counter = r % c.LBP_GRID_X
            
            reg_y_counter = r / c.LBP_GRID_Y
            
            q_x = reg_x_counter * reg_w / im_w
            
            q_y = reg_y_counter * reg_h / im_h
            
            first_idx = r * len_reg_hist
            
            last_idx = (r + 1) * len_reg_hist
            
            query_reg_hist = query_hist[first_idx:last_idx]
                
            # Consider all images of training subject p
                
            min_reg_diff = sys.maxint

            for t in range(0, len(train_labels)):
                
                if train_labels[t] == p:
                    
                    t_hist = train_histograms[t][0]
                    
                    for r2 in range(0, nr_regions):
                        
                        fi = r2 * len_reg_hist
        
                        li = (r2 + 1) * len_reg_hist
                        
                        t_reg_hist = t_hist[fi:li]
                        
                        hist_diff = cv2.compareHist(
                        query_reg_hist, t_reg_hist, cv.CV_COMP_CHISQR)
                        
                        # Calculate region position for train image
                        
                        reg_x_counter = r2 % c.LBP_GRID_X
                        
                        reg_y_counter = r2 / c.LBP_GRID_Y
                        
                        t_x = reg_x_counter * reg_w / im_w
                        
                        t_y = reg_y_counter * reg_h / im_h
                        
                        pos_diff_x = math.pow(q_x - t_x, 2)
                        pos_diff_y = math.pow(q_y - t_y, 2)
                        pos_diff = ce.ALFA * (pos_diff_x + pos_diff_y)
                        
                        reg_diff = hist_diff + pos_diff
                        
                        if reg_diff < min_reg_diff:
                            
                            min_reg_diff = reg_diff
    
            min_diff_list.append(min_reg_diff)
        
        diff = min(min_diff_list)
        
        diff_list.append(diff)
        
    idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]
    
    label = idxs[0]
    
    confidence = diff_list[label]
    
    return label, confidence


def recognize_face_from_model_files(
        face, face_models, params=None, show_results=False):
    """
    Recognize given face using
    the face recognition models saved as one file per person

    :type face: image
    :param face: face to be recognized

    :type face_models: LBPHFaceRecognizer
    :param face_models: face model

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face recognition (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False) recognized face

    :rtype: dictionary
    :returns: dictionary with results (see table)

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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
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

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    elapsed_CPU_time                       The elapsed CPU time in seconds
    error                                  A string specifying an error
                                           condition,
                                           or None if no errors occurred
    assigned_label                         Predicted label (integer)
    assigned_tag                           Predicted tag (string)
    confidence                             Confidence associated to prediction
    =====================================  =====================================
    """

    fm = face_models
    if face_models is None:
        fm = FaceModels(params)

    start_time = cv2.getTickCount()

    label = -1
    tag = -1
    confidence = -1
    error = None

    lbp_radius = c.LBP_RADIUS
    lbp_neighbors = c.LBP_NEIGHBORS
    lbp_grid_x = c.LBP_GRID_X
    lbp_grid_y = c.LBP_GRID_Y
    use_NBNN = ce.USE_NBNN
    use_weighted_regions = ce.USE_WEIGHTED_REGIONS

    if params is not None:
        if c.LBP_RADIUS_KEY is not None:
            lbp_radius = params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY is not None:
            lbp_neighbors = params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY is not None:
            lbp_grid_x = params[c.LBP_GRID_X_KEY]
        if c.LBP_GRID_Y_KEY is not None:
            lbp_grid_y = params[c.LBP_GRID_Y_KEY]
        if ce.USE_NBNN_KEY in params:
            use_NBNN = params[ce.USE_NBNN_KEY]
        if ce.USE_WEIGHTED_REGIONS_KEY in params:
            use_weighted_regions = params[ce.USE_WEIGHTED_REGIONS_KEY]

    query_model = cv2.createLBPHFaceRecognizer(
    lbp_radius, lbp_neighbors,
    lbp_grid_x, lbp_grid_y)
        
    query_model.train(
    np.asarray([np.asarray(face, dtype=np.uint8)]), np.asarray([0]))
    
    query_histograms = query_model.getMatVector("histograms")
    
    query_hist = query_histograms[0][0]
    
    diff_list = []
    
    train_labels = []
        
    for model_file in os.listdir(ce.DB_MODELS_PATH):
        
        model_file_path = os.path.join(ce.DB_MODELS_PATH, model_file)
        
        ok = fm.load_model(model_file_path)
        
        if ok:
        
            model_histograms = fm.model.getMatVector("histograms")
            
            model_labels = fm.model.getMat("labels")
            
            for i in range(0, len(model_histograms)):
            
                train_hist = model_histograms[i][0]
                
                diff = 0
                
                if use_weighted_regions:
                    
                    diff = calculate_w_reg_distance(query_hist, train_hist)
                    
                elif use_NBNN:
                    error = 'NBNN not implemented'
                
                else:
            
                    diff = cv2.compareHist(
                    query_hist, train_hist, cv.CV_COMP_CHISQR)  
                    
                diff_list.append(diff)
                
            train_labels.extend(model_labels)  
        
    # Get K nearest histograms
    
    if len(diff_list) > 0:

        idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]

        K = ce.KNN_NEIGHBORS

        if ce.CALCULATE_K_FROM_FEATURES:

            nr_features = 2 ** lbp_neighbors * lbp_grid_x * lbp_grid_y

            K = int(round(math.sqrt(nr_features)))

        if K == 1:

            idx = idxs[0]

            confidence = diff_list[idx]

            label = train_labels[idx][0]

        else:

            nearest_labels_list = []

            # K cannot be greater than number of training items
            if K > len(idxs):

                K = len(idxs)

            for i in range(0, K):

                idx = idxs[i]

                diff = diff_list[idx]

                weight = 0

                if diff < 1:

                    weight = 100

                elif diff > 100:

                    weight = 1

                else:

                    weight = int(round(100 / diff))

                label = train_labels[idx][0]

                for t in range(0, weight):

                    nearest_labels_list.append(label)

            # Find most common label in K nearest ones
            data = Counter(nearest_labels_list)

            label = data.most_common(1)[0][0]

            counter = data.most_common(1)[0][1]

            confidence = counter
    
        tag = fm.get_tag(label)

    rec_time_in_clocks = cv2.getTickCount() - start_time
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency()

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {c.ELAPSED_CPU_TIME_KEY: rec_time_in_seconds, c.ERROR_KEY: error,
              c.ASSIGNED_LABEL_KEY: label, c.ASSIGNED_TAG_KEY: tag,
              c.CONFIDENCE_KEY: confidence}

    if show_results:
        cv2.imshow(str(label), face)
        cv2.waitKey(0) 

    return result


def recognize_face_from_models_file(
        face, face_models, params=None, show_results=False):
    """
    Recognize given face using
    the face recognition model saved as one file,
    comparison between histograms is explicit

    :type face: OpenCV image
    :param face: face to be recognized

    :type face_models: LBPHFaceRecognizer
    :param face_models: face model

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face recognition (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False) recognized face

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  ==============
    Key (params)                                  Value                                     Default value
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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
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

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    elapsed_CPU_time                       The elapsed CPU time in seconds
    error                                  A string specifying an error
                                           condition,
                                           or None if no errors occurred
    assigned_label                         Predicted label (integer)
    assigned_tag                           Predicted tag (string)
    confidence                             Confidence associated to prediction
    =====================================  =====================================
    """
    
    fm = face_models
    if face_models is None:
        
        fm = FaceModels(params)

    start_time = cv2.getTickCount()
    
    label = -1
    tag = -1
    confidence = -1
    error = None
    
    train_histograms = fm.model.getMatVector("histograms")
    
    train_labels = fm.model.getMat("labels")
    
    w, h = face.shape
           
    lbp_radius = c.LBP_RADIUS
    lbp_neighbors = c.LBP_NEIGHBORS
    lbp_grid_x = c.LBP_GRID_X
    lbp_grid_y = c.LBP_GRID_Y
    use_NBNN = ce.USE_NBNN
    use_weighted_regions = ce.USE_WEIGHTED_REGIONS

    if params is not None:
        if c.LBP_RADIUS_KEY is not None:
            lbp_radius = params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY is not None:
            lbp_neighbors = params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY is not None:
            lbp_grid_x = params[c.LBP_GRID_X_KEY]
        if c.LBP_GRID_Y_KEY is not None:
            lbp_grid_y = params[c.LBP_GRID_Y_KEY]
        if ce.USE_NBNN_KEY in params:
            use_NBNN = params[ce.USE_NBNN_KEY]

        if ce.USE_WEIGHTED_REGIONS_KEY in params:
            use_weighted_regions = params[ce.USE_WEIGHTED_REGIONS_KEY]
           
    query_model = cv2.createLBPHFaceRecognizer(
    lbp_radius, lbp_neighbors, 
    lbp_grid_x, lbp_grid_y)
        
    query_model.train(
    np.asarray([np.asarray(face, dtype=np.uint8)]), np.asarray([0]))
    
    query_histograms = query_model.getMatVector("histograms")
    
    query_hist = query_histograms[0][0]
    
    len_query_hist = int(len(query_hist))
    
    query_hist_EMD = np.zeros((len_query_hist,
                               2))
    
    for i in range(0, len_query_hist):
        
        query_hist_EMD[i][0] = query_hist[i]
        query_hist_EMD[i][1] = i + 1
    
    USE_EMD = False
    
    if use_NBNN:
        
        people_nr = fm.get_people_nr()
                
        [label, confidence] = recognize_with_NBNN_distance(
        query_hist, train_histograms, train_labels, w, h, people_nr)
        
    else:
        
        diff_list = []
    
        for i in range(0,
                       len(train_histograms)):
            
            train_hist = train_histograms[i][0]
            
            len_train_hist = int(len(train_hist))
            
            train_hist_EMD = np.zeros((len_train_hist,
                                       2))
            
            for j in range(0, len_train_hist):

                train_hist_EMD[j][0] = train_hist[j]
                train_hist_EMD[j][1] = i + 1
            
            diff = 0
            
            if use_weighted_regions:
                
                diff = calculate_w_reg_distance(query_hist, train_hist)
                                
            else:
        
                if USE_EMD:
 
                    # Convert from numpy array to CV_32FC1 Mat
                    a64 = cv.fromarray(query_hist_EMD)
                    a32 = cv.CreateMat(a64.rows, a64.cols, cv.CV_32FC1)
                    cv.Convert(a64, a32)
                    
                    b64 = cv.fromarray(train_hist_EMD)
                    b32 = cv.CreateMat(b64.rows, b64.cols, cv.CV_32FC1)
                    cv.Convert(b64, b32)
                    
                    # Calculate Earth Mover's distance
                    diff = cv.CalcEMD2(a32, b32, cv.CV_DIST_L2)
                    
                else:
                
                    diff = cv2.compareHist(
                    query_hist, train_hist, cv.CV_COMP_CHISQR)  
                
            diff_list.append(diff)  
            
        # Get K nearest histograms
        
        idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]
        
        K = ce.KNN_NEIGHBORS
        
        if ce.CALCULATE_K_FROM_FEATURES:
            
            nr_features = 2 ** lbp_neighbors * lbp_grid_x * lbp_grid_y
            
            K = int(round(math.sqrt(nr_features)))
        
        if K == 1:
            
            idx = idxs[0]
            
            confidence = diff_list[idx]
            
            label = train_labels[idx][0]
            
        else:
            
            nearest_labels_list = []
            
            # K cannot be greater than number of training items
            if K > len(idxs):
                
                K = len(idxs)
            
            for i in range(0, K):
                
                idx = idxs[i]
                
                diff = diff_list[idx]
                
                label = train_labels[idx][0]
                
                if ce.USE_WEIGHTED_KNN:
                
                    weight = 0
                    
                    if diff < 1:
                        
                        weight = 100
                        
                    elif diff > 100:
                        
                        weight = 1
                        
                    else:
                        
                        weight = int(round(100 / diff))
                    
                    for t in range(0, weight):
                    
                        nearest_labels_list.append(label)
                        
                else:
                    
                    nearest_labels_list.append(label)
                
            # Find most common label in K nearest ones
            data = Counter(nearest_labels_list)
            
            label = data.most_common(1)[0][0]
            
            counter = data.most_common(1)[0][1]
            
            confidence = counter
        
    tag = fm.get_tag(label)

    # TEST ONLY
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence)

    rec_time_in_clocks = cv2.getTickCount() - start_time
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency()

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {c.ELAPSED_CPU_TIME_KEY: rec_time_in_seconds, c.ERROR_KEY: error,
              c.ASSIGNED_LABEL_KEY: label, c.ASSIGNED_TAG_KEY: tag,
              c.CONFIDENCE_KEY: confidence}

    if show_results:
        cv2.imshow(str(label), face)
        cv2.waitKey(0) 

    return result


def recognize_face_base(face, face_models, params=None, show_results=False):
    """
    Recognize given face using
    the face recognition model saved as one file,
    comparison between histograms is carried out by OpenCV

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters
                   to be used for the face recognition (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False) recognized face

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  ==============
    Key (params)                                  Value                                     Default value
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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
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

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    elapsed_CPU_time                       The elapsed CPU time in seconds
    error                                  A string specifying an error
                                           condition,
                                           or None if no errors occurred
    assigned_label                         Predicted label (integer)
    assigned_tag                           Predicted tag (string)
    confidence                             Confidence associated to prediction
    =====================================  =====================================
    """

    fm = face_models
    if face_models is None:
        fm = FaceModels(params)

    start_time = cv2.getTickCount()

    [label, confidence] = fm.model.predict(np.asarray(face, dtype=np.uint8))

    tag = fm.get_tag(label)

    # TEST ONLY
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence)

    rec_time_in_clocks = cv2.getTickCount() - start_time
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency()

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {c.ELAPSED_CPU_TIME_KEY: rec_time_in_seconds, c.ERROR_KEY: '',
              c.ASSIGNED_LABEL_KEY: label, c.ASSIGNED_TAG_KEY: tag,
              c.CONFIDENCE_KEY: confidence}

    if show_results:
        cv2.imshow(str(label), face)
        cv2.waitKey(0) 

    return result

    
def recognize_face(face, face_models, params=None, show_results=False):
    """
    Recognize given face using the face recognition model

    :type face: OpenCV image
    :param face: face to be recognized

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face recognition (see table)

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  ==============
    Key (params)                                  Value                                     Default value
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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
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

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    elapsed_CPU_time                       The elapsed CPU time in seconds
    error                                  A string specifying an error
                                           condition,
                                           or None if no errors occurred
    assigned_label                         Predicted label (integer)
    assigned_tag                           Predicted tag (string)
    confidence                             Confidence associated to prediction
    =====================================  =====================================
    """
    
    result = None
    
    use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS
    
    if (params is not None) and (ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY in params):
        use_one_file = params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY]

    if use_one_file:
        result = recognize_face_from_models_file(
        face, face_models, params, show_results)
        # result = recognize_face_base(
        # face, face_models, params, show_results)

    else:
        result = recognize_face_from_model_files(
        face, face_models, params, show_results)

    return result
