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
        faceDetectionExperiments();
        break;
    elif(moduleToBeTested == TestTypeEnum.FaceRecognition.value):
        print("\n ### FACE RECOGNITION ###");
        break;
    elif(moduleToBeTested == TestTypeEnum.WholeSystem.value):
        print("\n ### WHOLE SYSTEM ###");
        break;
    else:
        print("\nValue is not correct");




