from Constants import *
from enum import Enum
import yaml
import cv2

class TestType(Enum):
    FaceDetection = 1
    FaceRecognition = 2
    WholeSystem = 3

    # Load file with results of all experiments and return list of experiments
def loadExperimentResults(filePath):
    data = loadYAMLFile(filePath);
    experiments = data[EXPERIMENTS_KEY];
    return experiments;

# Save in csv file given list of experiments
def saveExperimentsInCSVFile(filePath, experiments):
    stream = open(filePath, 'w');

    # Write csv header
    stream.write(EXPERIMENT_NUMBER_KEY + ',' + EXPERIMENT_ALGORITHM_KEY + ',' +
                 SCALE_FACTOR_KEY + ',' + MIN_NEIGHBORS_KEY + ',' + FLAGS_KEY + ',' +
                 MIN_SIZE_WIDTH_KEY + ',' + MIN_SIZE_HEIGHT_KEY + ',' +
                 PRECISION_KEY + ',' + RECALL_KEY + ',' + F1_KEY + ',' +
                 MEAN_DETECTION_TIME_KEY + '\n');

    for experimentDict in experiments:
        experimentInnerDict = experimentDict[EXPERIMENT_KEY];
        paramsDict = experimentInnerDict[EXPERIMENT_PARAMS_KEY];
        flagEnumName = paramsDict[FLAGS_KEY].name;
        flagName = flagEnumName[flagEnumName.find('.')+1:]; # Get only flag name (without enum name)
        stream.write(str(experimentInnerDict[EXPERIMENT_NUMBER_KEY]) + ',' +
                     experimentInnerDict[EXPERIMENT_ALGORITHM_KEY] + ',' +
                     str(paramsDict[SCALE_FACTOR_KEY]) + ',' +
                     str(paramsDict[MIN_NEIGHBORS_KEY]) + ',' +
                     flagName + ',' +
                     str(paramsDict[MIN_SIZE_WIDTH_KEY]) + ',' +
                     str(paramsDict[MIN_SIZE_HEIGHT_KEY]) + ',' +
                     str(experimentInnerDict[PRECISION_KEY]) + ',' +
                     str(experimentInnerDict[RECALL_KEY]) + ',' +
                     str(experimentInnerDict[F1_KEY]) + ',' +
                     str(experimentInnerDict[MEAN_DETECTION_TIME_KEY]) + '\n');
    stream.close();




