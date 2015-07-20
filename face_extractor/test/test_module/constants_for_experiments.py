import os

# Parameters

# Path of root directory
ACTIVE_ROOT_DIRECTORY = os.getcwd() + os.sep + ".." + os.sep

# Face recognition parameter (used when Naive Bayes Nearest Neighbor is used)
ALFA = 1

# Path with aligned faces
ALIGNED_FACES_PATH = ''

# Path with annotations
ANNOTATIONS_PATH = r''

# If True, number of K nearest neighbors in face recognition is calculated
# from the number of neighbors in LBP and the number of cells in LBP grid
CALCULATE_K_FROM_FEATURES = False

# Directory containing the test set for caption recognition experiments
CAPTION_RECOGNITION_TEST_SET_PATH = ''

# CSV file with results
CSV_FILE_NAME = 'Results.csv'

# If True, dataset is already divided between training and test set
DATASET_ALREADY_DIVIDED = False

# Name of file containing face models
DB_NAME = ''

# Path of file containing face models
DB_PATH = ''

# Directory containing face models
DB_MODELS_PATH = ''

# Name of file with experiment results
EXPERIMENT_RESULTS_FILE_NAME = 'Experiments'

# Directory containing complete annotations for face detection
FACE_DETECTION_ANN_PATH = ''

# Directory that will contain results of face detection experiments
FACE_DETECTION_RESULTS_PATH = ''

# Directory containing the test set for face detection experiments
FACE_DETECTION_TEST_SET_PATH = ''

# Algorithm for face recognition
FACE_MODEL_ALGORITHM = 'LBP'

# Directory containing dataset for face recognition
FACE_RECOGNITION_DATASET_PATH = '' + os.sep

# Directory that will containn results of face recognition experiments
FACE_RECOGNITION_RESULTS_PATH = '' + os.sep

# Directory containing the test set for face recognition experiments
FACE_RECOGNITION_TEST_SET_PATH = ''

# Directory containing the training set for face recognition experiments
FACE_RECOGNITION_TRAINING_SET_PATH = ''

# Directory containing frames saved from video being analyzed
FRAMES_FILES_PATH = ''

# TODO ADD EXPLANATION
HSV_HIST_DIFF_THRESHOLD = 1000000

# Number of K nearest neighbors in face recognition
KNN_NEIGHBORS = 1

# TODO ADD EXPLANATION
LBP_HIST_DIFF_THRESHOLD = 3

# If True, use results of analysis on independent frames
LOAD_IND_FRAMES_RESULTS = True

# Parameters for simulated tracking
MAX_DELTA_PCT_W = 0.1
MAX_DELTA_PCT_X = 0.1
MAX_DELTA_PCT_Y = 0.1

# Maximum number of frames with missed detection
# that does not interrupt tracking
MAX_FR_WITH_MISSED_DET = 5

# Classifier for mouth detection
MOUTH_DETECTION_CLASSIFIER = 'haarcascade_mcs_mouth.xml'

# % of the image to keep next to the mouth in the vertical direction
OFFSET_PCT_Y_FROM_MOUTH = 0.5

# Path of training set used to create models for people recognition
PEOPLE_RECOGNITION_TRAINING_SET_PATH = ''

# Number of images per person
PERSON_IMAGES_NR = 10

# Name of video being analyzed
TEST_VIDEO_NAME = ''

# Number of images per person used for training set
TRAINING_IMAGES_NR = 2

# Save paths
SAVE_PATH_ALL_FACES = r'' + os.sep + TEST_VIDEO_NAME + os.sep + 'All faces'
SAVE_PATH_ALL_KEY_FRAMES = r'' + os.sep + TEST_VIDEO_NAME + os.sep + 'All key frames'
SAVE_PATH_FACE_GROUPS = r'' + os.sep + TEST_VIDEO_NAME + os.sep + 'Face groups'
SAVE_PATH_KEY_FRAMES = r'' + os.sep + TEST_VIDEO_NAME + os.sep + 'Key frames'

# If True, tracking is simulated
SIM_TRACKING = False

# If True, user annotations for people clusters are simulated
#  by using saved annotations for face tracks
SIMULATE_USER_ANNOTATIONS = True

# Size of sliding window in seconds
SLIDING_WINDOW_SIZE = 5.0

# Threshold for interrupting tracking
STOP_TRACKING_THRESHOLD = 20

# Path of test video
TEST_VIDEO_PATH = ''

# Path of temporary file for storing frames
TMP_FRAME_FILE_PATH= (
    ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'frame.bmp')

# If True, face models are updated
# after two face tracks are merged into one cluster
UPDATE_FACE_MODEL_AFTER_MERGING = False

# If True, training set for face recognition is built on the base of captions
USE_CAPTIONS = False

# If True, use eye detection
USE_EYE_DETECTION = True

# If True, use eye detection for images in training set
USE_EYE_DETECTION_IN_TRAINING = True

# If True, use eye positions for images in training set
USE_EYES_POSITION_IN_TRAINING = True  # Default True

# If True, use face detection for images in training set
USE_FACE_DETECTION_IN_TRAINING = False  # Default False

# If True, use mouth position
USE_MOUTH_POSITION = False

# If True, use Naive Bayes Nearest Neighbor
USE_NBNN = False

# If True, use one file for face models
USE_ONE_FILE_FOR_FACE_MODELS = True

# If True, use original frame rate of video for shot detection
USE_ORIGINAL_FPS_IN_SHOT_DETECTION = False

# If True, use people clustering
USE_PEOPLE_CLUSTERING = True

# If True, use people recognition
USE_PEOPLE_RECOGNITION = False

# If True, resize images
USE_RESIZING = True  # Default True

# If True, use sliding window in face extraction
USE_SLIDING_WINDOW = False

# If True, use weighted K-Nearest Neighbors in face recognition
USE_WEIGHTED_KNN = False

# If True, use weighted LBP
USE_WEIGHTED_REGIONS = False

# Frame rate at which video is analyzed in shot detection
USED_FPS_IN_SHOT_DETECTION = 1.0

# If True, use original frame rate of video when creating training set
USE_ORIGINAL_FPS_IN_TRAINING = False

# Frame rate at which video is analyzed in training from captions
USED_FPS_IN_TRAINING = 1.0

# If True, use tracking in face extraction
USE_TRACKING = False

# Director containing video annotations
VIDEO_ANN_PATH = ''

# File with results of video indexing experiments
VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME = ''

# Directory with results of video indexing experiments
VIDEO_INDEXING_RESULTS_PATH = r''

# Weights for 7 x 7 grid with weighted LBP
WEIGHT_0_REGIONS = [17, 21, 24, 27, 28, 34, 35, 41, 42, 48]
WEIGHT_2_REGIONS = [0, 6, 7, 13]
WEIGHT_4_REGIONS = [8, 9, 11, 12]

WORD_BLACKLIST_FILE_PATH = ''


# Directories

CLOTHING_RECOGNITION_DIR = 'Clothing recognition'
FACE_RECOGNITION_USER_ANNOTATIONS = 'User annotations'
FACE_TEMP_ANN_DIR = 'Temp annotations'
FACE_TEMP_SIMPLE_ANN_DIR = 'Temp simple annotations'


# Files
FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME = 'face_rec'


# Dictionary keys

ALIGNED_FACES_PATH_KEY = 'aligned_faces_path'
ANNOTATED_FACES_NR_KEY = 'ann_faces_nr'
ANNOTATIONS_FACE_KEY = 'face'
ANNOTATIONS_FACES_KEY = 'faces'
ANNOTATIONS_FRAME_FACES_NR_KEY = 'numberOfFaces'
ANNOTATIONS_FRAME_KEY = 'Image'
ANNOTATIONS_FRAME_NAME_KEY = 'imageName'
ANNOTATIONS_PATH_KEY = 'annotations_path'
ANNOTATIONS_PERSON_NAME_KEY = 'person_name'
ANNOTATIONS_PERSON_TAG_KEY = 'person_tag'
ANNOTATIONS_PERSON_TAG_KEY = 'person_tag'
CAPTION_PRECISION_KEY = 'caption_precision'
CAPTION_RECALL_KEY = 'caption_recall'
CAPTION_F1_KEY = 'caption_F1'
CAPTION_MEAN_PRECISION_KEY = 'caption_mean_precision'
CAPTION_STD_PRECISION_KEY = 'caption_std_precision'
CAPTION_MEAN_RECALL_KEY = 'caption_mean_recall'
CAPTION_STD_RECALL_KEY = 'caption_std_recall'
CAPTION_MEAN_F1_KEY = 'caption_mean_F1'
CAPTION_STD_F1_KEY = 'caption_std_F1'
CHECKED_KEY = 'checked'
CLOTH_MODELS_DIR_PATH_KEY = 'cloth_models_dir_path'
CODE_VERSION_KEY = 'code_version'
DATASET_ALREADY_DIVIDED_KEY = 'dataset_already_divided'
DATASET_PATH_KEY = 'dataset_path'
DB_NAME_KEY = 'db_name'
DETECTED_FACES_NR_KEY = 'detected_faces_nr'
EXPERIMENT_ALGORITHM_KEY = 'algorithm'
EXPERIMENT_KEY = 'experiment'
EXPERIMENT_NUMBER_KEY = 'experimentNumber'
EXPERIMENT_PARAMS_KEY = 'parameters'
EXPERIMENTS_KEY = 'experiments'
F1_KEY = 'F1'
FACE_CHECK_KEY = 'face_check'
FACE_DETECTION_RESULTS_PATH_KEY = 'face_detection_results'
FACE_EXTRACTION_KEY = 'face_extraction'
FACE_HEIGHT_KEY = 'height'
FACE_IMAGES_KEY = 'face_images'
FACE_MODEL_ALGORITHM_KEY = 'face_model_algorithm'
FACE_MODEL_KEY = 'face_model'
FACE_MODELS_DIR_PATH_KEY = 'face_models_dir_path'
FACE_RECOGNITION_KEY = 'face_recognition'
FACE_RECOGNITION_RESULTS_PATH_KEY = 'face_recognition_results_path'
FACE_TRACKING_FILE_PATH_KEY = 'face_tracking_file_path'
FACE_WIDTH_KEY = 'width'
FACE_X_KEY = 'x'
FACE_Y_KEY = 'y'
FACES_PATH_KEY = 'faces_path'
FALSE_POSITIVES_NR_KEY = 'false_positives_nr'
FRAME_KEY = 'image'
FRAME_NAME_KEY = 'image_name'
FRAMES_IN_MODELS_PATH_KEY = 'frames_in_models'
FRAMES_PATH_KEY = 'frames_path'
FRAME_POS_KEY = 'frame_position'
GLOBAL_RESULTS_KEY = 'global_results'
IMAGE_COUNTER_KEY = 'image_counter'
IMAGE_KEY = 'image'
IMAGE_NAME_KEY = 'image_name'
IMAGE_PATH_KEY = 'image_path'
IMAGES_KEY = 'images'
LOAD_IND_FRAMES_RESULTS_KEY = 'load_independent_frames_results'
MAX_FR_WITH_MISSED_DET_KEY = 'max_frames_with_missed_detections'
MEAN_DETECTION_TIME_KEY = 'mean_detection_time'
MEAN_F1_KEY = 'mean_F1'
MEAN_PRECISION_KEY = 'mean_precision'
MEAN_RECALL_KEY = 'mean_recall'
MEAN_RECOGNITION_TIME_KEY = 'mean_recognition_time'
MODEL_CREATION_TIME_KEY = 'model_creation_time'
MOUTH_DETECTION_CLASSIFIER_KEY = 'mouth_detection_classifier'
NO_FACE_STRING = 'No face detected'
NOSE_POS_FILE_PATH_KEY = 'nose_pos_file_path'
PEOPLE_KEY = 'people'
PERSON_CHECK_KEY = 'person_check'
PERSON_LABEL_KEY = 'label'
PRECISION_KEY = 'precision'
RECALL_KEY = 'recall'
RECOGNITION_RATE_KEY = 'recognition_rate'
RESULTS_PATH_KEY = 'results_path'
SAVED_FRAMES_NR_KEY = 'saved_frames_nr'
SIM_TRACKING_KEY = 'sim_tracking'
SIMULATE_USER_ANNOTATIONS_KEY = 'simulate_user_annotations'
SLIDING_WINDOW_SIZE_KEY = 'sliding_window_size'
SOFTWARE_TEST_FILE_PATH_KEY = 'software_test_file'
STD_F1_KEY = 'std_F1'
STD_PRECISION_KEY = 'std_precision'
STD_RECALL_KEY = 'std_recall'
TEST_IMAGES_NR_KEY = 'test_images_nr'
TEST_SET_PATH_KEY = 'test_set_path'
TEST_VIDEO_PATH_KEY = 'test_video_path'
TOT_FRAMES_NR_KEY = 'tot_frames_nr'
TRAINING_IMAGES_NR_KEY = 'training_images_nr'
TRAINING_SET_PATH_KEY = 'training_set_path'
TRUE_POSITIVES_NR_KEY = 'true_positives_nr'
UPDATE_FACE_MODEL_AFTER_MERGING_KEY = 'update_face_model_after_merging'
USE_CAPTIONS_KEY = 'use_captions'
USE_EYE_DETECTION_IN_TRAINING_KEY = r'use_eye_detection_in_training'
USE_EYES_POSITION_IN_TRAINING_KEY = r'use_eyes_position_in_training'
USE_EYE_DETECTION_KEY = 'use_eye_detection'
USE_FACE_DETECTION_IN_TRAINING_KEY = 'use_face_detection_in_training'
USE_ORIGINAL_FPS_IN_TRAINING_KEY = 'use_original_fps_in_training'
USED_FPS_IN_TRAINING_KEY = 'used_fps_in_training'
USE_NBNN_KEY = 'use_NBNN'
USE_PEOPLE_CLUSTERING_KEY = 'use_people_clustering'
USE_PEOPLE_RECOGNITION_KEY = 'use_people_recognition'
USE_RESIZING_KEY = 'use_resizing'
USE_ONE_FILE_FOR_FACE_MODELS_KEY = 'use_one_file_for_face_models'
USE_SLIDING_WINDOW_KEY = 'use_sliding_window'
USE_TRACKING_KEY = 'use_tracking'
USE_WEIGHTED_REGIONS_KEY = 'use_weighted_regions'
USER_ANNOTATION_TIME_KEY = 'user_annotation_time'
VIDEO_COUNTER_KEY = 'video_counter'
VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME_KEY = 'experiment_results_file_name'
VIDEO_INDEXING_RESULTS_PATH_KEY = 'video_indexing_results'
VIDEO_NAME_KEY = 'video_name'  # Name of video
VIDEO_PARAMS_FILE_PATH_KEY = 'video_parameters_file_path'
WORD_BLACKLIST_FILE_PATH_KEY = 'word_blacklist_file_path'