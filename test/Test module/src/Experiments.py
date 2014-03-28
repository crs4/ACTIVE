from numpy import *
from Utils import *
import cv2
from FaceDetectionExperiments import *

rootPath = r'..\..\Test files\Face detection\\';
moduleToBeTested = TestType.FaceDetection.value;

print(' ### ACTIVE PROJECT - EXPERIMENT MODULE ###\n');

if(moduleToBeTested == TestType.FaceDetection.value):

    paramsDict = {};

    scaleFactors = arange(1.05, 1.31, 0.05);
    minNeighbors = arange(2, 7, 1);

    for algorithm in FaceDetectionAlgorithm:
        for scaleFactor in scaleFactors:
            for minN in minNeighbors:

                algorithmEnumName = algorithm.name;
                algorithmName = algorithmEnumName[algorithmEnumName.find('.')+1:]; # Get only algorithm name (without enum name)
                print('Algorithm = ' + algorithmName + ', scale factor = ' + str(scaleFactor) +
                      ', min neighbors = ' + str(minN));

                paramsDict[SCALE_FACTOR_KEY] = float(scaleFactor);
                paramsDict[MIN_NEIGHBORS_KEY] = int(minN);
                paramsDict[FLAGS_KEY] = HaarCascadeFlag.DoCannyPruning;
                paramsDict[MIN_SIZE_WIDTH_KEY] = 20;
                paramsDict[MIN_SIZE_HEIGHT_KEY] = 20;

                #faceDetectionExperiments(rootPath, algorithm, paramsDict, False);

                faceDetectionExperiments(rootPath, algorithm, paramsDict, True);

elif(moduleToBeTested == TestType.FaceRecognition.value):
    #print("\n ### FACE RECOGNITION ###");
    print('\nNot available yet');

elif(moduleToBeTested == TestType.WholeSystem.value):
    #print("\n ### WHOLE SYSTEM ###");
    print('\nNot available yet');
else:
    print('\nValue is not correct');




