from Constants import *
from Utils import *
from os import listdir
import cv2
import sympy

def faceDetectionExperiments():

    #Algorithm choice

    algorithmsList = list(FaceDetectionAlgorithm);
    numberOfAlgorithms = len(algorithmsList);

    print("Face detection algorithm choice");
    print(algorithmsList);

    #Waiting a correct input by user
    while(True):
        algorithm = input("Please enter a value: ");

        if((algorithm > 0) & (algorithm <= numberOfAlgorithms)):
            print("\n ### " + str(algorithmsList[algorithm - 1]) + " ###\n");
            break;
        else:
            print("\nValue is not correct");

    videoDirectories = listdir(FRAMES_PATH);
    #Iterate over all directories with test frames
    for videoDir in videoDirectories:
        videoDirCompletePath = FRAMES_PATH + videoDir;

        #Build path of file with annotations
        annotationsFile = ANNOTATIONS_PATH + videoDir + '_annotations.yml';
        
        #Load annotations for this video
        frames = loadFrameAnnotations(annotationsFile);

        #Iterate over all frames related to video
        frameCounter = 0;
        for frameFile in listdir(videoDirCompletePath):
            print(frameFile);
            annotationsDict = frames[frameCounter][ANNOTATIONS_FRAME_KEY];
            print(annotationsDict);
            frameName = annotationsDict[ANNOTATIONS_FRAME_NAME_KEY];

            #Check that frame name from file with annotations corresponds to file name
            if(frameName != frameFile):
                print('Check failed');
                print('Frame file: ' + frameFile);
                print('Frame name from file with annotations: ' + frameName);
                continue;

            #Load frame
            frame = cv2.imread(videoDirCompletePath + '\\' + frameFile);
        
            #Call function for face detection, saving processing time
            startTime = cv2.getTickCount();
            
            #detectedFaces = imageFaceDetection(frame, algorithm, scaleFactor, minNeighbors, flags, minSize);
            ### TEST ONLY ###
            detectedFaces = [];
            #################
            
            detectionTimeInClocks = cv2.getTickCount() - startTime;
            detectionTimeInSeconds = detectionTimeInClocks / cv2.getTickFrequency();
            print('Detection time: ' + str(detectionTimeInSeconds) + ' s');

            #Save number of detected faces in image dictionary
            detectedFacesNrInImage = len(detectedFaces);
            imageDict = {};
            imageDict['detectedFacesNr'] = detectedFacesNrInImage;

            #Save number of annotated faces in image dictionary
            annotatedFacesNrInImage = annotationsDict[ANNOTATIONS_FRAME_NUMBER_OF_FACES];
            imageDict['annotatedFacesNr'] = annotatedFacesNrInImage;
            
            #Compare rectangles and update number of true positives and false positives
            
            
            frameCounter = frameCounter + 1;
            break;
        break;

### TEST ONLY ###
faceDetectionExperiments();
