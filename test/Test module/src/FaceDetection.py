import cv2
from Constants import *
from Utils import *
from sympy import Polygon, intersection

HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER = 'haarcascade_frontalface_alt.xml';
HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER = 'haarcascade_frontalface_alt_tree.xml';
HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER = 'haarcascade_frontalface_alt2.xml';
HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER = 'haarcascade_frontalface_default.xml';
HAARCASCADE_PROFILEFACE_CLASSIFIER = 'haarcascade_profileface.xml';
LBPCASCADE_FRONTALFACE_CLASSIFIER = 'lbpcascade_frontalface.xml';
LBPCASCADE_PROFILEFACE_CLASSIFIER = 'lbpcascade_profileface.xml';

# imageFilePath is the complete path of the image to be analyzed
# classifierFilesPath is the complete path of the directory that contains classifier files
# algorithm is a value in the enum FaceDetectionAlgorithm indicating the algorithm to be used
# paramsDict is a dictionary containing the values for the parameters
# if showResult equals True, image with detected faces is displayed
def faceDetectionFromImage(imageFilePath, classifierFilesPath, algorithm, paramsDict, showResult):
    '''
    Detect faces in image

    :type imageFilePath: string
    :param imageFilePath: path of image to be analyzed

    :type classifierFilesPath: string
    :param classifierFilesPath: path of directory containing classifier files

    :type algorithm: FaceDetectionAlgorithm
    :param algorithm: the algorithm to be used for face detection

    :type paramsDict: dictionary
    :param paramsDict: dictionary containing the parameters to be used for face detection

    :type showResult: boolean
    :param showResult: show (true) or do not show (false) image with detected faces
    '''

    # Saving processing time for face detection
    startTime = cv2.getTickCount();

    # Open image
    image = cv2.imread(imageFilePath, cv2.IMREAD_COLOR);

    # Load classifier files
    classifierFile = '';
    classifierFile2 = '';
    useOneClassifierFile = True;

    if(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalFaceAlt):
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER
    elif(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalFaceAltTree):
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalFaceAlt2):
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalFaceDefault):
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.HaarCascadeProfileFace):
        classifierFile = classifierFilesPath + HAARCASCADE_PROFILEFACE_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.HaarCascadeFrontalAndProfileFaces):
        useOneClassifierFile = False;
        classifierFile = classifierFilesPath + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER;
        classifierFile2 = classifierFilesPath + HAARCASCADE_PROFILEFACE_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.LBPCascadeFrontalface):
        classifierFile = classifierFilesPath + LBPCASCADE_FRONTALFACE_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.LBPCascadeProfileFace):
        classifierFile = classifierFilesPath + LBPCASCADE_PROFILEFACE_CLASSIFIER;
    elif(algorithm == FaceDetectionAlgorithm.LBPCascadeFrontalAndProfileFaces):
        useOneClassifierFile = False;
        classifierFile = classifierFilesPath + LBPCASCADE_FRONTALFACE_CLASSIFIER;
        classifierFile2 = classifierFilesPath + LBPCASCADE_PROFILEFACE_CLASSIFIER;
    else:
        print('\nAlgorithm is not available');
        return;

    faces = [];
    if(useOneClassifierFile):
        faceCascadeClassifier = cv2.CascadeClassifier(classifierFile);

        if(faceCascadeClassifier.empty()):
            print('Error loading cascade classifier file');
            return;
        else:
            if(algorithm == FaceDetectionAlgorithm.LBPCascadeProfileFace):
                # lbpcascade_profileface classifier only detects faces rotated to the right,
                # so it must be used on the original and on the flipped image
                facesFromOrigImage = detectFacesInImageWithSingleClassifier(image, faceCascadeClassifier, paramsDict);

                # Flip image around y-axis
                flippedImage = cv2.flip(image, 1);

                facesFromFlippedImage = detectFacesInImageWithSingleClassifier(flippedImage, faceCascadeClassifier, paramsDict);

                # Transform coordinates of faces from flipped image
                imageWidth = len(image[0,:]);

                for i in range(len(facesFromFlippedImage)):
                    facesFromFlippedImage[i][0] = imageWidth + 1 - facesFromFlippedImage[i][0] - facesFromFlippedImage[i][2];

                # Merge results
                faces = mergeClassifierResults(facesFromOrigImage, facesFromFlippedImage);

            else:
                # Use classifier on original image only
                faces = detectFacesInImageWithSingleClassifier(image, faceCascadeClassifier, paramsDict);

    else:
        faceCascadeClassifier1 = cv2.CascadeClassifier(classifierFile);
        faceCascadeClassifier2 = cv2.CascadeClassifier(classifierFile2);
        if(faceCascadeClassifier1.empty() | faceCascadeClassifier2.empty()):
            print('Error loading cascade classifier file');
            return;
        else:
            # Detect faces in image using first classifier
            facesFromClassifier1 = detectFacesInImageWithSingleClassifier(image, faceCascadeClassifier1, paramsDict);
            print('faces from classifier 1:');
            print(facesFromClassifier1);

            # Detect faces in image using second classifier
            facesFromClassifier2 = detectFacesInImageWithSingleClassifier(image, faceCascadeClassifier2, paramsDict);
            print('faces from classifier 2:');
            print(facesFromClassifier2);

            # Merge results
            faces = mergeClassifierResults(facesFromClassifier1, facesFromClassifier2);

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

def detectFacesInImageWithSingleClassifier(image, faceCascadeClassifier, paramsDict):
    '''
    Detect faces in image using a single classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type faceCascadeClassifier: faceCascadeClassifier
    :param faceCascadeClassifier: classifier to be used for the detection

    :type paramsDict: dictionary
    :param paramsDict: dictionary containing the parameters to be used for face detection
    '''
    haarScale= paramsDict[SCALE_FACTOR_KEY];
    minNeighbors = paramsDict[MIN_NEIGHBORS_KEY];
    haarFlags = paramsDict[FLAGS_KEY].value;
    minSize = (paramsDict[MIN_SIZE_WIDTH_KEY], paramsDict[MIN_SIZE_HEIGHT_KEY]);
    faces = faceCascadeClassifier.detectMultiScale(image, haarScale, minNeighbors, haarFlags, minSize);

    return faces;

def mergeClassifierResults(facesFromClassifier1, facesFromClassifier2):
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









