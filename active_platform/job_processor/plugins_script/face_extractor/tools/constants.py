# TODO UNCOMMENT FOR SERVER
from django.conf import settings
import os

# Parameters

# TODO CHANGE FOR SERVER
# Default path of directory for aligned faces
ALIGNED_FACES_PATH = r''

# If True, all bounding boxes related to one face track
# must be entirely contained by the corresponding frame
ALL_CLOTH_BBOXES_IN_FRAMES = False

# If True, check eye positions
CHECK_EYE_POSITIONS = True

# TODO CHANGE FOR SERVER
# Path of directory with OpenCV classifiers
CLASSIFIERS_DIR_PATH = r'/usr/share/opencv/haarcascades'
#CLASSIFIERS_DIR_PATH = r'C:\Opencv\opencv\sources\data\haarcascades'

# Height of bounding box for clothes
# (in % of the face bounding box height)
CLOTHES_BBOX_HEIGHT = 1.0

# Width of bounding box for clothes
# (in % of the face bounding box width)
CLOTHES_BBOX_WIDTH = 2.0 

# Method for comparing clothes of two face tracks 
# ('min', 'mean' or 'max')
CLOTHES_CHECK_METHOD = 'Max'

# Minimum distance between face features 
# of two face tracks for considering clothes
CLOTHES_CONF_THRESH = 8

# If True, bounding box for clothes is divided in 3 parts
CLOTHING_REC_USE_3_BBOXES = False

# If True, dominant color is used in clothing recognition
CLOTHING_REC_USE_DOMINANT_COLOR = False

# If True, position of bounding box for clothes 
# in the horizontal direction is fixed for the whole face track
CLOTHING_REC_USE_MEAN_X_OF_FACES = False

# Maximum distance between face features of two face tracks 
# for merging them in the same cluster.
# It should be greater or equals than CLOTHES_CONF_THRESH
CONF_THRESHOLD = 14

# Height of aligned faces (in pixels)
CROPPED_FACE_HEIGHT = 400

# Width of aligned faces (in pixels)
CROPPED_FACE_WIDTH = 200

# Minimum value for intersection area 
# between two detections for merging them
DET_MIN_INT_AREA = 0.5 

# Classifier for eye detection
EYE_DETECTION_CLASSIFIER = 'haarcascade_mcs_lefteye.xml'

# Classifier for face detection
FACE_DETECTION_ALGORITHM = 'HaarCascadeFrontalFaceAlt2'

# Flags used in face detection
FACE_DETECTION_FLAGS = 'DoCannyPruning'

# Mininum number of neighbors for face detection
FACE_DETECTION_MIN_NEIGHBORS = 5

# Minimum height of face detection bounding box (in pixels)
FACE_DETECTION_MIN_SIZE_HEIGHT = 20

# Minimum width of face detection bounding box (in pixels)
FACE_DETECTION_MIN_SIZE_WIDTH = 20

# Scale factor between two scans in face detection
FACE_DETECTION_SCALE_FACTOR = 1.1

# Minimum distance between faces in global face models
# It should be lower than GLOBAL_FACE_REC_THRESHOLD
GLOBAL_FACE_MODELS_MIN_DIFF = 5

# TODO CHANGE FOR SERVER
# Path of directory with people recognition data
GLOBAL_FACE_REC_DATA_DIR_PATH = os.path.join(os.path.join(settings.MEDIA_ROOT, 'models'), 'video')
#GLOBAL_FACE_REC_DATA_DIR_PATH = r'C:\Users\Maurizio\Documents\Video indexing\Global face recognition'

# Threshold for retaining prediction in global face recognition
# (faces whose prediction has a confidence value greater
# than GLOBAL_FACE_REC_THRESHOLD will be considered unknown)
GLOBAL_FACE_REC_THRESHOLD = 25  # default 8

# Number of columns used in grid for pre-aligned faces
GRID_CELLS_X = 3

# Number of rows used in grid for pre-aligned faces
GRID_CELLS_Y = 3

# Size of half sliding window (in frames)
HALF_WINDOW_SIZE = 10

# Size of kernel for smoothing histograms 
# when calculating dominant color
HIST_SMOOTHING_KERNEL_SIZE = 25

# Maximum size of kernel for image dilation in caption recognition
KERNEL_MAX_SIZE = 5

# Number of columns in grid used for calculating LBP
LBP_GRID_X = 4

# Number of rows in grid used for calculating LBP
LBP_GRID_Y = 8

# Number of neighbors used for calculating LBP
LBP_NEIGHBORS = 8

# Radius used for calculating LBP (in pixels)
LBP_RADIUS=1

# Margin used when drawing contours in caption recognition
LETT_MARGIN = 2

# Minimum threshold for considering captions in frame
LEV_RATIO_PCT_THRESH = 0.8

# Maximum difference between bounding boxes 
# of characters in the same row (in pixels)
MAX_BBOX_DIFF = 10

# Maximum height of characters (in % of the frame height)
MAX_CHAR_HEIGHT_PCT = 0.2

# Maximum width of characters (in % of the frame width)
MAX_CHAR_WIDTH_PCT = 0.2

# Maximum inclination of the line connecting the eyes 
# (in % of pi radians)
MAX_EYE_ANGLE = 0.125

# Maximum number of faces in face model related to one face track
MAX_FACES_IN_MODEL = 1000 

# Maximum number of frames with no corresponding detection 
# that does not interrupt tracking
MAX_FR_WITH_MISSED_DET = 50 

# Maximum difference between nose positions (
# stored as % of nose positions in face images)
MAX_NOSE_DIFF = 0.05

# Minimum height of characters (in pixels)
MIN_CHAR_HEIGHT = 5

# Minimum number of items contained in a cloth model
MIN_CLOTH_MODEL_SIZE = 5

# Minimum percentage of detected faces out of
# total faces in face track in order to retain face track
MIN_DETECTION_PCT = 0.3 

# Minimum distance between eyes 
# (in % of the width of the face bounding box)
MIN_EYE_DISTANCE = 0.25

# Minimum number of frames in the same face track
# with captions associated to the same person
# in order to consider caption
MIN_FRAMES_PER_CAPTION = 4

# Minimum duration of a segment (in seconds)
MIN_SEGMENT_DURATION = 1 

# Minimum length of tags considered in caption recognition
MIN_TAG_LENGTH = 10

# Height of neck (in % of the face bounding box height)
NECK_HEIGHT = 0.0

# Classifier for nose detection
NOSE_DETECTION_CLASSIFIER = 'haarcascade_mcs_nose.xml'

# % of the image to keep next to the eyes in the horizontal direction 
OFFSET_PCT_X = 0.20

# % of the image to keep next to the eyes in the vertical direction
OFFSET_PCT_Y = 0.50

# Ratio between height of character bounding box and text when trying
# to identify a character by adding to image a known character 
PELS_TO_TEXT_SIZE_RATIO = 25.7

# Standard deviation multiplier for calculating 
# thresholds for dividing between faces
STD_MULTIPLIER_FACE = 20 

# Standard deviation multiplier for 
# calculating thresholds for shot cut detection
STD_MULTIPLIER_FRAME = 20 

# Separator for tag parts
TAG_SEP = '_'

# TODO REVIEW (NICOLA)
# Path of directory containing "tesseract" directory
# TESSERACT_PARENT_DIR_PATH = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\face_extractor\tools' + os.sep
TESSERACT_PARENT_DIR_PATH = r'/var/spool/active_sinnova/job_processor/plugins_script/face_extractor/tools/'

# Minimum value for intersection area 
# between detection bbox and tracking window
# (in % of the area of the smallest rectangle)
TRACKING_MIN_INT_AREA = 0.1

# If True, final tag for a tracked face is obtained
# by aggregation of results for single frames
USE_AGGREGATION = False 

# If True, tracking is based on aligned face,
# otherwise it is based on original detected face
USE_ALIGNED_FACE_IN_TRACKING = True

# If True, use blacklist of item that make the results
# of the caption recognition on a frame rejected
USE_BLACKLIST = True

# If True, apply Canny edge detector to aligned faces
USE_CANNY_IN_CROPPED_FACES = False

# If True, use caption recognition in people recognition
USE_CAPTION_RECOGNITION = False

# If True, recognition based on clothes is used
USE_CLOTHING_RECOGNITION = True 

# If True, align faces by using eye positions
USE_EYES_POSITION = True

# If True, use face recognition in people recognition
USE_FACE_RECOGNITION = True

# If True, apply equalization to aligned faces
USE_HIST_EQ_IN_CROPPED_FACES = True

# If True, in aggregating results from several frames,
# final tag is the tag that was assigned to the majority of frames
USE_MAJORITY_RULE = True 

# If True, in aggregating results from several frames,
# final tag is the tag that received the minimum value 
# for the mean of confidences among frames
USE_MEAN_CONFIDENCE_RULE = False 

# If True, in aggregating results from several frames,
# final tag is the tag that received the minimum confidence value 
USE_MIN_CONFIDENCE_RULE = True

# If True, apply normalization to aligned faces
USE_NORM_IN_CROPPED_FACES = False

# If True, detections with no good nose position are discarded
USE_NOSE_POS_IN_DETECTION = False

# If True, compare in recognition only faces with similar nose positions
USE_NOSE_POS_IN_RECOGNITION = False

# If True, original frame rate is used
USE_ORIGINAL_FPS = False

# If True, original resolution is used
USE_ORIGINAL_RES = True

# Frame rate at which video is analyzed, if USE_ORIGINAL_FPS is False 
# (in frames per second)
USED_FPS = 5.0

# Frame rate at which video is analyzed for caption recognition
# (in frames per second)
# It should be less than USED_FPS
USED_FPS_FOR_CAPTIONS = 1.0

# Resolution at which frames/images are analyzed, 
# if USER_ORIGINAL_RES is False (% of original width and height)
USED_RES_SCALE_FACTOR = 0.5

# If True, words found in image by caption recognition and tags 
# are compared by using the Levenshtein distance
USE_LEVENSHTEIN = True

# If True, apply oval mask to face image
USE_OVAL_MASK = False

# If True, use skeletons for parallel and distributed computing
USE_SKELETONS = False

# If True, apply Tan & Triggs illumination normalization 
# to aligned faces
USE_TAN_AND_TRIGG_NORM = False

# If True, a variable threshold for clothing recognition is used
VARIABLE_CLOTHING_THRESHOLD = False

# TODO CHANGE FOR SERVER
# Path of directory where video indexing results are stored
VIDEO_INDEXING_PATH = os.path.join(settings.MEDIA_ROOT, 'items')
# VIDEO_INDEXING_PATH = r'C:\Users\Maurizio\Documents\Face summarization\Test'



# Directories


ALIGNED_FACES_DIR = 'Aligned faces'
BBOX_IMAGES_DIR = 'Bbox images'
CLOTH_MODELS_DIR = 'Cloth models'
FACE_ANNOTATION_DIR = 'Annotations'
FACE_DETECTION_DIR = 'Face detection'
FACE_EXTRACTION_DIR = 'Face extraction'
FACE_MODELS_DIR = 'Face models'
FACE_RECOGNITION_DIR = 'Face recognition'
FACE_RECOGNITION_KEY_FRAMES_DIR = 'Key frames'
FACE_RECOGNITION_PEOPLE_DIR = 'People'
FACE_SIMPLE_ANNOTATION_DIR = 'Simple annotations'
FACE_TRACKING_DIR = 'Face tracking'
FACE_TRACKING_SEGMENTS_DIR = 'Segments'
FRAMES_DIR = 'Frames'
PEOPLE_CLUSTERING_DIR = 'People clustering'
TRAINING_SET_DIR = 'Training set'
WHOLE_IMAGES_DIR = 'Whole images'




# Files

FACE_MODELS_FILE = 'Face_models'
FACES_FILE = 'Faces.yml'
FACES_NR_IN_FRAMES_FILE = 'faces_nr_in_frames.yml'
FRAMES_IN_MODELS_FILE = 'frames_in_models.yml'
NOSE_POSITIONS_FILE = 'noses'
TAG_LABEL_ASSOCIATIONS_FILE = 'Tag_label_associations.yml'
WORD_BLACKLIST_FILE = 'Word_blacklist.yml'



# Strings

UNDEFINED_LABEL = 'undefined'
UNDEFINED_TAG = 'undefined'




# Dictionary keys

ALIGNED_FACE_FILE_NAME = 'aligned_face_file_name'
ALIGNED_FACE_GRAY_SUFFIX = '_gray'
ALIGNED_FACES_PATH_KEY = 'aligned_faces_path'
ALL_CLOTH_BBOXES_IN_FRAMES_KEY = 'all_cloth_bboxes_in_frames'
ALL_LETTERS_KEY = 'all_letters'
ANNOTATIONS_FRAMES_KEY = 'images'
ANN_TAG_KEY = 'ann_tag'
ASSIGNED_LABEL_KEY = 'assigned_label'
ASSIGNED_TAG_KEY = 'assigned_tag'
AUDIO_SEGMENTS_KEY = 'audio_segments'
BBOX_KEY = 'bbox'
CAPTION_ASSIGNED_LABEL_KEY = 'caption_assigned_label'
CAPTION_ASSIGNED_TAG_KEY = 'caption_assigned_tag'
CAPTION_RECOGNITION_TIME_KEY = 'caption_recognition_time'
CAPTION_SEGMENTS_KEY = 'caption_segments'
CAPTION_SEGMENTS_NR_KEY = 'caption_segments_nr'
CHECK_EYE_POSITIONS_KEY = 'check_eye_positions'
CLASSIFIERS_DIR_PATH_KEY = 'classifiers_folder_path'
CLOTHES_BBOX_WIDTH_KEY = 'clothes_bounding_box_width'
CLOTHES_CHECK_METHOD_KEY = 'clothes_check_method'
CLOTHES_CONF_THRESH_KEY = 'conf_threshold_for_clothing_recognition'
CLOTHING_REC_USE_3_BBOXES_KEY = 'use_3_bboxes_in_clothing_recognition'
CLOTHING_REC_USE_DOMINANT_COLOR_KEY = (
    'use_dominant_color_in_clothing_recognition')
CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY = (
    'use_mean_x_of_faces_in_clothing_recognition')
CLOTH_MODELS_CREATION_TIME_KEY = 'cloth_models_creation_time'
CLOTHES_BBOX_HEIGHT_KEY = 'clothes_bounding_box_height'
CONFIDENCE_KEY = 'confidence'
CONF_THRESHOLD_KEY = 'conf_threshold'
CONTOURS_KEY = 'contours'
CROPPED_FACE_HEIGHT_KEY = 'cropped_face_height'
CROPPED_FACE_WIDTH_KEY = 'cropped_face_width'
DB_MODELS_PATH_KEY = 'db_models_path'
DETECTED_KEY = 'detected'
DETECTION_BBOX_KEY = 'detection_bbox'
TAG_ID_KEY = 'tag_id'
ELAPSED_CPU_TIME_KEY = 'elapsed_CPU_time'
ELAPSED_VIDEO_TIME_KEY = 'elapsed_video_time'
EQ_LETTERS_NR_KEY = 'eq_letters_nr'
ERROR_KEY = 'error'
EYE_DETECTION_CLASSIFIER_KEY = 'eye_detection_classifier'
FACE_DETECTION_ALGORITHM_KEY = 'face_detection_algorithm'
FACE_DETECTION_TIME_KEY = 'face_detection_time'
FACE_IN_MODELS_KEY = 'face_in_models'
FACE_MODELS_CREATION_TIME_KEY = 'face_models_creation_time'
FACE_KEY = 'face'
FACE_RECOGNITION_TIME_KEY = 'face_recognition_time'
FACE_TRACKING_TIME_KEY = 'face_tracking_time'
FACES_KEY = 'faces'
FLAGS_KEY = 'flags'
FRAME_COUNTER_KEY = 'frame_counter'
FRAME_EXTRACTION_TIME_KEY = 'frame_extraction_time'
FRAMES_KEY = 'images'
GLOBAL_FACE_MODELS_MIN_DIFF_KEY = 'global_face_models_min_diff'
GLOBAL_FACE_REC_DATA_DIR_PATH_KEY = 'global_face_recognition_dir_path'
GLOBAL_FACE_REC_THRESHOLD_KEY = 'global_face_recognition_threshold'
HALF_WINDOW_SIZE_KEY = 'half_window_size'
HIERARCHY_KEY = 'hierarchy'
HIST_SMOOTHING_KERNEL_SIZE_KEY = 'kernel_size_for_histogram_smoothing'
KEYFRAME_NAME_KEY = 'keyframe_name'
LBP_GRID_X_KEY = 'LBP_grid_x'
LBP_GRID_Y_KEY = 'LBP_grid_y'
LBP_NEIGHBORS_KEY = 'LBP_neighbors'
LBP_RADIUS_KEY = 'LBP_radius'
LEFT_EYE_POS_KEY = 'left_eye_position'
LEV_RATIO_PCT_THRESH_KEY = 'lev_ratio_pct_threshold'
MAX_EYE_ANGLE_KEY = 'max_eye_angle'
MAX_FACES_IN_MODEL_KEY = 'max_faces_in_model'
MAX_FR_WITH_MISSED_DET_KEY = 'max_frames_with_missed_detections'
MAX_NOSE_DIFF_KEY = 'max_nose_diff'
MEDOID_FRAME_NAME_KEY = 'medoid_frame_name'
MIN_CLOTH_MODEL_SIZE_KEY = 'min_cloth_model_size'
MIN_DETECTION_PCT_KEY = 'min_detection_pct'
MIN_EYE_DISTANCE_KEY = 'min_eye_distance'
MIN_FRAMES_PER_CAPTION_KEY = 'min_frames_per_caption'
MIN_NEIGHBORS_KEY = 'min_neighbors'
MIN_SEGMENT_DURATION_KEY = 'min_segment_duration'
MIN_SIZE_HEIGHT_KEY = 'min_size_height'
MIN_SIZE_WIDTH_KEY = 'min_size_width'
MIN_TAG_LENGTH_KEY = 'min_tag_length'
NECK_HEIGHT_KEY = 'neck_height'
NOSE_DETECTION_CLASSIFIER_KEY = 'nose_detection_classifier'
NOSE_POSITION_KEY = 'nose_position'
OFFSET_PCT_X_KEY = 'offset_pct_x'
OFFSET_PCT_Y_KEY = 'offset_pct_y'
ORD_BBOXS_KEY = 'ord_bboxs'
ORD_CONTOUR_IDXS_KEY = 'ord_contour_idxs'
PEOPLE_CLUSTERING_TIME_KEY = 'people_clustering_time'
PEOPLE_CLUSTERS_NR_KEY = 'people_clusters_nr'
PEOPLE_RECOGNITION_TIME_KEY = 'people_recognition_time'
PERSON_COUNTER_KEY = 'person_counter'
RELEVANT_PEOPLE_NR_KEY = 'relevant_people_nr'
RIGHT_EYE_POS_KEY = 'right_eye_position'
SAVED_FRAME_NAME_KEY = 'frame_name'
SCALE_FACTOR_KEY = 'scale_factor'
SEGMENT_COUNTER_KEY = 'segment_counter'
SEGMENT_DURATION_KEY = 'segment_duration'
SEGMENT_END_KEY = 'segment_end'
SEGMENT_START_KEY = 'segment_start'
SEGMENTS_NR_KEY = 'segments_nr'
SEGMENTS_KEY = 'segments'
SEGMENT_TOT_FRAMES_NR_KEY = 'segment_tot_frames_nr'
SHOT_CUT_DETECTION_TIME_KEY = 'shot_cut_detection_time'
STD_MULTIPLIER_FACE_KEY = 'std_multiplier_face'
STD_MULTIPLIER_FRAME_KEY = 'std_multiplier_frame'
TAGS_FILE_PATH_KEY = 'tags_file_path'
TAGS_KEY = 'tags'
TOT_LETTERS_NR_KEY = 'tot_letters_nr'
TOT_CAPTION_SEGMENT_DURATION_KEY = 'tot_caption_segments_duration'
TOT_SEGMENT_DURATION_KEY = 'tot_segments_duration' 
TRACKED_PERSON_TAG = 'tracked_person'
TRACKING_BBOX_KEY = 'tracking_bbox'
TRACKING_MIN_INT_AREA_KEY = 'tracking_min_int_area'
USE_AGGREGATION_KEY = 'use_aggregation'
USE_ALIGNED_FACE_IN_TRACKING_KEY = 'use_aligned_face_in_tracking'
USE_BLACKLIST_KEY = 'use_blacklist'
USE_CAPTION_RECOGNITION_KEY = 'use_caption_recognition'
USE_CLOTHING_RECOGNITION_KEY = 'use_clothing_recognition'
USE_EYES_POSITION_KEY = 'use_eyes_position'
USE_FACE_RECOGNITION_KEY = 'use_face_recognition'
USE_LEVENSHTEIN_KEY = 'use_levenshtein'
USE_MAJORITY_RULE_KEY = 'use_majority_rule'
USE_MEAN_CONFIDENCE_RULE_KEY = 'use_mean_confidence_rule'
USE_MIN_CONFIDENCE_RULE_KEY = 'use_min_confidence_rule'
USE_NOSE_POS_IN_DETECTION_KEY = 'use_nose_pos_in_detection'
USE_NOSE_POS_IN_RECOGNITION_KEY = 'use_nose_pos_in_recognition'
USE_ORIGINAL_FPS_KEY = 'use_original_fps'
USE_ORIGINAL_RES_KEY = 'use_original_res'
USE_SKELETONS_KEY = 'use_skeletons'
USED_FPS_KEY = 'used_fps'
USED_FPS_FOR_CAPTIONS_KEY = 'used_fps_for_captions'
USED_RES_SCALE_FACTOR_KEY = 'used_res_scale_factor'
TESSERACT_PARENT_DIR_PATH_KEY = 'tesseract_parent_dir_path'
VARIABLE_CLOTHING_THRESHOLD_KEY = 'variable_clothing_threshold'
VIDEO_DURATION_KEY = 'video_duration'
VIDEO_FPS_KEY = 'video_fps'
VIDEO_INDEXING_PATH_KEY = 'video_indexing_path'
VIDEO_SAVED_FRAMES_KEY = 'saved_frames'
VIDEO_SEGMENTS_KEY = 'video_segments'
VIDEO_TOT_FRAMES_KEY = 'tot_frames'
