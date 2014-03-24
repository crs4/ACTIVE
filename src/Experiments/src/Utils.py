from Constants import *
from enum import Enum
import yaml

class TestTypeEnum(Enum):
    FaceDetection = 1
    FaceRecognition = 2
    WholeSystem = 3

class FaceDetectionAlgorithm(Enum):
    HaarCascadeFrontalFaceAlt = 1 # Haar cascade usign haarcascade_frontalface_alt.xml

# Load file with annotations and return data
def loadAnnotations(filePath):
    stream = open(filePath, 'r');
    data = yaml.load(stream);
    return data;

# Load file with image annotations and return list of images
def loadFrameAnnotations(filePath):
    data = loadAnnotations(filePath);
    images = data[ANNOTATIONS_FRAMES_KEY];
    return images;

# Save YAML file
def saveYAMLFile(filePath, dict):
    stream = open(filePath, 'w');
    result = stream.write(yaml.dump(dict, default_flow_style=False));
    return result;


