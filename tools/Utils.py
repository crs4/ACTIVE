import cv2
import sys
import yaml
import numpy as np
import os
from Constants import *

FACE_CLASSIFIER = 'haarcascade_frontalface_alt2.xml';
EYE_CLASSIFIER = 'haarcascade_eye.xml';

def read_images(path, sz=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.

    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes

    Returns:
        A list [X,y]

            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
    """
    c = 0
    X,y = [], []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]

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
    stream = open(file_path, 'w');
    result = stream.write(yaml.dump(dictionary, default_flow_style = False));
    stream.close();
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
    haar_scale = 1.01;
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

