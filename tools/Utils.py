import cv2
import cv2.cv as cv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time
import yaml
from Constants import * 

def load_YAML_file(file_path):
    """Load YAML file.

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A dictionary with the contents of the file
    """
    try:
        
        with open(file_path, 'r') as stream:
            data = yaml.load(stream)
            return data
           
    except:
        
        return None

def load_image_annotations(file_path):
    """Load YAML file with image .

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A list of dictionaries with the annotated images
    """
    data = load_YAML_file(file_path)
    
    if(data):
        
        images = data[ANNOTATIONS_FRAMES_KEY]
        return images
        
    else:
        
        print 'Unable to open', file_path
        return None

def save_YAML_file(file_path, dictionary):
    """Save YAML file.

    Args:
        file_path = path of YAML file to be saved
        dictionary = dictionary with data to be saved

    Returns:
        A boolean indicating the result of the write operation
    """
    with open(file_path, 'w') as stream:
        result = stream.write(yaml.dump(dictionary, default_flow_style = False))
        return result

# Load file with results of all experiments and return list of experiments
def load_experiment_results(filePath):
    data = load_YAML_file(filePath)
    experiments = data[EXPERIMENTS_KEY]
    return experiments

def detect_eyes_in_image(image, eye_cascade_classifier):
    '''
    Detect eyes in image by using a single cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type eye_cascade_classifier: cascade classifier
    :param eye_cascade_classifier: classifier to be used for the detection

    '''

    min_neighbors = 0
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING

    image_width = len(image[0,:])
    image_height = len(image[:,0])
    
    eyes = eye_cascade_classifier.detectMultiScale(image, haar_scale, min_neighbors, haar_flags)

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
        if(eye_center_y < (image_height / 2)):
            if(eye_center_x < (image_width / 2)):
                left_eyes.append(eye)
            else:
                right_eyes.append(eye)

    left_eye = get_best_eye(left_eyes)

    right_eye = get_best_eye(right_eyes)

    # Get max eyes confidence

    eyes_final_list = []
    if(not(left_eye == None) and not(right_eye == None)):
        eyes_final_list = [left_eye, right_eye]
    
    return eyes_final_list   

def get_best_eye(eyes_list):
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

            if(not(other_eye_counter == eye_counter)):
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

                if((int_x2 > int_x1) and (int_y2 > int_y1)):
                    int_width = int_x2 - int_x1
                    int_height = int_y2 - int_y1
                    int_area = int_width * int_height
                    confidence = confidence + float(int_area)/float(eye_area)
                
            other_eye_counter = other_eye_counter + 1

        eyes_confidences.append(confidence)
        
        eye_counter = eye_counter + 1

    if(len(eyes_confidences) > 0):
        eye_index = eyes_confidences.index(max(eyes_confidences))
        return eyes_list[eye_index]
    else:
        return None

def detect_mouth_in_image(image, mouth_cascade_classifier):
    '''
    Detect mouth in image by using cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type mouth_cascade_classifier: cascade classifier
    :param mouth_cascade_classifier: classifier to be used for the detection

    ''' 
    
    min_neighbors = 5
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING
    
    mouth_list = []
    
    if(mouth_cascade_classifier is not None):
        mouth_list = mouth_cascade_classifier.detectMultiScale(
            image, haar_scale, min_neighbors, haar_flags)
        
    else:
        print('Mouth cascade classifier must be provided')
        
    return mouth_list

def detect_nose_in_image(image, nose_cascade_classifier):
    '''
    Detect nose in image by using cascade classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type nose_cascade_classifier: cascade classifier
    :param nose_cascade_classifier: classifier to be used for the detection

    ''' 
    
    min_neighbors = 5
    haar_scale = 1.1
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING
    
    nose_list = []
    
    if(nose_cascade_classifier is not None):
        nose_list = nose_cascade_classifier.detectMultiScale(
            image, haar_scale, min_neighbors, haar_flags)
        
    else:
        print('Nose cascade classifier must be provided')
        
    return nose_list

def aggregate_frame_results(frames, fm = None, tags = None):

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
  
    people_nr = 0
    if(fm is not None):
        
        people_nr = fm.get_people_nr()
        tags = fm.get_tags()
    
    elif(tags is not None):
        
        people_nr = len(tags)
    
    for tag in tags:
        assigned_frames_nr_dict[tag] = 0
        confidence_lists_dict[tag] = []

    #print(frames)

    for frame in frames:

        assigned_tag = frame[ASSIGNED_TAG_KEY]

        assigned_frames_nr_dict[assigned_tag] = assigned_frames_nr_dict[assigned_tag] + 1

        confidence = frame[CONFIDENCE_KEY]

        confidence_lists_dict[assigned_tag].append(confidence)

    # Take final decision on person

    final_tag = UNDEFINED_TAG
    final_confidence = -1
    max_frames_nr = 0
    if(USE_MAJORITY_RULE):

        candidate_tags_list = []
        
        for tag in tags:
            
            assigned_frames_nr = assigned_frames_nr_dict[tag]

            if(assigned_frames_nr > max_frames_nr):

                # There is one tag that has more occurrences that the others
                candidate_tags_list = []
                candidate_tags_list.append(tag)
                max_frames_nr = assigned_frames_nr

            elif(assigned_frames_nr == max_frames_nr):

                # There are two or more tags that have the same number of occurrences
                candidate_tags_list.append(tag)

        if (len(candidate_tags_list) >= 1):

            final_tag = candidate_tags_list[0]

            if(USE_MIN_CONFIDENCE_RULE):

                final_confidence = float(np.min(confidence_lists_dict[final_tag]))

                for i in range(1, len(candidate_tags_list)):

                    min_confidence = float(np.min(confidence_lists_dict[candidate_tags_list[i]]))

                    if (min_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = min_confidence

            elif(USE_MEAN_CONFIDENCE_RULE):

                #print('\nCONFIDENCE LIST\n')
                #print(confidence_lists_dict[final_tag])

                final_confidence = float(np.mean(confidence_lists_dict[final_tag]))
                #print(candidate_tags_list)

                for i in range(1, len(candidate_tags_list)):

                    mean_confidence = float(np.mean(confidence_lists_dict[candidate_tags_list[i]]))

                    if (mean_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = mean_confidence
            else:
                print('Warning! Method is not available')

    else:
        if(USE_MIN_CONFIDENCE_RULE):

            if(people_nr > 0):

                final_tag = tags[0]

                if(len(confidence_lists_dict[final_tag]) > 0):

                    final_confidence = float(np.min(confidence_lists_dict[final_tag]))

                for tag in tags:

                    if(len(confidence_lists_dict[tag]) > 0):

                        min_confidence = float(np.min(confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or (min_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = min_confidence

        elif(USE_MEAN_CONFIDENCE_RULE):

            if(people_nr > 0):

                final_tag = tags[0]

                if(len(confidence_lists_dict[final_tag]) > 0):

                    final_confidence = float(np.mean(confidence_lists_dict[final_tag]))

                for tag in tags:

                    if(len(confidence_lists_dict[tag]) > 0):

                        mean_confidence = float(np.mean(confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or (mean_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = mean_confidence
            
        else:
            print('Warning! Method is not available')
        
    # Percentage of frames assigned to most probable tag 
    pct = float(max_frames_nr) / len(frames)           
                        
    return [final_tag, final_confidence, pct]
        
def normalize_illumination(img):
    
    if(img != None):
        # Gamma correction
        gamma = 0.2
        
        width, height = img.shape
        
        nr_pels = width * height
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = round(math.pow(float(pel)/255, gamma) * 255)
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
                pel_sum = pel_sum + new_pel
                
        mean = float(pel_sum) / nr_pels
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = pel / math.pow(mean, 1.0/a)
                img[col, row] = new_pel
                
        pel_sum = 0
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = math.pow(min(pel, tau), a)
                pel_sum = pel_sum + new_pel
                
        mean = float(pel_sum) / nr_pels
        
        # Used in order to avoid overflow errors
        max_pel_value = 1000
        
        for row in range(0, height):
            for col in range(0, width):
                pel = img[col, row]
                new_pel = pel / math.pow(mean, 1.0/a)
                if(new_pel > max_pel_value):
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
        
def save_model_file(X, y, db_file_name = None):
    
    if(len(y) > 0): 
        model=cv2.createLBPHFaceRecognizer(
        LBP_RADIUS, 
        LBP_NEIGHBORS, 
        LBP_GRID_X, 
        LBP_GRID_Y)
        model.train(np.asarray(X), np.asarray(y))
        model_folder = DB_MODELS_PATH
        
        if db_file_name is not None:
            
            model_folder = db_file_name
            if not os.path.exists(model_folder):
                os.makedirs(model_folder)
        
        model_file = model_folder + os.sep + str(y[0])
        model.save(model_file)
    
def is_rect_enclosed(rect1, rect2):
    """Check if rectangle is inside another rectangle

    Args:
        rect1 = first rectangle given as list (x, y, width, height)
        rect2 = second rectangle given as list (x, y, width, height)

    Returns:
        True if rect 1 is inside rect 2
    """ 
    x11 = rect1[0]
    y11 = rect1[1]
    x12 = x11 + rect1[2]
    y12 = y11 + rect1[3] 
    
    x21 = rect2[0]
    y21 = rect2[1]
    x22 = x21 + rect2[2]
    y22 = y21 + rect2[3]
    
    if((x11 >= x21) and (y11 >= y21)
        and (x12 <= x22) and (y12 <= y22)):
        return True
    else:
        return False
 
def is_rect_similar(rect1, rect2, min_int_area):
    """
    Check if a rectangle is similar to another rectangle
    Returns True if rect 1 is similar to rect 2

    :type rect1: list
    :param rect1: first rectangle given as list (x, y, width, height)
    
    :type rect2: list
    :param rect2: second rectangle given as list (x, y, width, height)    
    
    :type min_int_area: float
    :param min_int_area: minimum area of intersection between the two 
    rectangles (related to area of the smallest one) for considering
    them similar  
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
    
    int_x1 = max(x11,x21)
    int_y1 = max(y11,y21)
    int_x2 = min(x12,x22)
    int_y2 = min(y12,y22)
    
    if((int_x1 < int_x2) and (int_y1 < int_y2)):
        # The two rectangles intersect
        
        if(is_rect_enclosed(rect1,rect2)
        or is_rect_enclosed(rect2,rect1)):
            # One rectangle is inside the other
            
            similar = True
            
        else:
            
            rect1_area = w1 * h1
            
            rect2_area = w2 * h2
            
            min_rect_area = min(rect1_area, rect2_area)
            
            int_area = (int_x2 - int_x1) * (int_y2 - int_y1)
            
            if(float(int_area) > (min_int_area * float(min_rect_area))):
                # Intersection area more than 0.5 times the area 
                # of the smallest rectangle between the two 
                # being compared
                
                similar = True
                
    return similar
                
        
def track_faces(frames, fm):
    
    segments = []

    tracking_frame_counter = 0
    
    for frame in frames:

        faces = frame[FACES_KEY]

        elapsed_video_s = frame[ELAPSED_VIDEO_TIME_KEY]

        if(len(faces) != 0):

            face_counter = 0
            for face in faces:

                segment_dict = {}

                segment_frame_counter = 1

                prev_bbox = face[BBOX_KEY]

                segment_frames_list = []

                segment_frame_dict = {}

                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                segment_frame_dict[FRAME_COUNTER_KEY] = tracking_frame_counter

                segment_frame_dict[ASSIGNED_TAG_KEY] = face[ASSIGNED_TAG_KEY]

                segment_frame_dict[CONFIDENCE_KEY] = face[CONFIDENCE_KEY]

                segment_frame_dict[BBOX_KEY] = prev_bbox

                segment_frames_list.append(segment_frame_dict)

                del frames[tracking_frame_counter][FACES_KEY][face_counter]

                sub_frame_counter = tracking_frame_counter + 1

                prev_frame_counter = tracking_frame_counter

                # Search face in subsequent frames and add good bounding boxes to segment
                # Bounding boxes included in this segment must not be considered by other segments

                for subsequent_frame in frames[sub_frame_counter :]:

                    # Consider only successive frames or frames whose maximum distance is MAX_FRAMES_WITH_MISSED_DETECTION + 1
                    if((sub_frame_counter > (prev_frame_counter + MAX_FRAMES_WITH_MISSED_DETECTION + 1))):

                        segment_frame_counter = segment_frame_counter - MAX_FRAMES_WITH_MISSED_DETECTION - 1

                        break;

                    sub_faces = subsequent_frame[FACES_KEY]

                    elapsed_video_s = subsequent_frame[ELAPSED_VIDEO_TIME_KEY]

                    if(len(sub_faces) != 0):

                        sub_face_counter = 0
                        for sub_face in sub_faces:

                            # Calculate differences between the two detections
                    
                            prev_bbox_x = prev_bbox[0]
                            prev_bbox_y = prev_bbox[1]
                            prev_bbox_w = prev_bbox[2]

                            bbox = sub_face[BBOX_KEY]

                            bbox_x = bbox[0]
                            bbox_y = bbox[1]
                            bbox_w = bbox[2]

                            delta_x = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
                            delta_y = abs(bbox_y - prev_bbox_y)/float(prev_bbox_w)
                            delta_w = abs(bbox_w - prev_bbox_w)/float(prev_bbox_w)

                            #Check if delta is small enough
                            if((delta_x < MAX_DELTA_PCT_X) and (delta_y < MAX_DELTA_PCT_Y) and (delta_w < MAX_DELTA_PCT_W)):

                                prev_bbox = bbox

                                segment_frame_dict = {}

                                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                                segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter

                                segment_frame_dict[ASSIGNED_TAG_KEY] = sub_face[ASSIGNED_TAG_KEY]

                                segment_frame_dict[CONFIDENCE_KEY] = sub_face[CONFIDENCE_KEY]

                                segment_frame_dict[BBOX_KEY] = bbox

                                segment_frames_list.append(segment_frame_dict)

                                del frames[sub_frame_counter][FACES_KEY][sub_face_counter]

                                prev_frame_counter = sub_frame_counter

                                consecutive_frames_with_missed_detection = 0

                                break; #Do not consider other faces in the same frame

                        sub_face_counter = sub_face_counter + 1
                        
                    sub_frame_counter = sub_frame_counter + 1

                    segment_frame_counter = segment_frame_counter + 1

                # Aggregate results from all frames in segment
                [final_tag, final_confidence] = aggregate_frame_results(segment_frames_list, fm)

                segment_dict[ASSIGNED_TAG_KEY] = final_tag

                segment_dict[CONFIDENCE_KEY] = final_confidence

                segment_dict[FRAMES_KEY] = segment_frames_list

                print('segment_frame_counter: ', segment_frame_counter)

                segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = segment_frame_counter

                segments.append(segment_dict)

                face_counter = face_counter + 1
                
        tracking_frame_counter = tracking_frame_counter + 1
        
    return segments

def track_faces_with_LBP(frames, fm):
    
    segments = []

    tracking_frame_counter = 0
    
    for frame in frames:

        faces = frame[FACES_KEY]

        elapsed_video_s = frame[ELAPSED_VIDEO_TIME_KEY]

        if(len(faces) != 0):

            face_counter = 0
            for face in faces:

                segment_dict = {}

                segment_frame_counter = 1

                prev_face = face[FACE_KEY]
                
                #cv2.imshow('prev_face', prev_face)
                #cv2.waitKey(0)
                
                prev_bbox = face[BBOX_KEY]

                segment_frames_list = []

                segment_frame_dict = {}

                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                segment_frame_dict[FRAME_COUNTER_KEY] = tracking_frame_counter

                segment_frame_dict[ASSIGNED_TAG_KEY] = face[ASSIGNED_TAG_KEY]

                segment_frame_dict[CONFIDENCE_KEY] = face[CONFIDENCE_KEY]

                segment_frame_dict[BBOX_KEY] = prev_bbox

                segment_frames_list.append(segment_frame_dict)

                del frames[tracking_frame_counter][FACES_KEY][face_counter]
                
                # Calculate LBP histograms from face
                X = []
                X.append(np.asarray(prev_face, dtype = np.uint8))
                c = [0]
                model = cv2.createLBPHFaceRecognizer(
                LBP_RADIUS,
                LBP_NEIGHBORS,
                LBP_GRID_X,
                LBP_GRID_Y)
                model.train(np.asarray(X), np.asarray(c))

                sub_frame_counter = tracking_frame_counter + 1

                prev_frame_counter = tracking_frame_counter

                # Search face in subsequent frames and add good bounding boxes to segment
                # Bounding boxes included in this segment must not be considered by other segments
                
                continue_tracking = True

                for subsequent_frame in frames[sub_frame_counter :]:

                    # Consider only successive frames or frames whose maximum distance is MAX_FRAMES_WITH_MISSED_DETECTION + 1
                    if((sub_frame_counter > (prev_frame_counter + MAX_FRAMES_WITH_MISSED_DETECTION + 1))):

                        segment_frame_counter = segment_frame_counter - MAX_FRAMES_WITH_MISSED_DETECTION - 1

                        break;

                    sub_faces = subsequent_frame[FACES_KEY]

                    elapsed_video_s = subsequent_frame[ELAPSED_VIDEO_TIME_KEY]

                    if(len(sub_faces) != 0):

                        sub_face_counter = 0
                        continue_tracking = False
                        for sub_face in sub_faces:

                            # Calculate differences between the two detections

                            this_face = sub_face[FACE_KEY]
                            
                            [lbl, conf] = model.predict(np.asarray(this_face, dtype = np.uint8))

                            print 'conf =', conf # TEST ONLY
                            
                            #cv2.imshow('this_face', this_face)
                            #cv2.waitKey(0)
                            
                            #Check if confidence is low enough
                            if(conf < STOP_TRACKING_THRESHOLD):
                                
                                # Calculate LBP histograms from face
                                X = []
                                X.append(np.asarray(this_face, dtype = np.uint8))
                                c = [0]
                                model = cv2.createLBPHFaceRecognizer(
                                LBP_RADIUS,
                                LBP_NEIGHBORS,
                                LBP_GRID_X,
                                LBP_GRID_Y)
                                model.train(np.asarray(X), np.asarray(c))
                                
                                continue_tracking = True

                                segment_frame_dict = {}

                                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                                segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter

                                segment_frame_dict[ASSIGNED_TAG_KEY] = sub_face[ASSIGNED_TAG_KEY]

                                segment_frame_dict[CONFIDENCE_KEY] = sub_face[CONFIDENCE_KEY]

                                segment_frame_dict[BBOX_KEY] = sub_face[BBOX_KEY]

                                segment_frames_list.append(segment_frame_dict)

                                del frames[sub_frame_counter][FACES_KEY][sub_face_counter]

                                prev_frame_counter = sub_frame_counter

                                consecutive_frames_with_missed_detection = 0

                                break; #Do not consider other faces in the same frame

                        sub_face_counter = sub_face_counter + 1
                        
                    sub_frame_counter = sub_frame_counter + 1

                    segment_frame_counter = segment_frame_counter + 1
                    
                    if(not continue_tracking):
                        
                        break

                # Aggregate results from all frames in segment
                [final_tag, final_confidence] = aggregate_frame_results(segment_frames_list, fm)

                segment_dict[ASSIGNED_TAG_KEY] = final_tag

                segment_dict[CONFIDENCE_KEY] = final_confidence

                segment_dict[FRAMES_KEY] = segment_frames_list

                print('segment_frame_counter: ', segment_frame_counter)

                segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = segment_frame_counter

                segments.append(segment_dict)

                face_counter = face_counter + 1
                
        tracking_frame_counter = tracking_frame_counter + 1
        
    return segments
    
def add_oval_mask(image):
    
    center_x = int(CROPPED_FACE_WIDTH / 2)
    center_y = int(CROPPED_FACE_HEIGHT / 2)
    center = (center_x, center_y)
    
    axe_x = center_x + int(center_x / 4)
    axe_y = center_y + int(center_x / 4)
    line_w = int(center_x / 2)
    axes = (axe_x, axe_y)
    cv2.ellipse(image, center, axes, 0, 0, 360, (0, 0, 0), line_w)
    
    return image


def get_shot_changes(diff_list, half_w_size, std_mult):
    '''
    Get frame counters for shot changes
    
    :type diff_list: list
    :param diff_list: list with frame differences
    
    :type half_w_size:integer
    :param half_w_size: size of half sliding window 
    
    :type std_mult: float
    :param std_mult: multiplier for standard deviation for calculating
    threshold
    '''
    
    shot_changes = []
    
    # Counter for frames from last shot change
    frames_from_change = 0
    
    # Counter for all frames. It starts at 1 for considering first frame
    counter = 1
    
    for diff in diff_list:
        
        # No sufficient frames remain
        if(counter > (len(diff_list) - half_w_size - 1)):
            
            break
        
        # No new decisions are made 
        # until half_w_size frames have elapsed
        if(frames_from_change < half_w_size):
            
            frames_from_change = frames_from_change + 1
            
        else:
            
            # Left half of window
            w_left = diff_list[(counter - half_w_size) : (counter - 1)]
            
            # Right half of window
            w_right = diff_list[(counter + 1) : counter + half_w_size]
            
            #print('counter',counter)
            frame_is_cut = is_cut(diff, w_left, w_right, std_mult)
            
            if(frame_is_cut):
                
                shot_changes.append(counter)
                
                frames_from_change = 0
            
        counter = counter + 1   
        
    return shot_changes
        
        
def is_cut(diff, w_left, w_right, std_mult):
    '''
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
    '''
    
    result = False
    
    # The middle sample must be the maximum in the window
    if((diff > max(w_left)) and (diff > max(w_right))):
        
        threshold_left = np.mean(w_left) + (
                         std_mult * np.std(w_left))
    
        threshold_right = np.mean(w_right) + (
                          std_mult * np.std(w_right))
                          
        if((diff > threshold_left) and (diff > threshold_right)):
            
            #print('threshold_left', threshold_left)
            #print('threshold_right', threshold_right)
            
            std_mult_left = (diff - np.mean(w_left)) / np.std(w_left)
            #print('std mult left', std_mult_left)
            std_mult_right = (diff - np.mean(w_right)) / np.std(w_right)
            #print('std mult right', std_mult_right)
            
            w_left.append(diff)
            w_left.extend(w_right)
            #print('w_left', w_left)
            #plt.plot(w_left)
            #plt.show() 
            
            result = True
            
    return result
    

def get_shot_changes_old(diff_list, start_idx, min_dist):
    '''
    Get frame counters for shot changes
    
    :type diff_list: list
    :param diff_list: list with histogram differences
    
    :type start_idx: integer
    :param start_idx: start of this list in original list
    
    :type min_dist: integer
    :param min_dist: minimum distance between two indexes    
    ''' 
    all_idxs = []
    
    # Do not consider segments whose duration is less than min_dist
    if(len(diff_list) < min_dist):
        
        return all_idxs
    
    #print(diff_list)
    #print('start_idx', start_idx)
    #print 'len(list):', len(diff_list)
    
    #plt.plot(diff_list)
    #plt.show() 
    
    mean = np.mean(diff_list)
    std = np.std(diff_list)
    
    #if(True):
    if(std > mean):
        
        threshold = mean + 1 * std

        #print 'mean = ', mean

        #print 'std = ', std

        #print 'threshold = ', threshold 
        
        #plt.plot(diff_list)
        #plt.show() 
        
        idxs = get_idxs_over_thresh(diff_list, start_idx, threshold)
        
        all_idxs.extend(idxs)
        
        sub_start_idx = 0
        
        for idx in idxs:
            
            print('idx', idx)
            
            sub_idx = idx - start_idx
            
            sub_list = diff_list[sub_start_idx:sub_idx]

            sub_sub_start_idx = start_idx + sub_start_idx

            sub_idxs = get_shot_changes(
            sub_list, sub_sub_start_idx, min_dist)
            
            all_idxs.extend(sub_idxs)
            
            sub_start_idx = sub_idx + 1
            
        # Check last part of list
        if(len(idxs) > 0):
            sub_list = diff_list[sub_start_idx:]
    
            sub_sub_start_idx = start_idx + sub_start_idx
    
            sub_idxs = get_shot_changes(
            sub_list, sub_sub_start_idx, min_dist)
                
            all_idxs.extend(sub_idxs)
            
    sorted_idxs = merge_near_idxs(all_idxs, diff_list, min_dist)
    
    # Add 1 to obtain frame indexes 
    # (differences start from second frame)
    
    counter = 0
    for i in sorted_idxs:
        
        sorted_idxs[counter] = sorted_idxs[counter] + 1
        counter = counter + 1
    
    return sorted_idxs
    

def get_idxs_over_thresh(lst, start_idx, threshold):
    '''
    Get indexes of list items that are greater than given threshold
    '''
    
    idxs = []
    
    counter = start_idx
    
    for item in lst:
        
        if(item > threshold):
            
            #print 'idx = ', counter
            
            idxs.append(counter)
            
        counter = counter + 1
        
    print('idxs', idxs)   
        
    return idxs


def merge_near_idxs(idxs, diff_list, min_dist):
    '''
    Merge near indexes according to diff_list
    :type idxs: list
    :param idxs: list of indexes

    :type diff_list: list
    :param diff_list: list of histogram differences

    :type min_dist: integer
    :param min_dist: minimum distance between two indexes
    '''

    sorted_idxs = sorted(idxs)

    last_idx = len(diff_list) - 1

    item_deleted = True

    while(item_deleted):

        counter = 0
        prev = 0
        item_deleted = False
        
        for i in sorted_idxs:

            print i

            if(i < (prev + min_dist)):

                if((prev == 0) or (diff_list[i] <= diff_list[prev])):

                    del sorted_idxs[counter]
                    item_deleted = True
                    break

                else:

                    if(diff_list[i] > diff_list[prev]):

                        del sorted_idxs[counter - 1]
                        item_deleted = True
                        break

            elif(i > (last_idx - min_dist)):

                 del sorted_idxs[counter]
                 item_deleted = True
                 break
                 
            prev = i

            counter = counter + 1

    return sorted_idxs
    
    
def get_hist_difference(image, prev_hists):
    '''
    Get difference between histograms of given image 
    and given histograms.
    Returns difference and histograms of given image
    
    :type image: OpenCV image
    :param image: image to be analyzed
    
    :type prev_hists: list
    :param prev_hists: histograms to be compared with histograms
                       of image
    '''
    
    tot_diff = None
    
    hists = None
    
    if (image is not None):
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
        mask = cv2.inRange(hsv, 
        np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
        hists = []
        
        for ch in range(0, 3):
            
            hist = cv2.calcHist(
            [hsv], [ch], mask, [256], [0, 255])
            
            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
            
            hists.append(hist)
            
        if(prev_hists is not None):
            
            tot_diff = 0
        
            for ch in range(0, 3):
                
                diff = abs(cv2.compareHist(
                hists[ch], prev_hists[ch], cv.CV_COMP_CHISQR))
                
                tot_diff = tot_diff + diff
            
    else:
        
        hists = None
            
    return [tot_diff, hists]

