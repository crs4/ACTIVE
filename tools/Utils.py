import cv2
import math
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
    Detect eyes in image using a single classifier

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

def aggregate_frame_results(frames, fm):

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
    people_nr = fm.get_people_nr()
    
    tags = fm.get_tags()
    
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

    final_tag = 'Undefined'
    final_confidence = -1
    if(USE_MAJORITY_RULE):
        max_frames_nr = 0
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
        
                        
    return [final_tag, final_confidence]
        
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
        FACE_RECOGNITION_RADIUS, 
        FACE_RECOGNITION_NEIGHBORS, 
        FACE_RECOGNITION_GRID_X, 
        FACE_RECOGNITION_GRID_Y)
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
                            delta_y = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
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
                
                cv2.imshow('prev_face', prev_face)
                cv2.waitKey(0)
                
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
                            
                            cv2.imshow('this_face', this_face)
                            cv2.waitKey(0)
                            
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

