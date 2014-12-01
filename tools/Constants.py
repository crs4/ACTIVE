import os

# Path of folders and files

#ACTIVE_ROOT_DIRECTORY=os.getcwd()+os.sep+".."+os.sep
ACTIVE_ROOT_DIRECTORY=r"C:\Users\Maurizio\Documents\Progetto ACTIVE" + os.sep # Maurizio Pintus
#ACTIVE_ROOT_DIRECTORY = r'C:\Active\Mercurial' + os.sep # Pc Lab
ANN_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\Annotations'
#CLASSIFIERS_FOLDER_PATH = r'C:\opencv\sources\data\haarcascades' # Pc Lab
CLASSIFIERS_FOLDER_PATH = r'C:\Opencv\opencv\sources\data\haarcascades' # Maurizio Pintus
CSV_FILE_NAME = 'Risultati.csv'
DB_MODELS_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'Models'
#DB_NAME = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'VidTIMIT'
DB_NAME = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'Videolina_80_LBP_1_8_4_4'
DB_PATH = r'C:\Active\Dataset\Videolina - Fotogrammi non annotati\Dataset_80\Training_set_ordered'
#DB_PATH = r'C:\Active\Dataset\VidTIMIT\Video\Training set'
FACE_ANNOTATION_DIR = r'Annotations' # Directory containg complete annotations
FACE_DETECTION_DIR = r'Face detection'
FACE_DETECTION_RESULTS_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\TestResultsNew'
FACE_DETECTION_TEST_SET_PATH = ACTIVE_ROOT_DIRECTORY + r'test\Test files\Face detection\TestSet'
#FACE_RECOGNITION_RESULTS_PATH = ACTIVE_ROOT_DIRECTORY + r'data\YouTube\Risultati\LBP_2_12_6_6_nose_position_oval_mask\Sliding window - 5 s'
FACE_RECOGNITION_RESULTS_PATH = r'C:\Active\Dataset\VidTIMIT\Risultati\LBP_1_8_4_4\Indipendent frames'
#FACE_RECOGNITION_TEST_SET_PATH = ACTIVE_ROOT_DIRECTORY + r'data\YouTube\Test_set'
FACE_RECOGNITION_TEST_SET_PATH = r'C:\Active\Dataset\VidTIMIT\Video\Test set'
FACE_EXTRACTOR_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'FaceExtractorConfiguration.yml'
FACE_RECOGNITION_DIR = r'Face recognition'
FACE_RECOGNITION_PEOPLE_DIR = r'People'
FACE_SIMPLE_ANNOTATION_DIR = r'Simple snnotations' # Directory containg simple annotations
#FACE_SUMMARIZATION_PATH = r'C:\Active\Face summarization' # Pc LAB
FACE_SUMMARIZATION_PATH = r'C:\Users\Maurizio\Documents\Face summarization' # Maurizio Pintus
FACE_TRACKING_DIR = r'Face tracking'
FACE_TRACKING_SEGMENTS_DIR = r'Segments'
#FRAMES_FILES_PATH = ACTIVE_ROOT_DIRECTORY + r'data\YouTube\Risultati\LBP_2_12_6_6_nose_position_oval_mask\Frames'
FRAMES_DIR_PATH = r'Frames'
FRAMES_FILES_PATH = r'C:\Active\Dataset\VidTIMIT\Risultati\LBP_1_8_4_4\Frames'
TEST_VIDEO_NAME = 'test1'
SAVE_PATH_ALL_FACES = r'C:\Active\Mercurial\test\Test files\Summarization' +  os.sep + TEST_VIDEO_NAME + os.sep + 'All faces'
SAVE_PATH_ALL_KEY_FRAMES = r'C:\Active\Mercurial\test\Test files\Summarization' +  os.sep + TEST_VIDEO_NAME + os.sep + 'All key frames'
SAVE_PATH_FACE_GROUPS = r'C:\Active\Mercurial\test\Test files\Summarization' +  os.sep + TEST_VIDEO_NAME + os.sep + 'Face groups'
SAVE_PATH_KEY_FRAMES = r'C:\Active\Mercurial\test\Test files\Summarization' +  os.sep + TEST_VIDEO_NAME + os.sep + 'Key frames'
SOFTWARE_TEST_FILE_KEY = 'software_test_file'
SOFTWARE_TEST_FILE_PATH = ACTIVE_ROOT_DIRECTORY + r'tools\test.jpg'
TAGS_FILE_PATH = ACTIVE_ROOT_DIRECTORY + 'tools' + os.sep + 'Tags.txt'
TEST_CONFIGURATION_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep +  'test' + os.sep + 'Test module' + os.sep + 'src' + os.sep + 'TestConfiguration.yml'
TEST_VIDEO_PATH = r'C:\Active\RawVideos' +  os.sep + TEST_VIDEO_NAME + '.mpg'
TMP_TRACKED_FACE_FILE_PATH = ACTIVE_ROOT_DIRECTORY + os.sep + 'tools' + os.sep + 'tracked_face.bmp'
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
CONFIDENCE_KEY = 'confidence'
DETECTED_FACES_NR_KEY = 'detected_faces_nr'
DETECTION_BBOX_KEY = 'detection_bbox'
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
LEFT_EYE_POS_KEY = 'left_eye_position'
NO_FACE_STRING = 'No face detected'
NOSE_POSITION_KEY = 'nose_position'
PEOPLE_KEY = 'people'
PERSON_CHECK_KEY = 'person_check'
PERSON_LABEL_KEY = 'label'
RIGHT_EYE_POS_KEY = 'right_eye_position'
SEGMENTS_KEY = 'segments'
SEGMENT_TOT_FRAMES_NR_KEY = 'segment_tot_frames_nr'
TEST_IMAGES_NR_KEY = 'test_images_nr'
TOT_FRAMES_NR_KEY = 'tot_frames_nr'
TRACKING_BBOX_KEY = 'tracking_bbox'
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
ALGORITH_NAME = 'HaarCascadeFrontalFaceAlt2'
DET_MIN_INT_AREA = 0.5 # Minimum value for intersection area 
					   # between two detections for merging them
EYE_DETECTION_CLASSIFIER = 'haarcascade_mcs_lefteye.xml'
FACE_DETECTION_ALGORITHM = 'HaarCascadeFrontalAndProfileFaces2'# Default HaarCascadeFrontalAndProfileFaces2
FACE_DETECTION_FLAGS = 'DoCannyPruning'
FACE_DETECTION_MIN_NEIGHBORS = 5
FACE_DETECTION_MIN_SIZE_HEIGHT = 20
FACE_DETECTION_MIN_SIZE_WIDTH = 20
FACE_DETECTION_SCALE_FACTOR = 1.1
MOUTH_DETECTION_CLASSIFIER = 'haarcascade_mcs_mouth.xml'
NOSE_DETECTION_CLASSIFIER = 'haarcascade_mcs_nose.xml'
DET_MIN_INT_AREA

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
RESULTS_PATH_KEY = 'resultsPath'
TEST_SET_PATH_KEY = 'testSetPath'

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
USE_CAPTIONS = False
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

CROPPED_FACE_HEIGHT = 200 # Default 200, 245 for weighted LBP, 331 for oval mask
CROPPED_FACE_WIDTH = 200 # Default 200, 215 for weighted LBP, 200 for oval mask
GRID_CELLS_X = 3
GRID_CELLS_Y = 3
OFFSET_PCT_X = 0.20 # Default 0.20, 0.20 for weighted LBP, 0.24 for oval mask
OFFSET_PCT_Y = 0.20 # Default 0.20, 0.29 for weighted LBP, 0.42 for oval mask 
OFFSET_PCT_Y_FROM_MOUTH = 0.5
USE_EYE_DETECTION = True
USE_EYES_POSITION = True # Default True
USE_FACE_DETECTION_IN_TRAINING = False # Default False
USE_MOUTH_POSITION = False
USE_NOSE_POSITION = False
USE_OVAL_MASK = False
USE_RESIZING = True

# Face extraction from video
LOAD_IND_FRAMES_RESULTS = True
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
USE_SLIDING_WINDOW = False
SLIDING_WINDOW_SIZE = 5.0 # Size of sliding window in seconds
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
LBP_HIST_DIFF_THRESHOLD = 3
HSV_HIST_DIFF_THRESHOLD = 1000000

# Video annotations
VIDEO_ANN_PATH = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\Dataset Videolina 1\Video'
SEGMENT_START_KEY = 'segment_start'
SEGMENT_END_KEY = 'segment_end'
SEGMENT_DURATION_KEY = 'segment_duration'
AUDIO_SEGMENTS_KEY = 'audio_segments'
CAPTION_SEGMENTS_KEY = 'caption_segments'
VIDEO_SEGMENTS_KEY = 'video_segments'

# Face summarization
ANSWER_NO = 'n'
ANSWER_YES = 'y'
CONF_THRESHOLD = 4 # Threshold for retaining prediction 
# (faces whose prediction ha a confidence value 
# greater than CONF_THRESHOLD will be considered 'Undefined')
DETECTED_KEY = 'detected'
FRAME_PATH_KEY = 'frame_path'
FRAME_POS_KEY = 'frame_position'
# TO BE DELETED
#FRAMES_TO_DISCARD = 2 # Number of initial frames in tracking segment
# not considered for threshold calculation
IS_KNOWN_PERSON_ASK = 'Do you know this person (y/n) ?'
MAX_FACES_IN_MODEL = 1000 # Maximum number of faces in face model
MIN_DETECTION_PCT = 0.5 # Min percentage of detected faces out of
# total faces in tracking segment in order to retain segment
MIN_SEGMENT_DURATION = 1 # Minimum duration of a segment (in seconds)
MIN_SHOT_DURATION = 1 # Minimum duration of a shot (in seconds)
PERSON_NAME = 'Name'
PERSON_SURNAME = 'Surname' 
TRACKING_MIN_INT_AREA = 0.5 # Minimum value for intersection area 
							# between detection bbox and tracking window
# TO BE DELETED
#MIN_TRACKING_TIME = 1 # Minimum time (in seconds) from detection 
						# before tracking interruption is possible T
STD_MULTIPLIER_FRAME = 50  # Standard deviation multiplier for calculating
						# thresholds for shot cut detection
					  # Tests on FicMix indicate that it should be 
					  # > 350 and < 2000
					  # Tests on YouTubeMix indicate that it should be
					  # > 500 and 
STD_MULTIPLIER_FACE = 50 # Standard deviation multiplier for calculating 
					    # thresholds for dividing between faces
TRACKED_PERSON_TAG = 'tracked_person'
UNDEFINED_TAG = 'undefined'
# TO BE DELETED
#USE_3_CHANNELS = False # True if all 3 channels must be used in checking
					  # histogram differences 
VIDEO_DURATION_KEY = 'video_duration' # Total duration of video (in ms)
WINDOW_PERSON = 'Person' # Indication of person in window that shows 
					     # a person in video
