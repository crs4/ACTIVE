import cv2
from Constants import *
from Utils import *
from sympy import Polygon

HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER = 'haarcascade_frontalface_alt.xml';

# imageFilePath is the complete path of the image to be analyzed
# classifierFilesPath is the complete path of the directory that contains classifier files
# algorithm is a value in the enum FaceDetectionAlgorithm indicating the algorithm to be used
# paramsDict is a dictionary containing the values for the parameters
# if showResult equals True, image with detected faces is displayed
def faceDetectionFromImage(imageFilePath, classifierFilesPath, algorithm, paramsDict, showResult):

    # Saving processing time for face detection
    startTime = cv2.getTickCount();

    # Open image
    image = cv2.imread(imageFilePath, cv2.IMREAD_COLOR);

    # Load classifier file
    classifierFile = '';

    if(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalFaceAlt):
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER
    else:
        print('\nAlgorithm is not available');
    faceCascadeClassifier = cv2.CascadeClassifier(classifierFile);

    if(faceCascadeClassifier.empty()):
        print('Error loading cascade classifier file');
    else:
        # Detect faces in image
        haarScale= paramsDict[SCALE_FACTOR_KEY];
        minNeighbors = paramsDict[MIN_NEIGHBORS_KEY];
        haarFlags = paramsDict[FLAGS_KEY];
        minSize = paramsDict[MIN_SIZE_KEY];
        faces = faceCascadeClassifier.detectMultiScale(image, haarScale, minNeighbors, haarFlags, minSize);

    if(showResult):
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0);
        cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE);
        cv2.imshow('Result', image);
        cv2.waitKey(0);

    detectionTimeInClocks = cv2.getTickCount() - startTime;
    detectionTimeInSeconds = detectionTimeInClocks / cv2.getTickFrequency();

    result = {}; # Dictionary that will contain detected faces and CPU time
    result[FACE_DETECTION_ELAPSED_CPU_TIME_KEY] = detectionTimeInSeconds;
    result[FACE_DETECTION_ERROR_KEY] = '';
    result[FACE_DETECTION_FACES_KEY] = faces;

    return result;
