import cv2
import os
from Constants import *
from enum import Enum
from Utils import *
from sympy import Polygon, intersection

HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER = 'haarcascade_frontalface_alt.xml';
HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER = 'haarcascade_frontalface_alt_tree.xml';
HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER = 'haarcascade_frontalface_alt2.xml';
HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER = 'haarcascade_frontalface_default.xml';
HAARCASCADE_PROFILEFACE_CLASSIFIER = 'haarcascade_profileface.xml';
LBPCASCADE_FRONTALFACE_CLASSIFIER = 'lbpcascade_frontalface.xml';
LBPCASCADE_PROFILEFACE_CLASSIFIER = 'lbpcascade_profileface.xml';

class FaceDetectionAlgorithm(Enum):
    HaarCascadeFrontalFaceAlt = 1 # Haar cascade using haarcascade_frontalface_alt.xml
    HaarCascadeFrontalFaceAltTree = 2 # Haar cascade using haarcascade_frontalface_alt_tree.xml
    HaarCascadeFrontalFaceAlt2 = 3 # Haar cascade using haarcascade_frontalface_alt2.xml
    HaarCascadeFrontalFaceDefault = 4 # Haar cascade using haarcascade_frontalface_default.xml
    HaarCascadeProfileFace = 5 # Haar cascade using haarcascade_profileface.xml
    HaarCascadeFrontalAndProfileFaces = 6; # Haar cascade using both haarcascade_frontalface_alt.xml and haarcascade_profileface.xml
    LBPCascadeFrontalface = 7 # LBP cascade using lbpcascade_frontalface.xml
    LBPCascadeProfileFace = 8 # LBP cascade using lbpcascade_profileface.xml
    LBPCascadeFrontalAndProfileFaces = 9  # LBP cascade using both lbpcascade_frontalface.xml and lbpcascade_profileface.xml

class HaarCascadeFlag(Enum):
    DoCannyPruning = cv2.CASCADE_DO_CANNY_PRUNING;
    DoRoughSearch = cv2.CASCADE_DO_ROUGH_SEARCH;
    FindBiggestObject = cv2.CASCADE_FIND_BIGGEST_OBJECT;
    ScaleImage = cv2.CASCADE_SCALE_IMAGE;

def detect_faces_in_image(resource_path, params, show_results):
    '''
    Detect faces in image

    :type resource_path: string
    :param resource_path: path of image to be analyzed
    
    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face detection

    :type showResult: boolean
    :param showResult: show (true) or do not show (false) image with detected faces
    '''

    # Saving processing time for face detection
    start_time = cv2.getTickCount();

    result = {};

    # Open image
    file_check = os.path.isfile(resource_path);
    if(not(file_check)):
        print('File does not exist');
        return ;
    try:
        image = cv2.imread(resource_path, cv2.IMREAD_GRAYSCALE);

        # Load classifier files
        classifier_file = '';
        classifier_file_2 = '';
        use_one_classifier_file = True;

        # Algorithm to be used for the face detection
        algorithm = params[ALGORITHM_KEY];

        # Path of directory containing classifier files
        classifiers_folder_path = params[CLASSIFIERS_FOLDER_PATH_KEY] + '\\';

        if(algorithm == 'HaarCascadeFrontalFaceAlt'):
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER
        elif(algorithm == 'HaarCascadeFrontalFaceAltTree'):
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER;
        elif(algorithm == 'HaarCascadeFrontalFaceAlt2'):
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER;
        elif(algorithm == 'HaarCascadeFrontalFaceDefault'):
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER;
        elif(algorithm == 'HaarCascadeProfileFace'):
            classifier_file = classifiers_folder_path + HAARCASCADE_PROFILEFACE_CLASSIFIER;
        elif(algorithm == 'HaarCascadeFrontalAndProfileFaces'):
            use_one_classifier_file = False;
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER;
            classifier_file_2 = classifiers_folder_path + HAARCASCADE_PROFILEFACE_CLASSIFIER;
        elif(algorithm == 'LBPCascadeFrontalface'):
            classifier_file = classifiers_folder_path + LBPCASCADE_FRONTALFACE_CLASSIFIER;
        elif(algorithm == 'LBPCascadeProfileFace'):
            classifier_file = classifiers_folder_path + LBPCASCADE_PROFILEFACE_CLASSIFIER;
        elif(algorithm == 'LBPCascadeFrontalAndProfileFaces'):
            use_one_classifier_file = False;
            classifier_file = classifiers_folder_path + LBPCASCADE_FRONTALFACE_CLASSIFIER;
            classifier_file_2 = classifiers_folder_path + LBPCASCADE_PROFILEFACE_CLASSIFIER;
        else:
            print('\nAlgorithm is not available');
            return;

        faces = [];
        if(use_one_classifier_file):
            face_cascade_classifier = cv2.CascadeClassifier(classifier_file);

            if(face_cascade_classifier.empty()):
                print('Error loading cascade classifier file');
                return;
            else:
                if(algorithm == FaceDetectionAlgorithm.LBPCascadeProfileFace):
                    # lbpcascade_profileface classifier only detects faces rotated to the right,
                    # so it must be used on the original and on the flipped image
                    faces_from_orig_image = detect_faces_in_image_with_single_classifier(image, face_cascade_classifier, params);

                    # Flip image around y-axis
                    flipped_image = cv2.flip(image, 1);

                    faces_from_flipped_image = detect_faces_in_image_with_single_classifier(flipped_image, face_cascade_classifier, params);

                    # Transform coordinates of faces from flipped image
                    image_width = len(image[0,:]);

                    for i in range(len(faces_from_flipped_image)):
                        faces_from_flipped_image[i][0] = image_width + 1 - faces_from_flipped_image[i][0] - faces_from_flipped_image[i][2];

                    # Merge results
                    faces = merge_classifier_results(faces_from_orig_image, faces_from_flipped_image);

                else:
                    # Use classifier on original image only
                    faces = detect_faces_in_image_with_single_classifier(image, face_cascade_classifier, params);

        else:
            face_cascade_classifier_1 = cv2.CascadeClassifier(classifier_file);
            face_cascade_classifier_2 = cv2.CascadeClassifier(classifier_file_2);
            if(face_cascade_classifier_1.empty() | face_cascade_classifier_2.empty()):
                print('Error loading cascade classifier file');
                return;
            else:
                # Detect faces in image using first classifier
                facesFromClassifier1 = detect_faces_in_image_with_single_classifier(image, face_cascade_classifier_1, params);

                # Detect faces in image using second classifier
                facesFromClassifier2 = detect_faces_in_image_with_single_classifier(image, face_cascade_classifier_2, params);

                # Merge results
                faces = merge_classifier_results(facesFromClassifier1, facesFromClassifier2);

        detection_time_in_clocks = cv2.getTickCount() - start_time;
        detection_time_in_seconds = detection_time_in_clocks / cv2.getTickFrequency();

        # Populate dictionary with detected faces and elapsed CPU time 
        result[FACE_DETECTION_ELAPSED_CPU_TIME_KEY] = detection_time_in_seconds;
        result[FACE_DETECTION_ERROR_KEY] = '';
        result[FACE_DETECTION_FACES_KEY] = faces;

        # Create face images from original image
        face_images = [];
        for (x, y, width, height) in faces:
            face_image = image[y:y+height, x:x+width];
            face_images.append(face_image);

        result[FACE_DETECTION_FACE_IMAGES_KEY] = face_images;

        if(show_results):
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0);
                cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE);
                cv2.imshow('Result', image);
                cv2.waitKey(0);

    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    return result;

def detect_faces_in_image_with_single_classifier(image, face_cascade_classifier, params):
    '''
    Detect faces in image using a single classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type face_cascade_classifier: face cascade classifier
    :param face_cascade_classifier: classifier to be used for the detection

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for face detection
    '''
    haar_scale = params[SCALE_FACTOR_KEY];
    min_neighbors = params[MIN_NEIGHBORS_KEY];

    haar_flags_str = params[FLAGS_KEY];
    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING;
    if(haar_flags_str == 'DoRoughSearch'):
        haar_flags = cv2.CASCADE_DO_ROUGH_SEARCH;
    elif(haar_flags_str == 'FindBiggestObject'):
        haar_flags = cv2.CASCADE_FIND_BIGGEST_OBJECT;
    elif(haar_flags_str == 'ScaleImage'):
        haar_flags = cv2.CASCADE_SCALE_IMAGE;
    
    min_size = (params[MIN_SIZE_WIDTH_KEY], params[MIN_SIZE_HEIGHT_KEY]);
    faces = face_cascade_classifier.detectMultiScale(image, haar_scale, min_neighbors, haar_flags, min_size);

    return faces;

def merge_classifier_results(facesFromClassifier1, facesFromClassifier2):
    '''
    Merge results from two classifiers in a single list

    :type facesFromClassifier1: list
    :param facesFromClassifier1: list of faces detected using first classifier, represented as (x, y, width, height) lists

    :type facesFromClassifier2: list
    :param facesFromClassifier2: list of faces detected using second classifier, represented as (x, y, width, height) lists
    '''
    faces = [];

    # Add faces from second classifier only if they are not already present in list of faces from first classifier
    for face2 in facesFromClassifier2:
        for face1 in facesFromClassifier1:

            x1 = face1[0];
            y1 = face1[1];
            w1 = face1[2];
            h1 = face1[3];
            x2 = face2[0];
            y2 = face2[1];
            w2 = face2[2];
            h2 = face2[3];

            if((x1 != x2) | (y1 != y2) | (w1 != w2) | (h1 != h2)):
                faces.append(face2);

    faces.extend(facesFromClassifier1);

    return faces;









