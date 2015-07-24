import os
import shutil
import subprocess
import sys

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
import tools.utils as utils
from tools.face_models import FaceModels

import constants_for_experiments as ce
from video_indexing_test import video_indexing_experiments

# TODO CHANGE
# video_idx_path = r'C:\Users\Maurizio\Documents\Video indexing\Face extraction'  # Portatile MP
video_idx_path = r'C:\Active\People recognition'  # Palladium
code_version = 372

# Fixed parameters

# Face detection
# TODO CHANGE
aligned_faces_path = r'C:\Active\Aligned faces'  # Palladium
check_eye_positions = True
# TODO CHANGE
# classifiers_dir_path = r'C:\Opencv\opencv\sources\data\haarcascades' # Portatile MP
classifiers_dir_path = r'C:\Opencv\sources\data\haarcascades'  # Palladium
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

# Video indexing
all_cloth_bboxes_in_frames = False  # TODO CHANGE?
clothes_bbox_height = 1.0
clothes_bbox_width = 2.0
clothes_check_method = 'Max'
clothes_conf_thresh = 8
conf_threshold = 8  # TODO CHANGE?
use_mean_x = False
half_window_size = 10
hsv_channels = 3  # TODO CHANGE?
kernel_size = 25
max_faces_in_model = 1000
max_fr_with_missed_det = 50
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
use_aligned_face_in_tracking = True
use_clothing = False
use_dom_color = False
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
# video_idx_results_path = r'C:\Users\Maurizio\Documents\Video indexing\People clustering\Results'
video_idx_results_path = r'C:\Active\Risultati test\People recognition'  # Palladium
video_idx_results_file_name = 'People_recognition'

# People recognition
global_face_models_min_diff = -1
# TODO CHANGE
# global_face_rec_data_dir_path = r'C:\Users\Maurizio\Documents\Risultati test\People recognition\Global face recognition' # Portatile MP
global_face_rec_data_dir_path = r'C:\Active\People recognition\Global face recognition data'  # Palladium
lev_ratio_pct_thresh = 0.8
min_frames_per_caption = 4
min_tag_length = 10
# TODO CHANGE
training_set_path = r'C:\Active\Dataset\Videolina-960I-80P-whole_images\80 persone'  # Palladium
use_blacklist = True
use_caption_rec = False
use_face_rec = True
use_levenshtein = True
used_fps_for_captions = 1.0
# TODO CHANGE
# tags_file_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\tools\Tags.txt'
# TODO CHANGE
# tessaract_parent_dir_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\face_extractor\tools'  # Portatile MP
tesseract_parent_dir_path = r'C:\Active\Mercurial\tools'  # Palladium
# TODO CHANGE
word_blacklist_path = r'C:\Active\Dataset\Word_blacklist.txt'  # Palladium

# Variable parameters

resource_paths = ['C:\Active\RawVideos\fic.02.mpg', 'C:\Active\RawVideos\MONITOR072011.mpg']
resource_ids = ['fic.02.mpg', 'MONITOR072011.mpg']

# TODO CHANGE
global_face_rec_thresh_list = range(2, 51, 2)
# global_face_rec_thresh_list = [8]

# TODO CHANGE
use_majority_rule_list = [True, False]
# use_majority_rule_list = [True]

test_counter = 0

res_counter = 0

for resource_path in resource_paths:

    resource_id = resource_ids[res_counter]

    dir_name = 'TEST ID ' + str(test_counter)

    print(dir_name)

    for use_maj_rule in use_majority_rule_list:

        for global_face_rec_thresh in global_face_rec_thresh_list:

            params = {ce.CODE_VERSION_KEY: code_version,

                      c.ALIGNED_FACES_PATH_KEY: aligned_faces_path,
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

                      c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY: all_cloth_bboxes_in_frames,
                      c.CLOTHES_BBOX_HEIGHT_KEY: clothes_bbox_height,
                      c.CLOTHES_BBOX_WIDTH_KEY: clothes_bbox_width,
                      c.CLOTHES_CHECK_METHOD_KEY: clothes_check_method,
                      c.CLOTHES_CONF_THRESH_KEY: clothes_conf_thresh,
                      c.CLOTHING_REC_HSV_CHANNELS_NR: hsv_channels,
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
                      c.MIN_FRAMES_PER_CAPTION_KEY: min_frames_per_caption,
                      c.MIN_TAG_LENGTH_KEY: min_tag_length,
                      ce.TRAINING_SET_PATH_KEY: training_set_path,
                      c.USE_BLACKLIST_KEY: use_blacklist,
                      c.USE_CAPTION_RECOGNITION_KEY: use_caption_rec,
                      c.USE_FACE_RECOGNITION_KEY: use_face_rec,
                      c.USE_LEVENSHTEIN_KEY: use_levenshtein,
                      c.USED_FPS_FOR_CAPTIONS_KEY: used_fps_for_captions,
                      # c.TAGS_FILE_PATH_KEY: tags_file_path,
                      c.TESSERACT_PARENT_DIR_PATH_KEY: tesseract_parent_dir_path,
                      ce.WORD_BLACKLIST_FILE_PATH_KEY: word_blacklist_path
                      }

            # TODO CHANGE
            if resource_id == 'fic.02.mpg':
                params[ce.ANNOTATIONS_PATH_KEY] = r'C:\Active\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'
            elif resource_id == 'MONITOR072011.mpg':
                params[ce.ANNOTATIONS_PATH_KEY] = r'C:\Active\Dataset\Annotazioni\Videolina-15V\MONITOR072011\Simple annotations'

            # TODO CHANGE
            # Save file with parameters
            # params_file_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\video_indexing_experiments_people_recognition.yml' Portatile MP
            params_file_path = r'C:\Active\Params\video_indexing_experiments_people_recognition.yml'
            utils.save_YAML_file(params_file_path, params)

            # # Launch subprocess
            # if test_counter == 0:
            #     command = ('python video_indexing_test.py -resource_path ' +
            #                resource_path + ' -resource_id ' + resource_id +
            #                ' -config ' + params_file_path +
            #                ' --create_models --no_software_test')
            # else:
            command = ('python video_indexing_test.py -resource_path ' +
                       resource_path + ' -resource_id ' + resource_id +
                       ' -config ' + params_file_path +
                       ' --no_software_test')
            subprocess.call(command)

            # Move directories with automatic annotations
            detailed_results_path = r'C:\Active\People recognition\Risultati dettagliati'
            old_ann_path = os.path.join(video_idx_path, str(resource_id), 'Face extraction\Annotations')
            new_ann_path = os.path.join(detailed_results_path, str(resource_id), 'Only_faces', dir_name, 'Annotations')
            shutil.move(old_ann_path, new_ann_path)
            old_simple_ann_path = os.path.join(video_idx_path, str(resource_id), 'Face extraction\Simple annotations')
            new_simple_ann_path = os.path.join(detailed_results_path, str(resource_id), 'Only_faces', dir_name, 'Simple annotations')
            shutil.move(old_simple_ann_path, new_simple_ann_path)

            # Move YAML file with recognition results
            file_name = str(resource_id) + '.YAML'
            old_file_path = os.path.join(video_idx_path, str(resource_id), c.FACE_EXTRACTION_DIR, c.FACE_RECOGNITION_DIR, file_name)
            new_file_path = os.path.join(detailed_results_path, str(resource_id), 'Only_faces', dir_name, file_name)
            shutil.move(old_file_path, new_file_path)

            test_counter += 1

    res_counter += 1
