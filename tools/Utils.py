import cv2
import sys
import yaml
import numpy
import os
from Constants import *

FACE_CLASSIFIER = 'haarcascade_frontalface_alt2.xml';
EYE_CLASSIFIER = 'haarcascade_eye.xml';

def load_YAML_file(file_path):
    """Load YAML file.

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A dictionary with the contents of the file
    """
    with open(file_path, 'r') as stream:
        data = yaml.load(stream);
        return data;

def load_image_annotations(file_path):
    """Load YAML file with image .

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A list of dictionaries with the annotated images
    """
    data = load_YAML_file(file_path);

    images = data[ANNOTATIONS_FRAMES_KEY];
    return images;

def save_YAML_file(file_path, dictionary):
    """Save YAML file.

    Args:
        file_path = path of YAML file to be saved
        dictionary = dictionary with data to be saved

    Returns:
        A boolean indicating the result of the write operation
    """
    with open(file_path, 'w') as stream:
        result = stream.write(yaml.dump(dictionary, default_flow_style = False));
        return result;

# Load file with results of all experiments and return list of experiments
def load_experiment_results(filePath):
    data = load_YAML_file(filePath);
    experiments = data[EXPERIMENTS_KEY];
    return experiments

def detect_eyes_in_image(image, eye_cascade_classifier):
    '''
    Detect eyes in image using a single classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type eye_cascade_classifier: cascade classifier
    :param eye_cascade_classifier: classifier to be used for the detection

    '''

    min_neighbors = 0;
    haar_scale = 1.1;
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING;

    image_width = len(image[0,:]);
    image_height = len(image[:,0]);
    
    eyes = eye_cascade_classifier.detectMultiScale(image, haar_scale, min_neighbors, haar_flags);

    # Divide between left eyes and right eyes
    left_eyes = [];
    right_eyes = [];
    for eye in eyes:
        eye_x = eye[0];
        eye_y = eye[1];
        eye_w = eye[2];
        eye_h = eye[3];
        eye_center_x = eye_x + (eye_w / 2);
        eye_center_y = eye_y + (eye_h / 2);
        if(eye_center_y < (image_height / 2)):
            if(eye_center_x < (image_width / 2)):
                left_eyes.append(eye);
            else:
                right_eyes.append(eye);

    left_eye = get_best_eye(left_eyes);

    right_eye = get_best_eye(right_eyes);

    # Get max eyes confidence

    eyes_final_list = [];
    if(not(left_eye == None) and not(right_eye == None)):
        eyes_final_list = [left_eye, right_eye];
    
    return eyes_final_list;   

def get_best_eye(eyes_list):
    # Calculate confidence for each eye rectangle
    eyes_confidences = [];

    eye_counter = 0;
    for eye in eyes_list:
        eye_x1 = eye[0];
        eye_y1 = eye[1];
        eye_w = eye[2];
        eye_h = eye[3];
        eye_x2 = eye_x1 + eye_w;
        eye_y2 = eye_y1 + eye_h;

        eye_area = eye_w * eye_h;
        
        confidence = 0;

        other_eye_counter = 0;
        for other_eye in eyes_list:

            if(not(other_eye_counter == eye_counter)):
                other_eye_x1 = other_eye[0];
                other_eye_y1 = other_eye[1];
                other_eye_w = other_eye[2];
                other_eye_h = other_eye[3];
                other_eye_x2 = other_eye_x1 + other_eye_w;
                other_eye_y2 = other_eye_y1 + other_eye_h;

                int_x1 = max(eye_x1, other_eye_x1);
                int_y1 = max(eye_y1, other_eye_y1);
                int_x2 = min(eye_x2, other_eye_x2);
                int_y2 = min(eye_y2, other_eye_y2);

                if((int_x2 > int_x1) and (int_y2 > int_y1)):
                    int_width = int_x2 - int_x1;
                    int_height = int_y2 - int_y1;
                    int_area = int_width * int_height;
                    confidence = confidence + float(int_area)/float(eye_area);
                
            other_eye_counter = other_eye_counter + 1;

        eyes_confidences.append(confidence);
        
        eye_counter = eye_counter + 1;

    if(len(eyes_confidences) > 0):
        eye_index = eyes_confidences.index(max(eyes_confidences));
        return eyes_list[eye_index];
    else:
        return None;

def aggregate_frame_results(frames, fm):

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
    people_nr = fm.get_people_nr();

    for label in range(0, people_nr):
        tag = fm.get_label(label);
        assigned_frames_nr_dict[tag] = 0
        confidence_lists_dict[tag] = []

    #print(frames)

    for frame in frames:

        assigned_tag = frame[FACE_EXTRACTION_TAG_KEY]

        assigned_frames_nr_dict[assigned_tag] = assigned_frames_nr_dict[assigned_tag] + 1

        confidence = frame[FACE_EXTRACTION_CONFIDENCE_KEY]

        confidence_lists_dict[assigned_tag].append(confidence)

    # Take final decision on person

    final_tag = 'Undefined'
    final_confidence = -1
    if(USE_MAJORITY_RULE):
        max_frames_nr = 0
        candidate_tags_list = []
        
        for label in range(0, people_nr):
            
            tag = fm.get_label(label);
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

                final_confidence = float(numpy.min(confidence_lists_dict[final_tag]));

                for i in range(1, len(candidate_tags_list)):

                    min_confidence = float(numpy.min(confidence_lists_dict[candidate_tags_list[i]]));

                    if (min_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = min_confidence

            elif(USE_MEAN_CONFIDENCE_RULE):

                #print('\nCONFIDENCE LIST\n')
                #print(confidence_lists_dict[final_tag])

                final_confidence = float(numpy.mean(confidence_lists_dict[final_tag]));
                #print(candidate_tags_list)

                for i in range(1, len(candidate_tags_list)):

                    mean_confidence = float(numpy.mean(confidence_lists_dict[candidate_tags_list[i]]));

                    if (mean_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = mean_confidence
                        
    return [final_tag, final_confidence]
        

