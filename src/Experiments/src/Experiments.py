from Utils import *
from FaceDetectionExperiments import *

print(" ### ACTIVE PROJECT - EXPERIMENT MODULE ###\n");

#Module choice

print("Module choice");
print(str(TestTypeEnum.FaceDetection.value) + " - Face detection");
print(str(TestTypeEnum.FaceRecognition.value) + " - Face recognition");
print(str(TestTypeEnum.WholeSystem.value) + " - Whole system");

#Waiting a correct input by user
while(True):
    moduleToBeTested = input("Please enter a value: ");

    if(moduleToBeTested == TestTypeEnum.FaceDetection.value):
        print("\n ### FACE DETECTION ###\n");
        #rootPath = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\Test\Test files\\'; # Path with all test files as row string
        rootPath = r'..\..\..\Test files\Face detection\\';
        paramsDict = {};
        paramsDict[SCALE_FACTOR_KEY] = 1.2;
        paramsDict[MIN_NEIGHBORS_KEY] = 3;
        paramsDict[FLAGS_KEY] = 0;
        paramsDict[MIN_SIZE_KEY] = (20,20);

        faceDetectionExperiments(rootPath, FaceDetectionAlgorithm.HaarCascadeFrontalFaceAlt, paramsDict);

        break;
    elif(moduleToBeTested == TestTypeEnum.FaceRecognition.value):
        #print("\n ### FACE RECOGNITION ###");
        print("Not available yet");
        break;
    elif(moduleToBeTested == TestTypeEnum.WholeSystem.value):
        #print("\n ### WHOLE SYSTEM ###");
        print("Not available yet");
        break;
    else:
        print("\nValue is not correct");




