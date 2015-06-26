import os
import sys

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_models import FaceModels
import test.test_module.constants_for_experiments as ce
from test.test_module.video_indexing_test import video_indexing_experiments

# TODO CHANGE
video_idx_path = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction'  # Portatile MP
video_idx_path = r'C:\Users\Maurizio\Documents\Face summarization\Test\Caption recognition' # Portatile MP

# Fixed parameters

# Face detection
check_eye_positions = False # TODO CHANGE?
# TODO CHANGE
classifiers_dir_path = r'C:\Opencv\opencv\sources\data\haarcascades'
eye_detection_classifier = 'haarcascade_mcs_lefteye.xml'
face_detection_algorithm = 'HaarCascadeFrontalAndProfileFaces2'  # TODO CHANGE?
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
ann_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'
# TODO CHANGE
aligned_faces_path = r'C:\Users\Maurizio\Documents\Aligned faces'
all_cloth_bboxes_in_frames = False
clothes_bbox_height = 1.0
clothes_bbox_width = 2.0
clothes_check_method = 'Max'
clothes_conf_thresh = 8
conf_threshold = 14
use_mean_x = False
half_window_size = 10
kernel_size = 25
max_faces_in_model = 1000
max_fr_with_missed_det = 5
max_nose_diff = 0.05
min_cloth_model_size = 5
min_det_pct = 0.3
min_segment_duration = 1
neck_height = 0
sim_user_ann = True
std_mult_face = 20
std_mult_frame = 20
tracking_min_int_area = 0.1
use_3_bboxes = False
use_aggr = False
use_aligned_face_in_tracking = False  # TODO CHANGE?
use_clothing = True
use_dom_color = False
use_maj_rule = True
use_min_conf_rule = True
use_mean_conf_rule = False
use_nose_pos_in_rec = False
use_or_fps = False
use_or_res = True
use_people_clustering = True
use_people_rec = True
used_fps = 5.0
variable_cloth_thresh = False
# TODO CHANGE
video_idx_results_path = r'C:\Users\Maurizio\Documents\Video indexing\People clustering\Results' # Portatile MP
# TODO CHANGE
video_idx_results_file_name = 'Pippo'

# People recognition
global_face_models_min_diff = 5
# TODO CHANGE
global_face_rec_data_dir_path = r'C:\Users\Maurizio\Documents\Risultati test\People recognition\Global face recognition' # Portatile MP
min_tag_length = 10
use_blacklist = True
use_caption_rec = True
use_face_rec = False
use_levenshtein = True
used_fps_for_captions = 1.0
# TODO CHANGE
tags_file_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\tools\Tags.txt'
# TODO CHANGE
tessaract_parent_dir_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\face_extractor\tools'

# Variable parameters

resource_paths = ['fic.02.mpg']
resource_ids = ['fic.02.mpg']

# TODO CHANGE
# global_face_rec_thresh_list = range(2, 51, 2)
global_face_rec_thresh_list = [8]

# TODO CHANGE
# lev_ratio_pct_thresh_list = np.arange(0, 1.01, 0.05)
lev_ratio_pct_thresh_list = [0.8]

test_counter = 0  # TODO CHANGE

res_counter = 0

for resource_path in resource_paths:

    resource_id = resource_ids[res_counter]

    dir_name = 'TEST ID ' + str(test_counter)

    print(dir_name)

    for lev_ratio_pct_thresh in lev_ratio_pct_thresh_list:

        for global_face_rec_thresh in global_face_rec_thresh_list:

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
                      c.ALIGNED_FACES_PATH: aligned_faces_path,
                      c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY: all_cloth_bboxes_in_frames,
                      c.CLOTHES_BBOX_HEIGHT_KEY: clothes_bbox_height,
                      c.CLOTHES_BBOX_WIDTH_KEY: clothes_bbox_width,
                      c.CLOTHES_CHECK_METHOD_KEY: clothes_check_method,
                      c.CLOTHES_CONF_THRESH_KEY: clothes_conf_thresh,
                      c.CLOTHING_REC_USE_3_BBOXES_KEY: use_3_bboxes,
                      c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY: use_dom_color,
                      c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY: use_mean_x,
                      c.CONF_THRESHOLD_KEY: conf_threshold,
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
                      c.VIDEO_INDEXING_PATH_KEY: video_idx_path,
                      ce.VIDEO_INDEXING_RESULTS_PATH_KEY: video_idx_results_path,
                      ce.VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME_KEY: video_idx_results_file_name,

                      c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY: global_face_models_min_diff,
                      c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY: global_face_rec_data_dir_path,
                      c.GLOBAL_FACE_REC_THRESHOLD_KEY: global_face_rec_thresh,
                      c.LEV_RATIO_PCT_THRESH_KEY: lev_ratio_pct_thresh,
                      c.MIN_TAG_LENGTH_KEY: min_tag_length,
                      c.USE_BLACKLIST_KEY: use_blacklist,
                      c.USE_CAPTION_RECOGNITION_KEY: use_caption_rec,
                      c.USE_FACE_RECOGNITION_KEY: use_face_rec,
                      c.USE_LEVENSHTEIN_KEY: use_levenshtein,
                      c.USED_FPS_FOR_CAPTIONS_KEY: used_fps_for_captions,
                      # c.TAGS_FILE_PATH_KEY: tags_file_path,
                      c.TESSERACT_PARENT_DIR_PATH_KEY: tessaract_parent_dir_path
                      }

            if test_counter == 0:
                # Add face models and blacklist
                # TODO CHANGE
                images_dir_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\80 persone'
                fm = FaceModels(params)
                # fm.create_models_from_whole_images(images_dir_path)
                fm.add_blacklist_item('Al_telefono')
                fm.add_blacklist_item('Intervista_di')
                fm.add_blacklist_item('Riprese_Montaggio')

                # Empty directory with temporary aligned faces
                for item in os.listdir(aligned_faces_path):
                    item_complete_path = os.path.join(aligned_faces_path, item)
                    os.remove(item_complete_path)

            video_indexing_experiments(resource_path, resource_id, params)

            test_counter += 1

    res_counter += 1