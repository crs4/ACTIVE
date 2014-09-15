import os
#ACTIVE_ROOT_DIRECTORY=os.getcwd()+os.sep+".."+os.sep
#ACTIVE_ROOT_DIRECTORY=r"C:\Users\Maurizio\Documents\Progetto ACTIVE"
ACTIVE_ROOT_DIRECTORY = r'C:\Active\Mercurial\\'
#DB_PATH=ACTIVE_ROOT_DIRECTORY+os.sep+"Training Set Videolina"
#DB_PATH=ACTIVE_ROOT_DIRECTORY+os.sep+"data"+os.sep+'datatest'+os.sep+"Dataset AT&T TRAINING"
#DB_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + "data" + os.sep + "Dataset Videolina 3" + os.sep + "Training Set Aligned"
#DB_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + "data" + os.sep + "Dataset Videolina 3" + os.sep + "Training Set"
#DB_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + "data" + os.sep + "datatest" + os.sep + "Dataset AT&T TRAINING Ridotto"
#DB_PATH = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\YouTube\Dataset_50\Training_set_test'
DB_PATH = R'C:\Active\Mercurial\data\YouTube\Training set'
DB_NAME = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'YT'
DB_MODELS_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'Models'

#Path of files
FACE_EXTRACTOR_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'FaceExtractorConfiguration.yml'
TEST_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep +  'test' + os.sep + 'Test module' + os.sep + 'src' + os.sep + 'TestConfiguration.yml'

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
DATASET_ALREADY_DIVIDED_KEY = 'datasetAlreadyDivided';

# Face bounding box position
FACE_X_KEY = 'x'
FACE_Y_KEY = 'y'
FACE_WIDTH_KEY = 'width'
FACE_HEIGHT_KEY = 'height'

# Result files
GLOBAL_RESULTS_KEY = 'globalResults';
IMAGES_KEY = 'images';
PEOPLE_KEY = 'people';
FACE_CHECK_KEY = 'faceCheck';
PERSON_CHECK_KEY = 'personCheck';
PERSON_ASSIGNED_LABEL_KEY = 'assignedPersonLabel'
PERSON_ASSIGNED_TAG_KEY = 'assignedPersonTag';
PERSON_ANNOTATED_TAG_KEY = 'annotatedPersonTag';
VIDEO_COUNTER = 'videoCounter'

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
ANNOTATIONS_PERSON_NAME_KEY = 'personName';
ANNOTATIONS_PERSON_TAG_KEY = 'personTag';

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
PERSON_CHECK_KEY = 'check';
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
FACE_EXTRACTION_CONFIDENCE_KEY = 'confidence'
FACE_EXTRACTION_TOT_FRAMES_NR = 'totFramesNr'
FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY = 'elapsedVideoTime'
FACE_EXTRACTION_FRAMES_KEY = 'frames'
FACE_EXTRACTION_FRAME_COUNTER_KEY = 'frameCounter'
FACE_EXTRACTION_SEGMENT_TOT_FRAMES_NR_KEY = 'segmentTotFramesNr'
FACE_EXTRACTION_SEGMENTS_KEY = 'segments'

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

# Face recognition parameter
FACE_RECOGNITION_RADIUS=1
FACE_RECOGNITION_NEIGHBORS=8
FACE_RECOGNITION_GRID_X=7
FACE_RECOGNITION_GRID_Y=7
#FACES_WIDTH = 200;
#FACES_HEIGHT = 200;
USE_HIST_EQ_IN_CROPPED_FACES = False
USE_NORM_IN_CROPPED_FACES = False
USE_CANNY_IN_CROPPED_FACES = False
USE_TAN_AND_TRIGG_NORM = True
USE_MIRRORED_FACES_IN_TRAINING = False
USE_BLACK_PELS = False # If true, pixels in some regions in face images are put equals to zero
LABEL_SEP = '_'

# Face Model parameter
FACEMODEL_ALGORITHM="LBP"
FACEMODEL_CONSTANT_ALGORITHM="LBP"
USE_ONE_FILE_FOR_FACE_MODELS = True

# Face alignment
TMP_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'aligned_face.bmp'
OFFSET_PCT_X = 0.20 # Default 0.20
OFFSET_PCT_Y = 0.29 # Default 0.20
OFFSET_PCT_Y_FROM_MOUTH = 0.5
CROPPED_FACE_WIDTH = 215 # Default 200
CROPPED_FACE_HEIGHT = 245 # Default 200
GRID_CELLS_X = 3
GRID_CELLS_Y = 3
USE_EYES_POSITION = True #TEST ONLY SET True
USE_FACE_DETECTION_IN_TRAINING = False #TEST ONLY SET False
USE_MOUTH_POSITION = False

# Face extraction from video
TMP_FRAME_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'frame.bmp'
USE_TRACKING = False
USE_MAJORITY_RULE = True # Assigne tag that whose assigned to the majority of frames
USE_MIN_CONFIDENCE_RULE = True # Assigne tag that received the minimum value of confidence
USE_MEAN_CONFIDENCE_RULE = False # Assigne tag that received the minimum value for the mean of conficences among frames
MAX_DELTA_PCT_X = 0.1
MAX_DELTA_PCT_Y = 0.1
MAX_DELTA_PCT_W = 0.1
MAX_FRAMES_WITH_MISSED_DETECTION = 5 # Maximum number of frames with missed detection that does not interrupt tracking
USE_SLIDING_WINDOW = False
SLIDING_WINDOW_SIZE = 5.0 # Size of sliding window in seconds
USE_ORIGINAL_FPS = True
USED_FPS = 1.0 # Bitrate at which video is analyzed


