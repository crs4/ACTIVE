from Constants import *
from Utils import *
#from FaceDetection import *
import os
from os import listdir, path
import cv2
from sympy import Polygon
from FaceDetection import *

def faceDetectionExperiments(rootPath, algorithm, paramsDict, showResult):
    '''
    Execute face detection experiments

    :type rootPath: string
    :param rootPath: path of directory containing all test files

    :type algorithm: FaceDetectionAlgorithm
    :param algorithm: the algorithm to be used for face detection

    :type paramsDict: dictionary
    :param paramsDict: dictionary containing the parameters to be used for face detection

    :type showResult: boolean
    :param showResult: show (true) or do not show (false) image with detected faces
    '''

    annotatedFacesNr = 0;
    truePositivesNr = 0;
    falsePositivesNr = 0;
    meanDetectionTime = 0;

    detectionDict = {};
    imagesListForYAML = []; # Array used for creating YAML file

    framesPath = rootPath + FACE_DETECTION_FRAMES_PATH;
    videoDirectories = listdir(framesPath);

    # Iterate over all directories with test frames
    globalFrameCounter = 0;
    for videoDir in videoDirectories:
        videoDirCompletePath = framesPath + videoDir;

        # Build path of file with annotations
        annotationsFile = rootPath + ANNOTATIONS_PATH + videoDir + '_annotations.yml';

        # Load annotations for this video
        frames = loadFrameAnnotations(annotationsFile);

        # Iterate over all frames taken from this video
        frameCounter = 0;
        for frameFile in listdir(videoDirCompletePath):

            annotationsDict = frames[frameCounter][ANNOTATIONS_FRAME_KEY];

            frameName = annotationsDict[ANNOTATIONS_FRAME_NAME_KEY];

            # Check that frame name from file with annotations corresponds to file name
            if(frameName != frameFile):
                print('Check failed');
                print('Frame file: ' + frameFile);
                print('Frame name from file with annotations: ' + frameName);
                continue;

            # Set path of frame and path of directory with classifier files
            framePath = videoDirCompletePath + '\\' + frameFile;
            classifierFilesPath = rootPath + CLASSIFIER_FILES_PATH;

            # Call function for face detection
            detectionResults = faceDetectionFromImage(framePath, classifierFilesPath, algorithm, paramsDict, showResult);

            # Add detection time to total
            meanDetectionTime = meanDetectionTime + detectionResults[FACE_DETECTION_ELAPSED_CPU_TIME_KEY];

            # Convert opencv rectangles in sympy polygons
            opencvDetectedFaces = detectionResults[FACE_DETECTION_FACES_KEY];
            detectedFaces = [];
            for (x, y, width, height) in opencvDetectedFaces:
                polygonFace = Polygon((x,y), (x+width, y), (x+width,y+height), (x, y+height));
                detectedFaces.append(polygonFace);

            # Save name of image and number of detected faces in image dictionary
            detectedFacesNrInImage = len(detectedFaces);
            imageDict = {};
            imageDictExtended = {};
            imageDict[FACE_DETECTIONS_FRAME_NAME_KEY] = frameName;
            imageDict[FACE_DETECTIONS_DETECTED_FACES_NR_KEY] = detectedFacesNrInImage;

            # Save number of annotated faces in image dictionary
            annotatedFacesNrInImage = annotationsDict[ANNOTATIONS_FRAME_FACES_NR_KEY];
            imageDict[ANNOTATED_FACES_NR_KEY] = annotatedFacesNrInImage;

            annotatedFaces = [];
            if(annotatedFacesNrInImage > 0):
                annotatedFaces = annotationsDict[ANNOTATIONS_FACES_KEY];
                annotatedFacesNr = annotatedFacesNr + annotatedFacesNrInImage;

            # Compare rectangles and update number of true positives and false positives
            truePositivesNrInImage = 0;

            detectedFacesListForYAML = []; # Array used for creating YAML file

            # Iterate through detected faces
            for detectedFaceRectangle in detectedFaces:
                detectedFaceWidth = int(detectedFaceRectangle.vertices[1].x - detectedFaceRectangle.vertices[0].x);
                detectedFaceHeight = int(detectedFaceRectangle.vertices[3].y - detectedFaceRectangle.vertices[0].y);
                truePositive = False; #True if detected face is a real face

                # Check if detected face contains one of the annotated faces.
                # Width of detected face must not be more than 4 times width of correctly annotated face.
                for annotatedFace in annotatedFaces:
                    annotatedFacePositionAndSize = annotatedFace[ANNOTATIONS_FACE_KEY];
                    x = annotatedFacePositionAndSize[ANNOTATIONS_FACE_X_KEY];
                    y = annotatedFacePositionAndSize[ANNOTATIONS_FACE_Y_KEY];
                    width = annotatedFacePositionAndSize[ANNOTATIONS_FACE_WIDTH_KEY];
                    height = annotatedFacePositionAndSize[ANNOTATIONS_FACE_HEIGHT_KEY];
                    annotatedFaceRectangle = Polygon((x,y), (x+width,y), (x+width,y+height), (x, y+height)); # Create sympy rectangle

                    if(detectedFaceRectangle.encloses(annotatedFaceRectangle) & (detectedFaceWidth <= 4 * width)):
                        truePositive = True;
                        truePositivesNr = truePositivesNr + 1;
                        truePositivesNrInImage = truePositivesNrInImage + 1

                        # Each face must be considered once
                        annotatedFaces.remove(annotatedFace);
                        break;

                # Save position and size of detected face in face dictionary and add this to list
                detectedFaceDict = {};
                detectedFaceInnerDict = {};
                detectedFaceInnerDict[FACE_DETECTIONS_FACE_X_KEY] = int(detectedFaceRectangle.vertices[0].x);
                detectedFaceInnerDict[FACE_DETECTIONS_FACE_Y_KEY] = int(detectedFaceRectangle.vertices[0].y);
                detectedFaceInnerDict[FACE_DETECTIONS_FACE_WIDTH_KEY] = detectedFaceWidth;
                detectedFaceInnerDict[FACE_DETECTIONS_FACE_HEIGHT_KEY] = detectedFaceHeight;

                # Save check result
                if(truePositive):
                    detectedFaceInnerDict[FACE_CHECK_KEY] = 'TP'; # Face is a true positive detection
                else:
                    detectedFaceInnerDict[FACE_CHECK_KEY] = 'FP'; # Face is a false positive detection

                detectedFaceDict[FACE_DETECTIONS_FACE_KEY] = detectedFaceInnerDict;
                detectedFacesListForYAML.append(detectedFaceDict);

            falsePositivesNrInImage = detectedFacesNrInImage - truePositivesNrInImage;
            imageDict[TRUE_POSITIVES_NR_KEY] = truePositivesNrInImage;
            imageDict[FALSE_POSITIVES_NR_KEY] = falsePositivesNrInImage;

            falsePositivesNr = falsePositivesNr + falsePositivesNrInImage;

            if(len(detectedFacesListForYAML) > 0):
                imageDict[FACE_DETECTIONS_FACES_KEY] = detectedFacesListForYAML;

            imageDictExtended[FACE_DETECTIONS_FRAME_KEY] = imageDict;

            imagesListForYAML.append(imageDictExtended);

            frameCounter = frameCounter + 1;
            globalFrameCounter = globalFrameCounter + 1;

    detectionDict[FACE_DETECTIONS_FRAMES_KEY] = imagesListForYAML;

    # Save check results
    detectionDict[ANNOTATED_FACES_NR_KEY] = annotatedFacesNr;
    detectionDict[TRUE_POSITIVES_NR_KEY] = truePositivesNr;
    detectionDict[FALSE_POSITIVES_NR_KEY] = falsePositivesNr;

    precision = 0;
    if(truePositivesNr != 0):
        precision = float(truePositivesNr) / (float(truePositivesNr + falsePositivesNr));

    recall = 0;
    if(annotatedFacesNr != 0):
        recall = float(truePositivesNr) / float(annotatedFacesNr);

    f1 = 0;
    if((precision + recall) != 0):
        f1 = 2 * (precision * recall) / (precision + recall);

    detectionDict[PRECISION_KEY] = precision;
    detectionDict[RECALL_KEY] = recall;
    detectionDict[F1_KEY] = f1;

    meanDetectionTime = meanDetectionTime / globalFrameCounter;

    detectionDict[MEAN_DETECTION_TIME_KEY] = meanDetectionTime;

    print("\n ### RESULTS ###\n");

    print('Precision: ' + str(precision*100) + '%');
    print('Recall: ' + str(recall*100) + '%');
    print('F1: ' + str(f1*100) + '%');
    print('Mean detection time: ' + str(meanDetectionTime) + ' s\n\n');

    # Update YAML file with results related to all the experiments
    numberOfAlreadyDoneExperiments = 0;

    newExperimentInnerDict = {};
    # Save algorithm name
    algorithmEnumName = FaceDetectionAlgorithm(algorithm).name;
    algorithmName = algorithmEnumName[algorithmEnumName.find('.')+1:]; # Get only algorithm name (without enum name)
    newExperimentInnerDict[EXPERIMENT_ALGORITHM_KEY] = algorithmName;

    # Save classification parameters
    newExperimentInnerDict[EXPERIMENT_PARAMS_KEY] = paramsDict;

    # Save results
    newExperimentInnerDict[PRECISION_KEY] = precision;
    newExperimentInnerDict[RECALL_KEY] = recall;
    newExperimentInnerDict[F1_KEY] = f1;
    newExperimentInnerDict[MEAN_DETECTION_TIME_KEY] = meanDetectionTime;

    allResultsYAMLFilePath = rootPath + RESULTS_PATH + FACE_DETECTION_EXPERIMENT_RESULTS_FILE_NAME + '.yml';
    fileCheck = os.path.isfile(allResultsYAMLFilePath);

    experiments = list();
    if(fileCheck):
        experiments = loadExperimentResults(allResultsYAMLFilePath);
        numberOfAlreadyDoneExperiments = len(experiments);
        newExperimentInnerDict[EXPERIMENT_NUMBER_KEY] = numberOfAlreadyDoneExperiments + 1;

    else:
        newExperimentInnerDict[EXPERIMENT_NUMBER_KEY] = 1;

    newExperimentDict = {};
    newExperimentDict[EXPERIMENT_KEY] = newExperimentInnerDict;
    experiments.append(newExperimentDict);
    experimentsDict = {};
    experimentsDict[EXPERIMENTS_KEY] = experiments;
    saveYAMLFile(allResultsYAMLFilePath, experimentsDict);

    # Update csv file with results related to all the experiments
    allResultsCSVFilePath = rootPath + RESULTS_PATH + FACE_DETECTION_EXPERIMENT_RESULTS_FILE_NAME + '.csv';
    saveExperimentsInCSVFile(allResultsCSVFilePath, experiments);

    # Save file with results related to this experiment
    resultsFilePath = rootPath + RESULTS_PATH + 'FaceDetectionExperiment' + str(numberOfAlreadyDoneExperiments + 1) + 'Results.yml';
    result = saveYAMLFile(resultsFilePath, detectionDict);
