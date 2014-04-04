
#Path of files
FACE_DETECTION_FRAMES_PATH = 'TestSet\\'
ANNOTATIONS_PATH = 'Annotations\\';
RESULTS_PATH = 'TestResults\\';

#Filenames
FACE_EXTRACTOR_CONFIGURATION_FILE = 'FaceExtractorConfiguration.yml'

# YAML file with frame annotations
ANNOTATIONS_FRAMES_KEY = 'images';
ANNOTATIONS_FRAME_KEY = 'Image';
ANNOTATIONS_FRAME_NAME_KEY = 'imageName';
ANNOTATIONS_FRAME_FACES_NR_KEY = 'numberOfFaces';
ANNOTATIONS_FACES_KEY = 'faces';
ANNOTATIONS_FACE_KEY = 'face';
ANNOTATIONS_FACE_X_KEY = 'x';
ANNOTATIONS_FACE_Y_KEY = 'y';
ANNOTATIONS_FACE_WIDTH_KEY = 'width';
ANNOTATIONS_FACE_HEIGHT_KEY = 'height';
ANNOTATED_FACES_NR_KEY = 'annotatedFacesNr';
ANNOTATATIONS_PERSON_NAME_KEY = 'personName'

# YAML file with face detection results
FACE_DETECTIONS_DETECTED_FACES_NR_KEY = 'detectedFacesNr';
FACE_DETECTIONS_FRAMES_KEY = 'images';
FACE_DETECTIONS_FRAME_KEY = 'image';
FACE_DETECTIONS_FRAME_NAME_KEY = 'imageName';
FACE_DETECTIONS_FACES_KEY = 'faces';
FACE_DETECTIONS_FACE_KEY = 'face';
FACE_DETECTIONS_FACE_X_KEY = 'x';
FACE_DETECTIONS_FACE_Y_KEY = 'y';
FACE_DETECTIONS_FACE_WIDTH_KEY = 'width';
FACE_DETECTIONS_FACE_HEIGHT_KEY = 'height';

# Face detection check
FACE_CHECK_KEY = 'check';
TRUE_POSITIVES_NR_KEY = 'truePositivesNr';
FALSE_POSITIVES_NR_KEY = 'falsePositivesNr';
PRECISION_KEY = 'precision';
RECALL_KEY = 'recall';
F1_KEY = 'F1';
MEAN_DETECTION_TIME_KEY = 'meanDetectionTime';

# Dictionary with classification parameters
FACE_DETECTION_KEY = 'faceDetection'
ALGORITHM_KEY = 'algorithm'
CLASSIFIERS_FOLDER_PATH_KEY = 'classifiersFolderPath'
SCALE_FACTOR_KEY = 'scaleFactor';
MIN_NEIGHBORS_KEY = 'minNeighbors';
FLAGS_KEY = 'flags';
MIN_SIZE_WIDTH_KEY = 'minSizeWidth';
MIN_SIZE_HEIGHT_KEY = 'minSizeHeight';
MAX_SIZE_WIDTH_KEY = 'maxSizeWidth';
MAX_SIZE_HEIGHT_KEY = 'maxSizeHeight';

# Face detection result dictionary
FACE_DETECTION_ELAPSED_CPU_TIME_KEY = 'elapsedCPUTime';
FACE_DETECTION_ERROR_KEY = 'error';
FACE_DETECTION_FACES_KEY = 'faces';

# Face extraction result dictionary
FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY = 'elapsedCPUTime';
FACE_EXTRACTION_ERROR_KEY = 'error';
FACE_EXTRACTION_FACES_KEY = 'faces';

# Face detection experiment results
FACE_DETECTION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceDetectionExperimentsResults';
EXPERIMENTS_KEY = 'experiments';
EXPERIMENT_KEY = 'experiment';
EXPERIMENT_NUMBER_KEY = 'experimentNumber';
EXPERIMENT_ALGORITHM_KEY = 'algorithm';
EXPERIMENT_PARAMS_KEY = 'parameters';