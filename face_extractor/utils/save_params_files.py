import os
import sys

sys.path.append("..")
import tools.constants as c
import tools.utils as utils
import test.test_module.constants_for_experiments as ce

PARAMS_DIR_PATH = '..' + os.sep + 'test' + os.sep + 'params_files'


# Caption recognition

test_set_path = r'C:\Users\Maurizio\Documents\File di test\Dataset ridotti per test module\Caption_test'

tags_file_path = '..' + os.sep + 'test_files' + os.sep + 'caption_recognition' + os.sep + 'Tags.txt'

params = {ce.TEST_SET_PATH_KEY: test_set_path,
          c.USE_LEVENSHTEIN_KEY: True, c.LEV_RATIO_PCT_THRESH_KEY: 0,
          c.MIN_TAG_LENGTH_KEY: 0, c.TAGS_FILE_PATH_KEY: tags_file_path,
          c.USE_BLACKLIST_KEY: False}

params_file_name = 'caption_test.yml'
params_file_path = os.path.join(PARAMS_DIR_PATH, params_file_name)

utils.save_YAML_file(params_file_path, params)

# Face detection
check_eye_positions = True
classifiers_dir_path = r'C:\Opencv\opencv\sources\data\haarcascades'
eye_detection_classifier = 'haarcascade_mcs_lefteye.xml'
face_detection_algorithm = 'HaarCascadeFrontalFaceAlt2'
annotations_path = 'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-300I'
flags = 'DoCannyPruning'
min_neighbors = 5
min_size_height = 20
min_size_width = 20
face_detection_results_path = r'C:\Users\Maurizio\Documents\Risultati test\Face detection\Videolina-300I\Check_eye_positions_true'
scale_factor = 1.1
test_set_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-300I'
max_eye_angle = 0.125
min_eye_distance = 0.25
nose_detection_classifier = 'haarcascade_mcs_nose.xml'
use_nose_pos_in_detection = False

params = {c.CHECK_EYE_POSITIONS_KEY: check_eye_positions,
          c.CLASSIFIERS_DIR_PATH_KEY: classifiers_dir_path,
          c.EYE_DETECTION_CLASSIFIER_KEY: eye_detection_classifier,
          c.FACE_DETECTION_ALGORITHM_KEY: face_detection_algorithm,
          ce.ANNOTATIONS_PATH_KEY: annotations_path,
          c.FLAGS_KEY: flags,
          c.MIN_NEIGHBORS_KEY: min_neighbors,
          c.MIN_SIZE_HEIGHT_KEY: min_size_height,
          c.MIN_SIZE_WIDTH_KEY: min_size_width,
          ce.FACE_DETECTION_RESULTS_PATH_KEY: face_detection_results_path,
          ce.TEST_SET_PATH_KEY: test_set_path,
          c.MAX_EYE_ANGLE_KEY: max_eye_angle,
          c.MIN_EYE_DISTANCE_KEY: min_eye_distance,
          c.NOSE_DETECTION_CLASSIFIER_KEY: nose_detection_classifier,
          c.USE_NOSE_POS_IN_DETECTION_KEY: use_nose_pos_in_detection
          }

params_file_name = 'fd_test.yml'
params_file_path = os.path.join(PARAMS_DIR_PATH, params_file_name)

utils.save_YAML_file(params_file_path, params)

# Face recognition
aligned_faces_path = r'C:\Users\Maurizio\Documents\Risultati test\Dummy test\Aligned_faces'
cropped_face_height = 400
cropped_face_width = 200
dataset_already_divided = False
dataset_path = r'C:\Users\Maurizio\Documents\Dataset\AT&T\Dataset'
db_name = 'db'
db_models_path = r'C:\Users\Maurizio\Documents\Risultati test\Dummy test\models'
face_model_algorithm = 'LBP'
face_recognition_results_path = r'C:\Users\Maurizio\Documents\Risultati test\Dummy test\results'
LBP_grid_x = 4
LBP_grid_y = 8
LBP_neighbors = 8
LBP_radius = 1
offset_pct_x = 0.20
offset_pct_y = 0.50
training_images_nr = 9
use_eye_detection = False
use_eye_detection_in_training = False
use_eyes_position = False
use_eyes_position_in_training = False
use_face_detection_in_training = False
use_NBNN = True
use_one_file_for_face_models = True
use_resizing = False
use_weighted_regions = False

params = {c.CHECK_EYE_POSITIONS_KEY: check_eye_positions,
          c.CLASSIFIERS_DIR_PATH_KEY: classifiers_dir_path,
          c.EYE_DETECTION_CLASSIFIER_KEY: eye_detection_classifier,
          c.FACE_DETECTION_ALGORITHM_KEY: face_detection_algorithm,
          c.FLAGS_KEY: flags,
          c.MIN_NEIGHBORS_KEY: min_neighbors,
          c.MIN_SIZE_HEIGHT_KEY: min_size_height,
          c.MIN_SIZE_WIDTH_KEY: min_size_width,
          c.MAX_EYE_ANGLE_KEY: max_eye_angle,
          c.MIN_EYE_DISTANCE_KEY: min_eye_distance,
          c.NOSE_DETECTION_CLASSIFIER_KEY: nose_detection_classifier,
          c.USE_NOSE_POS_IN_DETECTION_KEY: use_nose_pos_in_detection,

          c.ALIGNED_FACES_PATH_KEY: aligned_faces_path,
          c.CROPPED_FACE_HEIGHT_KEY: cropped_face_height,
          c.CROPPED_FACE_WIDTH_KEY: cropped_face_width,
          ce.DATASET_ALREADY_DIVIDED_KEY: dataset_already_divided,
          ce.DATASET_PATH_KEY: dataset_path,
          ce.DB_NAME_KEY: db_name,
          c.DB_MODELS_PATH_KEY: db_models_path,
          ce.FACE_MODEL_ALGORITHM_KEY: face_model_algorithm,
          ce.FACE_RECOGNITION_RESULTS_PATH_KEY: face_recognition_results_path,
          c.LBP_GRID_X_KEY: LBP_grid_x,
          c.LBP_GRID_Y_KEY: LBP_grid_y,
          c.LBP_NEIGHBORS_KEY: LBP_neighbors,
          c.LBP_RADIUS_KEY: LBP_radius,
          c.OFFSET_PCT_X_KEY: offset_pct_x,
          c.OFFSET_PCT_Y_KEY: offset_pct_y,
          ce.TRAINING_IMAGES_NR_KEY: training_images_nr,
          ce.USE_EYE_DETECTION_KEY: use_eye_detection,
          ce.USE_EYE_DETECTION_IN_TRAINING_KEY: use_eye_detection_in_training,
          c.USE_EYES_POSITION_KEY: use_eyes_position,
          ce.USE_EYES_POSITION_IN_TRAINING_KEY: use_eyes_position_in_training,
          ce.USE_FACE_DETECTION_IN_TRAINING_KEY: use_face_detection_in_training,
          ce.USE_NBNN_KEY: use_NBNN,
          ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY: use_one_file_for_face_models,
          ce.USE_RESIZING_KEY: use_resizing,
          ce.USE_WEIGHTED_REGIONS_KEY: use_weighted_regions
          }

params_file_name = 'fr_test.yml'
params_file_path = os.path.join(PARAMS_DIR_PATH, params_file_name)

utils.save_YAML_file(params_file_path, params)

# Video indexing with no people recognition
ann_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'
all_cloth_bboxes_in_frames = False
clothes_bbox_height = 1.0
clothes_bbox_width = 2.0
clothes_check_method = 'Max'
clothes_conf_thresh = 8
use_3_bboxes = False
use_dom_color = False
use_mean_x = False
conf_thresh = 14
half_window_size = 10
kernel_size = 25
max_faces_in_model = 1000
max_fr_with_missed_det = 5
max_nose_diff = 0.05
min_cloth_model_size = 5
min_det_pct = 0.3
min_segment_duration = 1
neck_height = 0
sim_user_ann = False
std_mult_face = 20
std_mult_frame = 20
tracking_min_int_area = 0.1
use_aggr = False
use_aligned_face_in_tracking = True
use_clothing = True
use_maj_rule = True
use_min_conf_rule = True
use_mean_conf_rule = False
use_nose_pos_in_rec = False
use_or_fps = False
use_or_res = True
use_people_clustering = True
use_people_rec = False
used_fps = 5.0
variable_cloth_thresh = False
video_indexing_path = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction'
video_indexing_results = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction\Results'

params = {c.CHECK_EYE_POSITIONS_KEY: check_eye_positions,
          c.CLASSIFIERS_DIR_PATH_KEY: classifiers_dir_path,
          c.EYE_DETECTION_CLASSIFIER_KEY: eye_detection_classifier,
          c.FACE_DETECTION_ALGORITHM_KEY: face_detection_algorithm,
          c.FLAGS_KEY: flags,
          c.MIN_NEIGHBORS_KEY: min_neighbors,
          c.MIN_SIZE_HEIGHT_KEY: min_size_height,
          c.MIN_SIZE_WIDTH_KEY: min_size_width,
          c.MAX_EYE_ANGLE_KEY: max_eye_angle,
          c.MIN_EYE_DISTANCE_KEY: min_eye_distance,
          c.NOSE_DETECTION_CLASSIFIER_KEY: nose_detection_classifier,
          c.USE_NOSE_POS_IN_DETECTION_KEY: use_nose_pos_in_detection,

          c.CROPPED_FACE_HEIGHT_KEY: cropped_face_height,
          c.CROPPED_FACE_WIDTH_KEY: cropped_face_width,
          c.LBP_GRID_X_KEY: LBP_grid_x,
          c.LBP_GRID_Y_KEY: LBP_grid_y,
          c.LBP_NEIGHBORS_KEY: LBP_neighbors,
          c.LBP_RADIUS_KEY: LBP_radius,
          c.OFFSET_PCT_X_KEY: offset_pct_x,
          c.OFFSET_PCT_Y_KEY: offset_pct_y,

          ce.ANNOTATIONS_PATH_KEY: ann_path,
          c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY: all_cloth_bboxes_in_frames,
          c.CLOTHES_BBOX_HEIGHT_KEY: clothes_bbox_height,
          c.CLOTHES_BBOX_WIDTH_KEY: clothes_bbox_width,
          c.CLOTHES_CHECK_METHOD_KEY: clothes_check_method,
          c.CLOTHES_CONF_THRESH_KEY: clothes_conf_thresh,
          c.CLOTHING_REC_USE_3_BBOXES_KEY: use_3_bboxes,
          c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: use_dom_color,
          c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY: use_mean_x,
          c.CONF_THRESHOLD_KEY: conf_thresh,
          c.HALF_WINDOW_SIZE_KEY: half_window_size,
          c.HIST_SMOOTHING_KERNEL_SIZE_KEY: kernel_size,
          c.MAX_FACES_IN_MODEL_KEY: max_faces_in_model,
          c.MAX_FR_WITH_MISSED_DET_KEY: max_fr_with_missed_det,
          c.MAX_NOSE_DIFF_KEY: max_nose_diff,
          c.MIN_CLOTH_MODEL_SIZE_KEY: min_cloth_model_size,
          c.MIN_DETECTION_PCT_KEY: min_det_pct,
          c.MIN_SEGMENT_DURATION_KEY: min_segment_duration,
          c.NECK_HEIGHT_KEY: neck_height,
          ce.SIMULATE_USER_ANNOTATIONS_KEY: sim_user_ann,
          c.STD_MULTIPLIER_FACE_KEY: std_mult_face,
          c.STD_MULTIPLIER_FRAME_KEY: std_mult_frame,
          c.TRACKING_MIN_INT_AREA_KEY: tracking_min_int_area,
          c.USE_AGGREGATION_KEY: use_aggr,
          c.USE_ALIGNED_FACE_IN_TRACKING_KEY: use_aligned_face_in_tracking,
          c.USE_CLOTHING_RECOGNITION_KEY: use_clothing,
          c.USE_MAJORITY_RULE_KEY: use_maj_rule,
          c.USE_MIN_CONFIDENCE_RULE_KEY: use_min_conf_rule,
          c.USE_MEAN_CONFIDENCE_RULE_KEY: use_mean_conf_rule,
          c.USE_NOSE_POS_IN_RECOGNITION_KEY: use_nose_pos_in_rec,
          c.USE_ORIGINAL_FPS_KEY: use_or_fps,
          c.USE_ORIGINAL_RES_KEY: use_or_res,
          ce.USE_PEOPLE_CLUSTERING_KEY: use_people_clustering,
          ce.USE_PEOPLE_RECOGNITION_KEY: use_people_rec,
          c.USED_FPS_KEY: used_fps,
          c.VARIABLE_CLOTHING_THRESHOLD_KEY: variable_cloth_thresh,
          c.VIDEO_INDEXING_PATH_KEY: video_indexing_path,
          ce.VIDEO_INDEXING_RESULTS_PATH_KEY: video_indexing_results
          }

params_file_name = 'video_indexing_test_no_people_recognition.yml'
params_file_path = os.path.join(PARAMS_DIR_PATH, params_file_name)

utils.save_YAML_file(params_file_path, params)
