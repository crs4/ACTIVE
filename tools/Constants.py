import os
ACTIVE_ROOT_DIRECTORY="C:\Users\Maurizio\Documents\Progetto ACTIVE"
DB_PATH=ACTIVE_ROOT_DIRECTORY+"\data\DATASET AT&T"

# Test configuration
TEST_FILES_PATH_KEY = 'testSetPath';
DATASET_PATH_KEY = 'datasetPath';
TRAINING_SET_PATH_KEY = 'trainingSetPath'
TEST_SET_PATH_KEY = 'testSetPath'
ANNOTATIONS_PATH_KEY = 'annotationsPath';
CLASSIFIER_FILES_PATH_KEY = 'classifierFilesPath';
RESULTS_PATH_KEY = 'testResultsPath';
SOFTWARE_TEST_FILE_KEY = 'softwareTestFile';
PERSON_IMAGES_NR_KEY = 'personImagesNr'
TRAINING_IMAGES_NR_KEY = 'trainingImagesNr';
PEOPLE_NR_KEY = 'peopleNr';
DATASET_ALREADY_DIVIDED = 'datasetAlreadyDivided';

# File paths
FACE_EXTRACTOR_CONFIGURATION_FILE = ACTIVE_ROOT_DIRECTORY + r'\tools\FaceExtractorConfiguration.yml'
TEST_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + r'\test\Test module\src\TestConfiguration.yml'

# Face bounding box position
FACE_X_KEY = 'x'
FACE_Y_KEY = 'y'
FACE_WIDTH_KEY = 'width'
FACE_HEIGHT_KEY = 'height'

# YAML result files
GLOBAL_RESULTS_KEY = 'globalResults';
IMAGES_KEY = 'images';
PEOPLE_KEY = 'people';
FACE_CHECK_KEY = 'faceCheck';
PERSON_CHECK_KEY = 'personCheck';
PERSON_ASSIGNED_LABEL_KEY = 'assignedPersonLabel'
PERSON_ASSIGNED_TAG_KEY = 'assignedPersonTag';
PERSON_ANNOTATED_TAG_KEY = 'annotatedPersonTag';

# YAML file with frame annotations
ANNOTATIONS_FRAMES_KEY = 'images';
ANNOTATIONS_FRAME_KEY = 'Image';
ANNOTATIONS_FRAME_NAME_KEY = 'imageName';
ANNOTATIONS_FRAME_FACES_NR_KEY = 'numberOfFaces';
ANNOTATIONS_FACES_KEY = 'faces';
ANNOTATIONS_FACE_KEY = 'face';
ANNOTATED_FACES_NR_KEY = 'annotatedFacesNr';
ANNOTATIONS_PERSON_NAME_KEY = 'personName';
ANNOTATIONS_PERSON_TAG_KEY = 'personTag';

# YAML file with face detection results
FACE_DETECTIONS_DETECTED_FACES_NR_KEY = 'detectedFacesNr';
FACE_DETECTIONS_FRAMES_KEY = 'images';
FACE_DETECTIONS_FRAME_KEY = 'image';
FACE_DETECTIONS_FRAME_NAME_KEY = 'imageName';
FACE_DETECTIONS_FACES_KEY = 'faces';
FACE_DETECTIONS_FACE_KEY = 'face';

# Face detection check
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
FACE_RECOGNITION_KEY = 'faceRecognition';
FACE_EXTRACTION_KEY = 'faceExtraction'

# Face detection result dictionary
FACE_DETECTION_ELAPSED_CPU_TIME_KEY = 'elapsedCPUTime';
FACE_DETECTION_ERROR_KEY = 'error';
FACE_DETECTION_FACES_KEY = 'faces';
FACE_DETECTION_FACE_IMAGES_KEY = 'faceImages'

# Face recognition result dictionary
FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY = 'elapsedCPUTime';
FACE_RECOGNITION_ERROR_KEY = 'error';
FACE_RECOGNITION_IMAGE_NAME_KEY = 'imageName';
FACE_RECOGNITION_IMAGE_KEY = 'image';
FACE_RECOGNITION_GLOBAL_RESULTS = 'globalResults';
FACE_RECOGNITION_IMAGES_KEY = 'images';
FACE_RECOGNITION_PEOPLE_KEY = 'people';
PERSON_LABEL_KEY = 'label';
PERSON_ASSIGNED_LABEL_KEY = 'label';
PERSON_CONFIDENCE_KEY = 'confidence';
PERSON_TRUE_POSITIVES_NR_KEY = 'truePositivesNr';
PERSON_FALSE_POSITIVES_NR_KEY = 'falsePositivesNr';
PERSON_PRECISION_KEY = 'precision';
PERSON_RECALL_KEY = 'recall';
PERSON_F1_KEY = 'F1';
RECOGNITION_RATE_KEY = 'recognitionRate';
MEAN_PRECISION_KEY = 'meanPrecision';
STD_PRECISION_KEY = 'stdPrecision';
MEAN_RECALL_KEY = 'meanRecall';
STD_RECALL_KEY = 'stdRecall';
MEAN_F1_KEY = 'meanF1';
STD_F1_KEY = 'stdF1';
MEAN_RECOGNITION_TIME_KEY = 'meanRecognitionTime';

# Face extraction result dictionary
FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY = 'elapsedCPUTime';
FACE_EXTRACTION_ERROR_KEY = 'error';
FACE_EXTRACTION_FACES_KEY = 'faces';
FACE_EXTRACTION_TAG_KEY = 'tag';
FACE_EXTRACTION_BBOX_KEY = 'bbox';

# YAML file with face extraction results
FACE_EXTRACTION_FACE_KEY = 'face';
FACE_EXTRACTION_IMAGE_KEY = 'image';

# Experiment results
FACE_DETECTION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceDetectionExperimentsResults';
FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceRecognitionExperimentsResults';
FACE_EXTRACTION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceExtractionExperimentResults';
EXPERIMENTS_KEY = 'experiments';
EXPERIMENT_KEY = 'experiment';
EXPERIMENT_NUMBER_KEY = 'experimentNumber';
EXPERIMENT_ALGORITHM_KEY = 'algorithm';
EXPERIMENT_PARAMS_KEY = 'parameters';
