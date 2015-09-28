import constants as c
import copy
import cv2
import cv2.cv as cv
import math
import numpy as np
import os
import pickle as pk
import sys
import yaml
 

def add_oval_mask(image):
    """
    Add oval mask to image

    :type image: OpenCV image
    :param image: image to be masked

    :rtype: OpenCV image
    :returns: masked image
    """
    
    center_x = int(c.CROPPED_FACE_WIDTH / 2)
    center_y = int(c.CROPPED_FACE_HEIGHT / 2)
    center = (center_x, center_y)
    
    axe_x = center_x + int(center_x / 4)
    axe_y = center_y + int(center_x / 4)
    line_w = int(center_x / 2)
    axes = (axe_x, axe_y)
    cv2.ellipse(image, center, axes, 0, 0, 360, (0, 0, 0), line_w)
    
    return image


def aggregate_frame_results(frames, fm=None, tags=None, params=None):
    """
    Aggregate results of several frames
    
    :type frames: list of dictionaries
    :param frames: frames to be aggregated
    
    :type fm: FaceModels
    :param fm: face model
    
    :type tags: list
    :param tags: list of possible tags
    
    :type params: dictionary
    :param params: configuration parameters (see table)

    :rtype: list
    :returns: a [final_tag, final_confidence, pct] list,
              where final_tag is the predicted tag,
              final_confidence is the corresponding confidence
              and pct is the percentage of frames assigned to
              the most probable tag

    ========================  ==================================================  ==============
    Key                       Value                                               Default value
    ========================  ==================================================  ==============
    use_majority_rule         If True, in aggregating results from several        True
                              frames, final tag is the tag that was assigned
                              to the majority of frames
    use_mean_confidence_rule  If True, in aggregating results from several        False
                              frames, final tag is the tag that received
                              the minimum value for the mean of confidences
                              among frames
    use_min_confidence_rule   If True, in aggregating results from several        True
                              frames,final tag is the tag that received
                              the minimum confidence value
    ========================  ==================================================  ==============
    """

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
  
    people_nr = 0
    if fm is not None:
        
        people_nr = fm.get_people_nr()
        tags = fm.get_labels()
    
    elif tags is not None:
        
        people_nr = len(tags)

    for tag in tags:
        assigned_frames_nr_dict[tag] = 0
        confidence_lists_dict[tag] = []

    for frame in frames:
        assigned_tag = frame[c.ASSIGNED_TAG_KEY]
        assigned_frames_nr_dict[assigned_tag] += 1
        confidence = frame[c.CONFIDENCE_KEY]
        confidence_lists_dict[assigned_tag].append(confidence)

    # Take final decision on tag

    final_tag = c.UNDEFINED_TAG
    final_confidence = -1
    max_frames_nr = 0
    
    use_majority_rule = c.USE_MAJORITY_RULE
    use_mean_conf_rule = c.USE_MEAN_CONFIDENCE_RULE
    use_min_conf_rule = c.USE_MIN_CONFIDENCE_RULE
    
    if params is not None:
        if c.USE_MAJORITY_RULE_KEY in params:
            use_majority_rule = params[c.USE_MAJORITY_RULE_KEY]
        if c.USE_MEAN_CONFIDENCE_RULE_KEY in params:
            use_mean_conf_rule = params[c.USE_MEAN_CONFIDENCE_RULE_KEY]
        if c.USE_MIN_CONFIDENCE_RULE_KEY in params:
            use_min_conf_rule = params[c.USE_MIN_CONFIDENCE_RULE_KEY]
        
    if use_majority_rule:

        candidate_tags_list = []
        
        for tag in tags:
            
            assigned_frames_nr = assigned_frames_nr_dict[tag]

            if assigned_frames_nr > max_frames_nr:

                # There is one tag that has more occurrences that the others
                candidate_tags_list = [tag]
                max_frames_nr = assigned_frames_nr

            elif assigned_frames_nr == max_frames_nr:

                # There are two or more tags that have
                # the same number of occurrences
                candidate_tags_list.append(tag)

        if len(candidate_tags_list) >= 1:

            final_tag = candidate_tags_list[0]

            if use_min_conf_rule:

                final_confidence = float(
                    np.min(confidence_lists_dict[final_tag]))

                for i in range(1, len(candidate_tags_list)):

                    min_confidence = float(
                        np.min(confidence_lists_dict[candidate_tags_list[i]]))

                    if min_confidence < final_confidence:

                        final_tag = candidate_tags_list[i]

                        final_confidence = min_confidence

            elif use_mean_conf_rule:

                final_confidence = float(
                    np.mean(confidence_lists_dict[final_tag]))

                for i in range(1, len(candidate_tags_list)):

                    mean_confidence = float(
                        np.mean(confidence_lists_dict[candidate_tags_list[i]]))

                    if mean_confidence < final_confidence:

                        final_tag = candidate_tags_list[i]

                        final_confidence = mean_confidence
            else:
                print('Warning! Method is not available')

    else:
        if use_min_conf_rule:

            if people_nr > 0:

                final_tag = tags[0]

                if len(confidence_lists_dict[final_tag]) > 0:

                    final_confidence = float(
                        np.min(confidence_lists_dict[final_tag]))

                for tag in tags:

                    if len(confidence_lists_dict[tag]) > 0:

                        min_confidence = float(
                            np.min(confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or
                                (min_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = min_confidence

        elif use_mean_conf_rule:

            if people_nr > 0:

                final_tag = tags[0]

                if len(confidence_lists_dict[final_tag]) > 0:

                    final_confidence = float(
                        np.mean(confidence_lists_dict[final_tag]))

                for tag in tags:

                    if len(confidence_lists_dict[tag]) > 0:

                        mean_confidence = float(
                            np.mean(confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or
                                (mean_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = mean_confidence
            
        else:
            print('Warning! Method is not available')
        
    # Percentage of frames assigned to the most probable tag
    pct = float(max_frames_nr) / len(frames)           
                        
    return [final_tag, final_confidence, pct]


def check_eye_pos(eye_left, eye_right, face_bbox, params=None):
    """
    Check eye positions

    :type eye_left: tuple
    :param eye_left: position of left eye, given as tuple (x,y)

    :type eye_right: tuple
    :param eye_right: position of right eye, given as tuple (x,y)

    :type face_bbox: tuple
    :param face_bbox: face bounding box,
                      given as a (x, y, width, height) tuple

    :type params: dictionary
    :param params: configuration parameters (see table)

    :rtype: boolean
    :returns: True if eye positions are good, False otherwise

    ========================  ==================================================  ==============
    Key                       Value                                               Default value
    ========================  ==================================================  ==============
    min_eye_distance          Minimum distance between eyes (in % of the width    0.25
                              of the face bounding box)
    max_eye_angle             Maximum inclination of the line connecting          0.125
                              the eyes (in % of pi radians)
    ========================  ==================================================  ==============
    """

    check = False

    min_distance_pct = c.MIN_EYE_DISTANCE
    max_angle_pct = c.MAX_EYE_ANGLE

    if params is not None:
        if c.MIN_EYE_DISTANCE_KEY in params:
            min_distance_pct = params[c.MIN_EYE_DISTANCE_KEY]
        if c.MAX_EYE_ANGLE_KEY in params:
            max_angle_pct = params[c.MAX_EYE_ANGLE_KEY]

    x1 = eye_left[0]

    y1 = eye_left[1]

    x2 = eye_right[0]

    y2 = eye_right[1]

    # Check that distance between eyes is greater than a minimum
    face_width = float(face_bbox[2])

    min_distance = face_width * min_distance_pct

    eye_distance = math.hypot(x2 - x1, y2 - y1)

    if eye_distance >= min_distance:

        # Check that the inclination of the line connecting
        # the eyes is less than a maximum
        max_angle = math.pi * max_angle_pct

        angle = math.asin(abs(y2 - y1) / eye_distance)

        if angle <= max_angle:

            check = True

    return check


def compare_clothes(
        model1, model2, db_path_1, db_path_2, face_conf,
        intra_dist1=None, params=None, k=1):
    """
    Compare two cloth models

    :type model1: list
    :param model1: list of color histograms of clothes

    :type model2: list
    :param model2: list of color histograms of clothes to be compared
                   with those of model1

    :type db_path_1: string
    :param db_path_1: path containing file with list
                      of color histograms of clothes
                      (used if model1 is None)

    :type db_path_2: string
    :param db_path_2: path containing file with list of color histograms
                    of clothes to be compared with those of db_path_1
                    (used if model2 is None)

    :type face_conf: float
    :param face_conf: confidence with face recognition

    :type intra_dist1: float
    :param intra_dist1: mean of intra distances for db_path_1,
                         if already computed

    :type params: dictionary
    :param params: configuration parameters (see table)

    :type k: float
    :param k: multiplier for intra distances for calculating threshold

    :rtype: tupe
    :returns: a (sim, dist_ratio) tuple,
              where sim is True if the two models are similar
              and dist is the distance between the two models,
              normalized to the threshold value

    ===========================================  =================================  ==============
    Key                                          Value                              Default value
    ===========================================  =================================  ==============
    conf_threshold                               Maximum distance between face      14.0
                                                 features of two face tracks
                                                 for merging them in the same
                                                 cluster
    clothes_check_method                         Method for comparing clothes of    'max'
                                                 the two cloth models
                                                 ('min', 'mean' or 'max')
    use_3_bboxes_in_clothing_recognition         If True, bounding box for clothes  False
                                                 is divided into 3 parts
    conf_threshold_for_clothing_recognition      Minimum distance between face      8.0
                                                 features of two face tracks
                                                 for considering clothes
    nr_of_HSV_channels_in_clothing_recognition   Number of HSV channels used        3
                                                 in clothing recognition (1-3)
    variable_clothing_threshold                  If True, a variable threshold      False
                                                 for clothing recognition is used
    ===========================================  =================================  ==============
    """
    
    # Method for comparing clothes ('min', 'mean' or 'max')
    method = c.CLOTHES_CHECK_METHOD
    
    # True if 3 bboxes per frame are used  
    used_3_bboxes = c.CLOTHING_REC_USE_3_BBOXES
    
    # Threshold for merging face tracks (threshold_face high)
    conf_threshold = c.CONF_THRESHOLD
    
    # Threshold for using clothing recognition (threshold_face low)
    clothes_conf_th = c.CLOTHES_CONF_THRESH

    # Number of used HSV channels
    hsv_channels = c.CLOTHING_REC_HSV_CHANNELS_NR
    
    # True if threshold for clothing is variable
    variable_clothing_th = c.VARIABLE_CLOTHING_THRESHOLD
    
    if params is not None:
        if c.CONF_THRESHOLD_KEY in params:
            conf_threshold = params[c.CONF_THRESHOLD_KEY]
        if c.CLOTHES_CHECK_METHOD_KEY in params:
            method = params[c.CLOTHES_CHECK_METHOD_KEY]
        if c.CLOTHING_REC_USE_3_BBOXES_KEY in params:
            used_3_bboxes = params[c.CLOTHING_REC_USE_3_BBOXES_KEY]
        if c.CLOTHES_CONF_THRESH_KEY in params:
            clothes_conf_th = params[c.CLOTHES_CONF_THRESH_KEY]
        if c.CLOTHING_REC_HSV_CHANNELS_NR_KEY in params:
            hsv_channels = params[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]
        if c.VARIABLE_CLOTHING_THRESHOLD_KEY in params:
            variable_clothing_th = params[c.VARIABLE_CLOTHING_THRESHOLD_KEY]
    
    sim = False
    dist_ratio = -1
          
    if model1 is None:
        if os.path.isfile(db_path_1):
            with open(db_path_1, 'r') as f1:
                model1 = pk.load(f1)

    if model2 is None:
        if os.path.isfile(db_path_2):
            with open (db_path_2, 'r') as f2:
                model2 = pk.load(f2)

    if model1 and model2:

        if intra_dist1 is None:

            intra_dist1 = get_mean_intra_distance(
                model1, used_3_bboxes, hsv_channels)

        intra_dist2 = get_mean_intra_distance(
            model2, used_3_bboxes, hsv_channels)

        dist = get_mean_inter_distance(
            model1, model2, used_3_bboxes, hsv_channels)

        chosen_value = 0

        if variable_clothing_th:
            k = (conf_threshold - clothes_conf_th) / (
            face_conf - clothes_conf_th)

        if method.lower() == 'min':

            chosen_value = k * min(intra_dist1, intra_dist2)

        elif method.lower() == 'mean':

            chosen_value = k * np.mean(intra_dist1, intra_dist2)

        elif method.lower() == 'max':

            chosen_value = k * max(intra_dist1, intra_dist2)

        else:

            print('Warning! Method for comparing clothes not available')

        if dist < chosen_value:

            sim = True

        dist_ratio = dist / chosen_value

    return sim, dist_ratio


def detect_eyes_in_image(image, eye_cascade_classifier):
    """
    Detect eyes in image by using a single cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type eye_cascade_classifier: CascadeClassifier
    :param eye_cascade_classifier: classifier to be used for the eye detection

    :rtype: list
    :returns: a (left_eye_x, left_eye_y, right_eye_x, right_eye_y)
              list containing eye positions

    """

    min_neighbors = 0
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING

    image_width = len(image[0, :])
    image_height = len(image[:, 0])
    
    eyes = eye_cascade_classifier.detectMultiScale(
        image, haar_scale, min_neighbors, haar_flags)

    # Divide between left eyes and right eyes
    left_eyes = []
    right_eyes = []
    for eye in eyes:
        eye_x = eye[0]
        eye_y = eye[1]
        eye_w = eye[2]
        eye_h = eye[3]
        eye_center_x = eye_x + (eye_w / 2)
        eye_center_y = eye_y + (eye_h / 2)
        if eye_center_y < (image_height / 2):
            if eye_center_x < (image_width / 2):
                left_eyes.append(eye)
            else:
                right_eyes.append(eye)

    left_eye = get_best_eye(left_eyes)

    right_eye = get_best_eye(right_eyes)

    # Get max eyes confidence

    eyes_final_list = []
    if (left_eye is not None) and (right_eye is not None):
        eyes_final_list = [left_eye, right_eye]
    
    return eyes_final_list


def detect_mouth_in_image(image, mouth_cascade_classifier):
    """
    Detect mouth in image by using cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type mouth_cascade_classifier: CascadeClassifier
    :param mouth_cascade_classifier: classifier to be used for the detection

    :rtype: list
    :returns: list of mouths detected ,
              represented as (x, y, width, height) tuples
    """
    
    min_neighbors = 1
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING
    
    mouth_list = []
    
    if mouth_cascade_classifier is not None:
        mouth_list = mouth_cascade_classifier.detectMultiScale(
            image, haar_scale, min_neighbors, haar_flags)
        
    else:
        print('Mouth cascade classifier must be provided')
        
    return mouth_list


def detect_nose_in_image(image, nose_cascade_classifier):
    """
    Detect nose in image by using cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type nose_cascade_classifier: CascadeClassifier
    :param nose_cascade_classifier: classifier to be used for the detection

    :rtype: list
    :returns: list of noses detected,
              represented as (x, y, width, height) tuples
    """
    
    min_neighbors = 5
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING
    
    nose_list = []
    
    if nose_cascade_classifier is not None:
        nose_list = nose_cascade_classifier.detectMultiScale(
            image, haar_scale, min_neighbors, haar_flags)
        
    else:
        print('Nose cascade classifier must be provided')
        
    return nose_list


def find_dominant_region(hist, kernel_size):
    """
    Find dominant region in given histogram

    :type hist: numpy array
    :param hist: histogram

    :type kernel_size: odd integer
    :param kernel_size: size of kernel used to smooth histogram

    :rtype: list
    :returns: a (left_idx, right_idx) tuple indicating the locations
              of dominant region borders
    """
    
    # Smooth histogram to eliminate local minima
    
    hist_item = cv2.GaussianBlur(hist, (kernel_size, kernel_size), 0)

    # Find maximum location
    
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(hist_item, mask=None)

    max_idx = int(max_loc[1])
    
    # Find minimum adjacent neighbors to maximum location
    
    # Find left minimum
    left_idx = max_idx
    
    last_hist_value = max_val
    for left_idx in range(max_idx - 1, -1, -1):
        
        hist_value = hist_item.item((left_idx, 0))
        
        if hist_value > last_hist_value:
            
            break
        
        else:
            
            last_hist_value = hist_value
            
    # Find right minimum
    
    hist_size = hist_item.shape[0]
    
    right_idx = max_idx
    
    last_hist_value = max_val
    for right_idx in range(max_idx + 1, hist_size, 1):
        
        hist_value = hist_item.item((right_idx, 0))
        
        if hist_value > last_hist_value:
            
            break
            
        else:
            
            last_hist_value = hist_value
            
    locs = (left_idx, right_idx)
    
    return locs


def get_best_eye(eyes_list):
    """
    Get best eye from given list

    :type eyes_list: list
    :param eyes_list: list of eyes given as a (x, y, width, height) tuple

    :rtype: list or None
    :returns: best eye
    """
    # Calculate confidence for each eye rectangle
    eyes_confidences = []

    eye_counter = 0
    for eye in eyes_list:
        eye_x1 = eye[0]
        eye_y1 = eye[1]
        eye_w = eye[2]
        eye_h = eye[3]
        eye_x2 = eye_x1 + eye_w
        eye_y2 = eye_y1 + eye_h

        eye_area = eye_w * eye_h
        
        confidence = 0

        other_eye_counter = 0
        for other_eye in eyes_list:

            if not(other_eye_counter == eye_counter):
                other_eye_x1 = other_eye[0]
                other_eye_y1 = other_eye[1]
                other_eye_w = other_eye[2]
                other_eye_h = other_eye[3]
                other_eye_x2 = other_eye_x1 + other_eye_w
                other_eye_y2 = other_eye_y1 + other_eye_h

                int_x1 = max(eye_x1, other_eye_x1)
                int_y1 = max(eye_y1, other_eye_y1)
                int_x2 = min(eye_x2, other_eye_x2)
                int_y2 = min(eye_y2, other_eye_y2)

                if (int_x2 > int_x1) and (int_y2 > int_y1):
                    int_width = int_x2 - int_x1
                    int_height = int_y2 - int_y1
                    int_area = int_width * int_height
                    confidence += float(int_area) / float(eye_area)

            other_eye_counter += 1

        eyes_confidences.append(confidence)

        eye_counter += 1

    if len(eyes_confidences) > 0:
        eye_index = eyes_confidences.index(max(eyes_confidences))
        return eyes_list[eye_index]
    else:
        return None


def get_dominant_color(hsv_image, kernel_size):
    """
    Get dominant color from image

    :type hsv_image: OpenCV image in HSV space
    :param hsv_image: image to be analyzed

    :type kernel_size: odd integer
    :param kernel_size: size of kernel used to smooth histogram

    :rtype: OpenCV mask
    :return: mask for dominant color
    """

    mask = cv2.inRange(
        hsv_image, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    h_hist = cv2.calcHist([hsv_image], [0], mask, [255], [0, 256])
    
    (h_left_idx, h_right_idx) = find_dominant_region(h_hist, kernel_size)
    
    mask_s = cv2.inRange(
    hsv_image, np.array((h_left_idx, 0., 0.)), 
    np.array((h_right_idx, 255., 255.)))
    
    s_hist = cv2.calcHist([hsv_image], [1], mask_s, [255], [0, 256])
    
    (s_left_idx, s_right_idx) = find_dominant_region(s_hist, kernel_size)
    
    mask_v = cv2.inRange(
    hsv_image, np.array((h_left_idx, s_left_idx, 0.)), 
    np.array((h_right_idx, s_right_idx, 255.)))
    
    v_hist = cv2.calcHist([hsv_image], [2], mask_v, [255], [0, 256])
    
    (v_left_idx, v_right_idx) = find_dominant_region(v_hist, kernel_size)
    
    final_mask = cv2.inRange(
    hsv_image, np.array((h_left_idx, s_left_idx, v_left_idx)), 
    np.array((h_right_idx, s_right_idx, v_right_idx)))
    
    return final_mask


def get_hist_difference(image, prev_hists):
    """
    Get difference between histograms of given image
    and given histograms.

    :type image: OpenCV image
    :param image: image to be analyzed

    :type prev_hists: list
    :param prev_hists: histograms to be compared with histograms
                       of image

    :rtype: list
    :returns: a [difference, histograms] list, where histograms are
              the histograms calculated on given image
    """
    
    tot_diff = None
    
    hists = None
    
    if image is not None:
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
        mask = cv2.inRange(
            hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
        hists = []
        
        for ch in range(0, 3):
            
            hist = cv2.calcHist(
            [hsv], [ch], mask, [256], [0, 255])
            
            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
            
            hists.append(hist)
            
        if prev_hists is not None:
            
            tot_diff = 0
        
            for ch in range(0, 3):
                
                diff = abs(cv2.compareHist(
                hists[ch], prev_hists[ch], cv.CV_COMP_CHISQR))
                
                tot_diff = tot_diff + diff
            
    else:
        
        hists = None
            
    return [tot_diff, hists]


def get_image_score(image):
    """
    Get a score for this image.
    Best images have lower scores

    :type image: OpenCV image
    :param image: image to be checked

    :rtype: float
    :returns: score
    """
    score = get_image_symmetry(image)
    
    return score


def get_image_symmetry(image):
    """
    Get an indication of image symmetry.
    Lower the value greater the symmetry

    :type image: OpenCV image
    :param image: image to be checked

    :rtype: float
    :returns: symmetry value
    """
    
    moments = cv2.moments(image)
    
    nu_3_0 = moments['nu30']
    
    return abs(nu_3_0)


def get_mean_inter_distance(model1, model2, use_3_bboxes=False, hsv_channels=3):
    """
    Calculate mean distance between histograms in two cloth models

    :type model1: list
    :param model1: list of color histograms

    :type model2: list
    :param model2: list of color histograms
                   to be compared with those of model1

    :type use_3_bboxes: boolean
    :param use_3_bboxes: True if 3 bboxes per frame are used

    :type hsv_channels: integer
    :param hsv_channels: number of used HSV channels

    :rtype: float
    :returns: distance value
    """
    
    min_distance = 0
    
    counter1 = 0
    len_model1 = len(model1)
    len_model2 = len(model2)
    mins_list = []
    
    for counter1 in range(0, len_model1):
        
        hists1 = model1[counter1]
        
        diff_list = []
        
        counter2 = 0
        
        for counter2 in range(0, len_model2):
            
            hists2 = model2[counter2]
            
            tot_diff = 0
            
            if use_3_bboxes:
                
                # For every bounding box in the same frame
                for i in range(0, 3):
                
                    hists1_i = hists1[i]
                    
                    hists2_i = hists2[i] 
                    
                    # For every color channel
                    for ch in range(0, hsv_channels):
                        
                        diff = abs(cv2.compareHist(
                        hists1_i[ch], hists2_i[ch], cv.CV_COMP_CHISQR))
                        
                        tot_diff = tot_diff + diff     
                
            else:
    
                # For every color channel
                for ch in range(0, hsv_channels):
                    
                    diff = abs(cv2.compareHist(
                    hists1[ch], hists2[ch], cv.CV_COMP_CHISQR))
                    
                    tot_diff = tot_diff + diff  
                
            diff_list.append(tot_diff)
            
        if len(diff_list) > 0:
            
            # Get minimum distance between considered frame in model1 
            # and all frames in model2
            model_min = min(diff_list)
            mins_list.append(model_min)
    
    if len(mins_list) > 0:
    
            min_distance = min(mins_list)
    
    return min_distance 


def get_mean_intra_distance(model, used_3_bboxes=False, hsv_channels=3):
    """
    Calculate mean distance between histograms in cloth model

    :type model: list
    :param model: list of color histograms

    :type used_3_bboxes: boolean
    :param used_3_bboxes: True if 3 bboxes per frame are used

    :type hsv_channels: integer
    :param hsv_channels: number of used HSV channels

    :rtype: float
    :returns: distance value
    """
    
    mean = 0
    
    counter = 0
    len_model = len(model)
    
    means_list = []
    
    for counter in range(0, len_model):
        
        hists = model[counter]
        
        diff_list = []
        
        for sub_counter in range(counter + 1, len_model):
            
            sub_hists = model[sub_counter]
        
            tot_diff = 0
            
            if used_3_bboxes:
                
                # For every bounding box in the same frame
                for i in range(0, 3):

                    hists_i = hists[i]
                    
                    sub_hists_i = sub_hists[i] 
                    
                    # For every color channel
                    for ch in range(0, hsv_channels):
                        
                        diff = abs(cv2.compareHist(
                        hists_i[ch], sub_hists_i[ch], cv.CV_COMP_CHISQR))
                        
                        tot_diff = tot_diff + diff
            
            else:
    
                # For every color channel
                for ch in range(0, hsv_channels):
                    diff = abs(cv2.compareHist(
                    hists[ch], sub_hists[ch], cv.CV_COMP_CHISQR))
                    tot_diff = tot_diff + diff
        
            diff_list.append(tot_diff)
            
        if len(diff_list) > 0:
            
            model_mean = np.mean(diff_list)
            
            means_list.append(model_mean)
            
    if len(means_list) > 0:
    
            mean = np.mean(means_list)
    
    return mean


def get_time_intervals(time_list, min_sep):
    """
    Get time intervals from given list of time instants

    :type time_list: list
    :param time_list: list of time instants

    :type min_sep: float
    :param min_sep: minimum separation between time intervals

    :rtype: list
    :return: a list of (start, duration) tuples,
             where start indicates the starting time of the time interval
             and duration the duration of the time interval
    """

    time_intervals = []

    # Order time instants
    ord_time_list = sorted(time_list)

    counter = 0
    prev_time_instant = 0
    start = 0
    for time_instant in ord_time_list:
        if counter == 0:
            start = time_instant
            prev_time_instant = time_instant
            counter += 1
        else:
            if time_instant < (prev_time_instant + min_sep):
                prev_time_instant = time_instant
                counter += 1
                continue
            else:
                # Time interval ends
                duration = prev_time_instant - start
                if duration > 0:
                    interval = (start, duration)
                    time_intervals.append(interval)
                # New time interval
                start = time_instant
                prev_time_instant = time_instant

        counter += 1

    # Save last time interval
    duration = prev_time_instant - start
    if duration > 0:
        interval = (start, duration)
        time_intervals.append(interval)

    return time_intervals


def get_shot_changes(diff_list, half_w_size, std_mult):
    """
    Get frame counters for shot cuts

    :type diff_list: list
    :param diff_list: list with frame differences

    :type half_w_size: integer
    :param half_w_size: size of half sliding window

    :type std_mult: float
    :param std_mult: multiplier for standard deviation for calculating
                     threshold

    :rtype: list
    :returns: list of shot cuts
    """
    
    shot_changes = []
    
    # Counter for frames from last shot change
    frames_from_change = 0
    
    # Counter for all frames. It starts at 1 for considering first frame
    counter = 1
    
    for diff in diff_list:
        
        # No sufficient frames remain
        if counter > (len(diff_list) - half_w_size - 1):
            
            break
        
        # No new decisions are made 
        # until half_w_size frames have elapsed
        if frames_from_change < half_w_size:

            frames_from_change += 1
            
        else:
            
            # Left half of window
            w_left = diff_list[(counter - half_w_size): (counter - 1)]
            
            # Right half of window
            w_right = diff_list[(counter + 1): counter + half_w_size]

            frame_is_cut = is_cut(diff, w_left, w_right, std_mult)
            
            if frame_is_cut:
                
                shot_changes.append(counter)
                
                frames_from_change = 0

        counter += 1
        
    return shot_changes


def is_cut(diff, w_left, w_right, std_mult):
    """
    Check if given difference represents a shot cut

    :type diff: float
    :param diff: value of frame difference to be checked

    :type w_left: list
    :param w_left: left half of sliding window

    :type w_right: list
    :param w_right: right half of sliding window

    :type std_mult: float
    :param std_mult: multiplier for standard deviation for calculating
                     threshold

    :rtype: boolean
    :returns: True if given difference represents a shot cut,
              False otherwise
    """
    
    result = False
    
    # The middle sample must be the maximum in the window
    if (diff > max(w_left)) and (diff > max(w_right)):
        
        threshold_left = np.mean(w_left) + (std_mult * np.std(w_left))
    
        threshold_right = np.mean(w_right) + (std_mult * np.std(w_right))
                          
        if (diff > threshold_left) and (diff > threshold_right):
            
            result = True
            
    return result


def is_rect_enclosed(rect1, rect2):
    """
    Check if rectangle is inside another rectangle

    :type rect1: tuple
    :param rect1: first rectangle given as a (x, y, width, height) tuple

    :type rect2: tuple
    :param rect2: second rectangle given as a (x, y, width, height) tuple

    :rtype: boolean
    :return: True if rect1 is inside rect2, False otherwise
    """
    x11 = rect1[0]
    y11 = rect1[1]
    x12 = x11 + rect1[2]
    y12 = y11 + rect1[3] 
    
    x21 = rect2[0]
    y21 = rect2[1]
    x22 = x21 + rect2[2]
    y22 = y21 + rect2[3]
    
    if (x11 >= x21) and (y11 >= y21) and (x12 <= x22) and (y12 <= y22):
        return True
    else:
        return False


def is_rect_similar(rect1, rect2, min_int_area):
    """
    Check if a rectangle is similar to another rectangle.
    Returns True if rect 1 is similar to rect 2.

    :type rect1: tuple
    :param rect1: first rectangle given as a (x, y, width, height) tuple

    :type rect2: tuple
    :param rect2: second rectangle given as a (x, y, width, height) tuple

    :type min_int_area: float
    :param min_int_area: minimum area of intersection between the two
                         rectangles (related to area of the smallest one)
                         for considering them similar

    :rtype: tuple
    :return: a (similar, int_area, int_area_pct) tuple,
             where similar is True
             if rectangles are similar and False otherwise,
             int_area is the area of the intersection,
             int_area_pct is the ratio between the area of the intersection
             and the area of the biggest rectangle
    """
    
    similar = False
    
    x11 = rect1[0]
    y11 = rect1[1]
    w1 = rect1[2]
    x12 = x11 + w1
    h1 = rect1[3]
    y12 = y11 + h1
    x21 = rect2[0]
    y21 = rect2[1]
    w2 = rect2[2]
    x22 = x21 + w2
    h2 = rect2[3]
    y22 = y21 + h2
    
    int_x1 = max(x11, x21)
    int_y1 = max(y11, y21)
    int_x2 = min(x12, x22)
    int_y2 = min(y12, y22)

    int_area = 0
    int_area_pct = 0
    
    if (int_x1 < int_x2) and (int_y1 < int_y2):
        # The two rectangles intersect

        rect1_area = w1 * h1

        rect2_area = w2 * h2

        max_rect_area = max(rect1_area, rect2_area)
        
        if is_rect_enclosed(rect1, rect2):
            # rect1 is inside rect2
            similar = True
            int_area = rect1_area
            
        elif is_rect_enclosed(rect2, rect1):
            # rect2 is inside rect1
            similar = True
            int_area = rect2_area

        else:

            min_rect_area = min(rect1_area, rect2_area)
            
            int_area = (int_x2 - int_x1) * (int_y2 - int_y1)
            
            if float(int_area) > (min_int_area * float(min_rect_area)):
                # Intersection area more than min_int_area times 
                # the area of the smallest rectangle 
                # between the two being compared
                
                similar = True

        int_area_pct = float(int_area) / max_rect_area
                
    return similar, int_area, int_area_pct


def is_there_a_corresponding_detection(segment_frame, people_list):
    """
    Find if in given list of people there is a face detection
    corresponding to bounding box in given frame

    :type segment_frame: dictionary
    :param segment_frame: a frame

    :type people_list: list
    :param people_list: list of people

    :rtype: boolean
    :returns: True if a corresponding detection was found, False otherwise
    """

    segment_frame_name = segment_frame[c.SAVED_FRAME_NAME_KEY]
    segment_frame_bbox = segment_frame[c.DETECTION_BBOX_KEY]
    for person_dict in people_list:
        segments = person_dict[c.SEGMENTS_KEY]
        for segment in segments:
            frames = segment [c.FRAMES_KEY]
            for frame in frames:
                frame_name = frame[c.SAVED_FRAME_NAME_KEY]
                is_detected = frame[c.DETECTED_KEY]
                if is_detected:
                    if segment_frame_name == frame_name:
                        # Same frame
                        frame_bbox = segment_frame[c.DETECTION_BBOX_KEY]
                        if is_rect_similar(
                                segment_frame_bbox, frame_bbox,
                                c.DET_MIN_INT_AREA):
                            return True
    return False


def load_YAML_file(file_path):
    """
    Load YAML file.

    :type file_path: string
    :param file_path: path of YAML file to be loaded

    :rtype: dictionary or list
    :returns: the contents of the file
    """
    
    try:
        
        with open(file_path, 'r') as stream:
            data = yaml.load(stream)
            return data
           
    except IOError as e:
        error_str = "I/O error({0}): {1}".format(e.errno, e.strerror)
        print error_str
        return None

    except:
         print "Unexpected error:", sys.exc_info()[0]
         return None

def merge_consecutive_segments(segments, min_duration):
    """
    Merge consecutive video segments

    :type segments: list
    :param segments: list of dictionaries representing video segments

    :type min_duration: float
    :param min_duration: minimum duration of segments (in seconds)

    :rtype: tuple
    :returns: a (merged_segments, tot_dur) tuple,
              where merged_segments is the list of merged segments
              and tot_dur the total duration of segments
    """
    
    merged_segments = []
    
    # Order segments by starting time
    ord_segments = []
    
    idx = 0
    
    while len(segments) > 0:
        
        counter = 0
        
        min_start = sys.maxint
        for segment_dict in segments:
            
            start = segment_dict[c.SEGMENT_START_KEY]
                                
            if start < min_start:
                
                min_start = start
                
                idx = counter

            counter += 1
                
        ord_segments.append(segments[idx])

        del segments[idx]
        
    # Merge consecutive segments
        
    tot_dur = 0
        
    prev_end = -sys.maxint
    first_start = 0
    tot_seg_dur = 0
    last_segment_appended = True
    
    # Iterate through ordered segments
    
    counter = 0

    segment_dict = {}

    new_segment_dict = {}

    for segment_dict in ord_segments:

        start = segment_dict[c.SEGMENT_START_KEY]
        
        dur = segment_dict[c.SEGMENT_DURATION_KEY]
        
        # First segment
        if counter == 0:
            
            first_start = start
            
            tot_seg_dur = dur
            
            prev_end = start + dur

            # New segment
            new_segment_dict = copy.deepcopy(segment_dict)

            # List of frames in new segment
            list_of_frames = copy.deepcopy(segment_dict[c.FRAMES_KEY])
            
            last_segment_appended = False

            counter += 1

            continue

        # Merge consecutive segments
        if start < (prev_end + (min_duration * 1000.0)):
            
            tot_seg_dur = (
            tot_seg_dur + (start - prev_end) + dur)

            # Add to list frames from this segment
            list_of_frames.extend(copy.deepcopy(segment_dict[c.FRAMES_KEY]))

            last_segment_appended = False
        
        else:

            tot_dur = tot_dur + tot_seg_dur
            
            # TODO DELETE
            # simple_seg_dict = {c.SEGMENT_START_KEY: first_start,
            #                   c.SEGMENT_DURATION_KEY: tot_seg_dur}

            new_segment_dict[c.SEGMENT_START_KEY] = first_start
            new_segment_dict[c.SEGMENT_DURATION_KEY] = tot_seg_dur
            new_segment_dict[c.FRAMES_KEY] = list_of_frames

            # merged_segments.append(simple_seg_dict)
            merged_segments.append(new_segment_dict)

            # New segment
            new_segment_dict = copy.deepcopy(segment_dict)

            # List of frames in new segment
            list_of_frames = copy.deepcopy(segment_dict[c.FRAMES_KEY])

            first_start = start
            
            tot_seg_dur = dur
            
            last_segment_appended = True
        
        prev_end = start + dur

        counter += 1
        
    if not last_segment_appended:
        
        new_segment_dict[c.SEGMENT_START_KEY] = first_start
        new_segment_dict[c.SEGMENT_DURATION_KEY] = tot_seg_dur
        new_segment_dict[c.FRAMES_KEY] = list_of_frames

        merged_segments.append(new_segment_dict)
        
        tot_dur = tot_dur + tot_seg_dur
        
    return merged_segments, tot_dur
        

def merge_near_idxs(idxs, diff_list, min_dist):
    """
    Merge near indexes according to given list of histogram differences

    :type idxs: list
    :param idxs: list of indexes

    :type diff_list: list
    :param diff_list: list of histogram differences

    :type min_dist: integer
    :param min_dist: minimum distance between two indexes

    :rtype: list
    :returns: list of indexes
    """

    sorted_idxs = sorted(idxs)

    last_idx = len(diff_list) - 1

    item_deleted = True

    while item_deleted:

        counter = 0
        prev = 0
        item_deleted = False
        
        for i in sorted_idxs:

            print i

            if i < (prev + min_dist):

                if (prev == 0) or (diff_list[i] <= diff_list[prev]):

                    del sorted_idxs[counter]
                    item_deleted = True
                    break

                else:

                    if diff_list[i] > diff_list[prev]:

                        del sorted_idxs[counter - 1]
                        item_deleted = True
                        break

            elif i > (last_idx - min_dist):

                del sorted_idxs[counter]
                item_deleted = True
                break
                 
            prev = i

            counter += 1

    return sorted_idxs
        

def normalize_illumination(img):
    """
    Apply Tan & Triggs normalization to image

    :type img: OpenCV image
    :param img: image to be normalized

    :rtype: OpenCV image or None
    :returns: normalized image
    """
    
    if img is not None:
        # Gamma correction
        gamma = 0.2
        
        width, height = img.shape
        
        nr_pels = width * height
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = round(math.pow(float(pel) / 255, gamma) * 255)
                img[col, row] = new_pel
        
        # Difference of Gaussians
        sigma_1 = 1.0
        dog1 = cv2.GaussianBlur(img, (0, 0), sigma_1)
        sigma_2 = 2.0
        dog2 = cv2.GaussianBlur(img, (0, 0), sigma_2)
        
        img = dog1 - dog2
        
        # Contrast equalization
        
        eq_img = cv2.equalizeHist(img)
        
        a = 0.1
        
        tau = 10.0
        
        img_mean = cv2.mean(img)[0]
        
        pel_sum = 0
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = math.pow(pel, a)
                pel_sum += new_pel
                
        mean = float(pel_sum) / nr_pels
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = pel / math.pow(mean, 1.0 / a)
                img[col, row] = new_pel
                
        pel_sum = 0
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = math.pow(min(pel, tau), a)
                pel_sum += new_pel
                
        mean = float(pel_sum) / nr_pels
        
        # Used in order to avoid overflow errors
        max_pel_value = 1000
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = pel / math.pow(mean, 1.0 / a)
                if new_pel > max_pel_value:
                    new_pel = max_pel_value
                img[col, row] = new_pel
                
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = 0.5 * math.tanh(pel / tau) + 0.5
                img[col, row] = new_pel * 255
        
        return img
        
    else:
        
        return None
                
        
def save_YAML_file(file_path, data):
    """
    Save YAML file

    :type file_path: string
    :param file_path: path of YAML file to be saved

    :type data: dictionary or list
    :param data: data to be saved

    :rtype: boolean
    :returns: a boolean indicating the result of the write operation
    """

    with open(file_path, 'w') as stream:
        # result = stream.write(
        # yaml.dump(data, default_flow_style=False))
        result = yaml.dump(data, stream, default_flow_style=False)
        return result


def similar_face_tracks(
        face_track1, face_track2, max_diff, min_int_area, min_pct):
    """
    Check if two given face tracks are similar

    :type face_track1: dictionary
    :param face_track1: first face track

    :type face_track2: dictionary
    :param face_track2: second face track

    :type max_diff: integer
    :param max_diff: maximum difference between start and end of
                     two face tracks (in milliseconds)

    :type min_int_area: float
    :param min_int_area: minimum value for intersection area
                         between two bounding boxes for considering them similar
                         (in % of the area of the smallest bounding box)

    :type min_pct: float
    :param min_pct: minimum percentage of frames in which there is
                    a corresponding bounding box
                    for considering the two tracks similar

    :rtype: boolean
    :returns: True if two face tracks are similar, False otherwise
    """

    sim = False

    # Check if start and end of the two face tracks correspond
    start1 = face_track1[c.SEGMENT_START_KEY]
    start2 = face_track2[c.SEGMENT_START_KEY]
    if abs(start1 - start2) <= max_diff:
        dur1 = face_track1[c.SEGMENT_DURATION_KEY]
        end1 = start1 + dur1
        dur2 = face_track2[c.SEGMENT_DURATION_KEY]
        end2 = start2 + dur2
        if abs(dur1 - dur2) <= max_diff:

            sim_bboxes = 0.0
            same_frames = 0.0
            # Search same frames
            for frame1 in face_track1:
                frame_name1 = frame1[c.SAVED_FRAME_NAME_KEY]
                for frame2 in face_track2:
                    frame_name2 = frame2[c.SAVED_FRAME_NAME_KEY]
                    if frame_name1 == frame_name2:
                        # Same frame
                        same_frames += 1

                        # Check bounding boxes
                        bbox1 = frame1[c.DETECTION_BBOX_KEY]
                        bbox2 = frame2[c.DETECTION_BBOX_KEY]
                        if is_rect_similar(bbox1, bbox2, min_int_area):
                            sim_bboxes += 1

            if same_frames > 0:
                pct = sim_bboxes / same_frames
                if pct > min_pct:
                    sim = True

                    # TODO DELETE TEST ONLY
                    print('face_track1', face_track1)
                    print('face_track2', face_track2)
                    print('len(face_track1)', len(face_track1))
                    print('len(face_track2)', len(face_track2))
                    base_path = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction\fic.02.mpg\Face_extraction\Frames'
                    for frame in face_track1:
                        frame_name = frame[c.SAVED_FRAME_NAME_KEY]
                        full_path = os.path.join(base_path, frame_name)
                        img = cv2.imread(full_path)
                        face_bbox = frame[c.BBOX_KEY]
                        face_x0 = face_bbox[0]
                        face_y0 = face_bbox[1]
                        face_width = face_bbox[2]
                        face_height = face_bbox[3]
                        face_x1 = face_x0 + face_width
                        face_y1 = face_y0 + face_height
                        cv2.rectangle(
                        img, (face_x0, face_y0), (face_x1, face_y1),
                        (255, 0, 0), 3, 8, 0)
                        cv2.imshow('face track 1', img)
                        cv2.waitKey(0)
                    for frame in face_track2:
                        frame_name = frame[c.SAVED_FRAME_NAME_KEY]
                        full_path = os.path.join(base_path, frame_name)
                        img = cv2.imread(full_path)
                        face_bbox = frame[c.BBOX_KEY]
                        face_x0 = face_bbox[0]
                        face_y0 = face_bbox[1]
                        face_width = face_bbox[2]
                        face_height = face_bbox[3]
                        face_x1 = face_x0 + face_width
                        face_y1 = face_y0 + face_height
                        cv2.rectangle(
                        img, (face_x0, face_y0), (face_x1, face_y1),
                        (255, 0, 0), 3, 8, 0)
                        cv2.imshow('face track 2', img)
                        cv2.waitKey(0)


    return sim




