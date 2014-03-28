from Constants import *
from enum import Enum
import yaml
import cv2

class TestType(Enum):
    FaceDetection = 1
    FaceRecognition = 2
    WholeSystem = 3

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

# Load file with annotations and return data
def loadYAMLFile(filePath):
    stream = open(filePath, 'r');
    data = yaml.load(stream);
    stream.close();
    return data;

# Load file with image annotations and return list of images
def loadFrameAnnotations(filePath):
    data = loadYAMLFile(filePath);
    images = data[ANNOTATIONS_FRAMES_KEY];
    return images;

# Load file with results of all experiments and return list of experiments
def loadExperimentResults(filePath):
    data = loadYAMLFile(filePath);
    experiments = data[EXPERIMENTS_KEY];
    return experiments;

# Save YAML file
def saveYAMLFile(filePath, dict):
    stream = open(filePath, 'w');
    result = stream.write(yaml.dump(dict, default_flow_style=False));
    stream.close();
    return result;

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


