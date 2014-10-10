import os

# Path of folders and files

#ACTIVE_ROOT_DIRECTORY=os.getcwd()+os.sep+".."+os.sep
#ACTIVE_ROOT_DIRECTORY=r"C:\Users\Maurizio\Documents\Progetto ACTIVE" + os.sep
ACTIVE_ROOT_DIRECTORY = r'C:\Active\Mercurial' + os.sep
ANN_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\Annotations'
CLASSIFIERS_FOLDER_PATH = ACTIVE_ROOT_DIRECTORY +  r'test\Test files\Face detection\ClassifierFiles'
CSV_FILE_NAME = 'Risultati.csv'
DB_MODELS_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'Models'
DB_NAME = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'Fic.02'
DB_PATH=ACTIVE_ROOT_DIRECTORY+os.sep + r'data\Videolina - Training set da testo\Frame per training scelti automaticamente\Fic.02\Training_set_ordered'
FACE_DETECTION_RESULTS_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\TestResultsNew'
FACE_DETECTION_TEST_SET_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\TestSet'
FACE_RECOGNITION_RESULTS_PATH = ACTIVE_ROOT_DIRECTORY + r'data\Videolina - Training set da testo\Frame per training scelti automaticamente\Fic.02\Risultati\LBP_1_8_4x4_sliding_window_1_s'
FACE_RECOGNITION_TEST_SET_PATH = ACTIVE_ROOT_DIRECTORY + r'data\Videolina - Training set da testo\Frame per training scelti automaticamente\Fic.02\Test_set'
FACE_EXTRACTOR_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'FaceExtractorConfiguration.yml'
FRAMES_YAML_FILES_PATH = ACTIVE_ROOT_DIRECTORY + r'data\Videolina - Training set da testo\Frame per training scelti automaticamente\Fic.02\Risultati\LBP_1_8_4x4_sliding_window_1_s\Frames'
SAVE_PATH_ALL_FACES = r'C:\Active\Mercurial\test\Test files\Summarization\Fic.02\All faces'
SAVE_PATH_FACE_GROUPS = r'C:\Active\Mercurial\test\Test files\Summarization\Fic.02\Face groups'
SAVE_PATH_KEY_FRAMES = r'C:\Active\Mercurial\test\Test files\Summarization\Fic.02\Key frames'
SOFTWARE_TEST_FILE_KEY = 'software_test_file'
SOFTWARE_TEST_FILE_PATH = ACTIVE_ROOT_DIRECTORY + r'tools\test.jpg'
TAGS_FILE_PATH = ACTIVE_ROOT_DIRECTORY + 'tools' + os.sep + 'Tags.txt'
TEST_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep +  'test' + os.sep + 'Test module' + os.sep + 'src' + os.sep + 'TestConfiguration.yml'
TEST_VIDEO_PATH = r'C:\Active\RawVideos\fic.02.mpg'
TMP_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'aligned_face.bmp'
TMP_FRAME_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'frame.bmp'

# Face bounding box position
FACE_X_KEY = 'x'
FACE_Y_KEY = 'y'
FACE_WIDTH_KEY = 'width'
FACE_HEIGHT_KEY = 'height'

# Results

ANN_TAG_KEY = 'ann_tag'
ASSIGNED_LABEL_KEY = 'assigned_label'
ASSIGNED_TAG_KEY = 'assigned_tag'
BBOX_KEY = 'bbox'
CHECKED_KEY = 'checked'
DETECTED_FACES_NR_KEY = 'detected_faces_nr'
ELAPSED_CPU_TIME_KEY = 'elapsed_CPU_time'
ELAPSED_VIDEO_TIME_KEY = 'elapsed_video_time'
ERROR_KEY = 'error'
FACE_CHECK_KEY = 'face_check'
FACE_MODEL_KEY = 'face_model'
FACE_IMAGES_KEY = 'face_images'	
FACE_KEY = 'face'
FACES_KEY = 'faces'
FALSE_POSITIVES_NR_KEY = 'false_positives_nr'
FRAME_COUNTER_KEY = 'frame_counter'
FRAME_KEY = 'image'
FRAME_NAME_KEY = 'image_name'
FRAMES_KEY = 'images'
GLOBAL_RESULTS_KEY = 'global_results'
IMAGE_COUNTER_KEY = 'image_counter'
IMAGE_NAME_KEY = 'image_name'
IMAGE_KEY = 'image'
IMAGE_PATH_KEY = 'image_path'
IMAGES_KEY = 'images'
PEOPLE_KEY = 'people'
PERSON_CHECK_KEY = 'person_check'
PERSON_LABEL_KEY = 'label'
SEGMENTS_KEY = 'segments'
SEGMENT_TOT_FRAMES_NR_KEY = 'segment_tot_frames_nr'
TOT_FRAMES_NR_KEY = 'tot_frames_nr'
TRUE_POSITIVES_NR_KEY = 'true_positives_nr'
VIDEO_COUNTER_KEY = 'video_counter'

# Performance measures

RECOGNITION_RATE_KEY = 'recognition_rate'
PRECISION_KEY = 'precision';
MEAN_PRECISION_KEY = 'mean_precision'
STD_PRECISION_KEY = 'std_precision'
RECALL_KEY = 'recall';
MEAN_RECALL_KEY = 'mean_recall'
STD_RECALL_KEY = 'std_recall'
F1_KEY = 'F1';
MEAN_F1_KEY = 'mean_F1'
STD_F1_KEY = 'std_F1'
CONFIDENCE_KEY = 'confidence'
MEAN_DETECTION_TIME_KEY = 'mean_detection_time'
MEAN_RECOGNITION_TIME_KEY = 'mean_recognition_time'

# Annotations

ANNOTATIONS_FRAMES_KEY = 'images';
ANNOTATIONS_FRAME_KEY = 'Image';
ANNOTATIONS_FRAME_NAME_KEY = 'imageName';
ANNOTATIONS_FRAME_FACES_NR_KEY = 'numberOfFaces';
ANNOTATIONS_FACES_KEY = 'faces';
ANNOTATIONS_FACE_KEY = 'face';
ANNOTATED_FACES_NR_KEY = 'ann_faces_nr';
ANNOTATIONS_PERSON_NAME_KEY = 'person_name';
ANNOTATIONS_PERSON_TAG_KEY = 'person_tag';

# Dictionary with detection parameters

ALGORITHM_KEY = 'algorithm'
CLASSIFIERS_FOLDER_PATH_KEY = 'classifiers_folder_path'
FACE_DETECTION_KEY = 'face_detection'
FACE_EXTRACTION_KEY = 'face_extraction'
FACE_RECOGNITION_KEY = 'face_recognition';
FLAGS_KEY = 'flags';
MAX_SIZE_HEIGHT_KEY = 'max_size_height';
MAX_SIZE_WIDTH_KEY = 'max_size_width';
MIN_NEIGHBORS_KEY = 'min_neighbors';
MIN_SIZE_HEIGHT_KEY = 'min_size_height';
MIN_SIZE_WIDTH_KEY = 'min_size_width';
SCALE_FACTOR_KEY = 'scale_factor';

# Detection parameters
ALGORITH_NAME = 'HaarCascadeFrontalAndProfileFaces2'
EYE_DETECTION_CLASSIFIER = 'haarcascade_mcs_lefteye.xml'
FACE_DETECTION_ALGORITHM = 'HaarCascadeFrontalAndProfileFaces2'# TEST ONLY Default HaarCascadeFrontalFaceAlt2
FACE_DETECTION_FLAGS = 'DoCannyPruning'
FACE_DETECTION_MIN_NEIGHBORS = 5
FACE_DETECTION_MIN_SIZE_HEIGHT = 20
FACE_DETECTION_MIN_SIZE_WIDTH = 20
FACE_DETECTION_SCALE_FACTOR = 1.1

# Experiment parameters

FACE_DETECTION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceDetectionExperimentsResults';
FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceRecognitionExperimentsResults';
FACE_EXTRACTION_EXPERIMENT_RESULTS_FILE_NAME = 'FaceExtractionExperimentResults';
EXPERIMENTS_KEY = 'experiments';
EXPERIMENT_KEY = 'experiment';
EXPERIMENT_NUMBER_KEY = 'experimentNumber';
EXPERIMENT_ALGORITHM_KEY = 'algorithm';
EXPERIMENT_PARAMS_KEY = 'parameters';
EXPERIMENT_RESULTS_FILE_NAME = 'FaceDetectionExperiments'

# Face recognition parameters
ALFA = 1
CALCULATE_K_FROM_FEATURES = False
FACE_MODEL_ALGORITHM="LBP"
LBP_RADIUS=1
LBP_NEIGHBORS=8
LBP_GRID_X=4
LBP_GRID_Y=4
KNN_NEIGHBORS = 1
TAG_SEP = '_'
# If true, pixels in some regions in face images are put equals to zero
USE_BLACK_PELS = False 
USE_CANNY_IN_CROPPED_FACES = False
USE_CAPTIONS = True
USE_HIST_EQ_IN_CROPPED_FACES = True
USE_MIRRORED_FACES_IN_TRAINING = False
USE_NBNN = False
USE_NORM_IN_CROPPED_FACES = False
USE_ONE_FILE_FOR_FACE_MODELS = True
USE_TAN_AND_TRIGG_NORM = False
USE_WEIGHTED_KNN = False
USE_WEIGHTED_REGIONS = False

# Weights for 7 x 7 grid with weighted LBP

WEIGHT_0_REGIONS = [17, 21, 24, 27, 28, 34, 35, 41, 42, 48]
WEIGHT_2_REGIONS = [0, 6, 7, 13]
WEIGHT_4_REGIONS = [8, 9, 11, 12]

# Face alignment parameters

CROPPED_FACE_HEIGHT = 200 # Default 200 245 for weighted LBP
CROPPED_FACE_WIDTH = 200 # Default 200 215 for weighted LBP
GRID_CELLS_X = 3
GRID_CELLS_Y = 3
OFFSET_PCT_X = 0.20 # Default 0.20
OFFSET_PCT_Y = 0.20 # Default 0.20 0.29 for weighted LBP
OFFSET_PCT_Y_FROM_MOUTH = 0.5
USE_EYE_DETECTION = True
USE_EYES_POSITION = False # Default True
USE_FACE_DETECTION_IN_TRAINING = False # Default False
USE_MOUTH_POSITION = False
USE_RESIZING = True

# Face extraction from video
LOAD_IND_FRAMES_RESULTS = False
MAX_DELTA_PCT_W = 0.1
MAX_DELTA_PCT_X = 0.1
MAX_DELTA_PCT_Y = 0.1
# Maximum number of frames with missed detection that does not interrupt tracking
MAX_FRAMES_WITH_MISSED_DETECTION = 5 
USE_ORIGINAL_FPS = True
# Bitrate at which video is analyzed in face extraction
USED_FPS = 1.0
USE_ORIGINAL_FPS_IN_SHOT_DETECTIN = False
# Bitrate at which video is analyzed in shot detection
USED_FPS_IN_SHOT_DETECTION = 1.0
USE_ORIGINAL_FPS_IN_TRAINING = False 
# Bitrate at which video is analyzed in training from captions
USED_FPS_IN_TRAINING = 1.0
# Assigne tag that whose assigned to the majority of frames
USE_MAJORITY_RULE = True 
# Assigne tag that received the minimum value for the mean of confidences among frames
USE_MEAN_CONFIDENCE_RULE = False 
# Assigne tag that received the minimum value of confidence
USE_MIN_CONFIDENCE_RULE = True
USE_SLIDING_WINDOW = True
SLIDING_WINDOW_SIZE = 1.0 # Size of sliding window in seconds
USE_TRACKING = False
STOP_TRACKING_THRESHOLD = 20

# Caption recognition
ALL_LETTERS_KEY = 'all_letters'
CONTOURS_KEY = 'contours'
EQ_LETTERS_NR_KEY = 'eq_letters_nr'
HIERARCHY_KEY = 'hierarchy'
KERNEL_MAX_SIZE = 5
LETT_MARGIN = 2
LEV_RATIO_PCT_THRESH = 0.8
MAX_BBOX_DIFF = 10
MAX_CHAR_HEIGHT_PCT = 0.2
MAX_CHAR_WIDTH_PCT = 0.2
MIN_CHAR_HEIGHT = 5
ORD_BBOXS_KEY = 'ord_bboxs'
ORD_CONTOUR_IDXS_KEY = 'ord_contour_idxs'
PELS_TO_TEXT_SIZE_RATIO = 25.7
TOT_LETTERS_NR_KEY = 'tot_letters_nr'
USE_LEVENSHTEIN = True

# Face extraction test
SIM_TRACKING = False

# Summarization
LBP_HIST_DIFF_THRESHOLD = 100
HSV_HIST_DIFF_THRESHOLD = 1000000




