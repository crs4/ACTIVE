import os
import sys

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)
import tools.constants as c

# TODO CHANGE
# For execution from command line
# path_to_be_appended = ".." + os.sep + "test"
# sys.path.append(path_to_be_appended)
# import test_module.constants_for_experiments as ce
# from test_module.video_indexing_test import video_indexing_experiments

# For execution from pyCharm
import test.test_module.constants_for_experiments as ce
from test.test_module.video_indexing_test import video_indexing_experiments

# TODO CHANGE
code_version = 347

#  TODO CHANGE
# video_idx_path = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction'  # Portatile MP
video_idx_path = r'C:\Active\Face tracking'  # Palladium

# Fixed parameters

# Face detection
check_eye_positions = True
# TODO CHANGE
# classifiers_dir_path = r'C:\Opencv\opencv\sources\data\haarcascades' # Portatile MP
classifiers_dir_path = r'C:\opencv\sources\data\haarcascades' # Palladium
eye_detection_classifier = 'haarcascade_mcs_lefteye.xml'
face_detection_algorithm = 'HaarCascadeFrontalFaceAlt2'
flags = 'DoCannyPruning'
min_neighbors = 5
min_size_height = 20
min_size_width = 20
scale_factor = 1.1
max_eye_angle = 0.125
min_eye_distance = 0.25
nose_detection_classifier = 'haarcascade_mcs_nose.xml'
use_nose_pos_in_detection = False

# Face recognition
cropped_face_height = 400
cropped_face_width = 200
LBP_grid_x = 4
LBP_grid_y = 8
LBP_neighbors = 8
LBP_radius = 1
offset_pct_x = 0.20
offset_pct_y = 0.50

# Video indexing with no people recognition
# TODO CHANGE
# ann_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'  # Portatile MP
# ann_path = r'C:\Active\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'  # Palladium - fic.02
ann_path = r'C:\Active\Dataset\Annotazioni\Videolina-15V\MONITOR072011\Simple annotations'  # Palladium - MONITOR072011
half_window_size = 10
max_fr_with_missed_det = 50
max_nose_diff = 0.05
min_det_pct = 0.3
min_segment_duration = 1
sim_user_ann = False
std_mult_face = 20
std_mult_frame = 20
tracking_min_int_area = 0.1
use_aligned_face_in_tracking = True
use_maj_rule = True
use_min_conf_rule = True
use_mean_conf_rule = False
use_nose_pos_in_rec = False
use_or_fps = False
use_or_res = True
use_people_clustering = False
use_people_rec = False
used_fps = 5.0
# TODO CHANGE
# video_idx_results_path = r'C:\Users\Maurizio\Documents\Video indexing\People clustering\Results'  # Portatile MP
video_idx_results_path = r'C:\Active\Risultati test\Face tracking'  # Palladium
video_idx_results_file_name = 'Results'

# Variable parameters

# resource_path_list = [r'C:\Active\RawVideos\fic.02.mpg', r'C:\Active\RawVideos\MONITOR072011.mpg']
# resource_path_list = [r'C:\Active\RawVideos\fic.02.mpg']
resource_path_list = [r'C:\Active\RawVideos\MONITOR072011.mpg']
resource_id_list = ['fic.02.mpg', 'MONITOR072011.mpg']

counter = 1

for resource_path in resource_path_list:

    resource_id = resource_id_list[counter]
    params = {ce.CODE_VERSION_KEY: code_version,

              c.CHECK_EYE_POSITIONS_KEY: check_eye_positions,
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
              c.HALF_WINDOW_SIZE_KEY: half_window_size,
              c.MAX_FR_WITH_MISSED_DET_KEY: max_fr_with_missed_det,
              c.MAX_NOSE_DIFF_KEY: max_nose_diff,
              c.MIN_DETECTION_PCT_KEY: min_det_pct,
              c.MIN_SEGMENT_DURATION_KEY: min_segment_duration,
              ce.SIMULATE_USER_ANNOTATIONS_KEY: sim_user_ann,
              c.STD_MULTIPLIER_FACE_KEY: std_mult_face,
              c.STD_MULTIPLIER_FRAME_KEY: std_mult_frame,
              c.TRACKING_MIN_INT_AREA_KEY: tracking_min_int_area,
              c.USE_ALIGNED_FACE_IN_TRACKING_KEY: use_aligned_face_in_tracking,
              c.USE_MAJORITY_RULE_KEY: use_maj_rule,
              c.USE_MIN_CONFIDENCE_RULE_KEY: use_min_conf_rule,
              c.USE_MEAN_CONFIDENCE_RULE_KEY: use_mean_conf_rule,
              c.USE_NOSE_POS_IN_RECOGNITION_KEY: use_nose_pos_in_rec,
              c.USE_ORIGINAL_FPS_KEY: use_or_fps,
              c.USE_ORIGINAL_RES_KEY: use_or_res,
              ce.USE_PEOPLE_CLUSTERING_KEY: use_people_clustering,
              ce.USE_PEOPLE_RECOGNITION_KEY: use_people_rec,
              c.USED_FPS_KEY: used_fps,
              c.VIDEO_INDEXING_PATH_KEY: video_idx_path,
              ce.VIDEO_INDEXING_RESULTS_PATH_KEY: video_idx_results_path,
              ce.VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME_KEY: video_idx_results_file_name
              }

    video_indexing_experiments(resource_path, resource_id, params)

    counter += 1


