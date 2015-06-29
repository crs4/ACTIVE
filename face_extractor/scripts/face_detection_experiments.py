import os
import sys

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
import test.test_module.constants_for_experiments as ce
from test.test_module.fd_test import fd_experiments

# Fixed parameters

check_eye_positions = True
# TODO CHANGE
# classifiers_dir_path = r'C:\Opencv\opencv\sources\data\haarcascades' # Portatile MP
classifiers_dir_path = r'C:\Active\OpenCV classifiers'  # Palladium
eye_detection_classifier = 'haarcascade_mcs_lefteye.xml'
# TODO CHANGE
# annotations_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-300I' # Portatile MP
annotations_path = r'C:\Active\Dataset\Annotazioni\Videolina-300I' # Palladium
flags = 'DoCannyPruning'
min_neighbors = 5
min_size_height = 20
min_size_width = 20
# TODO CHANGE
# face_detection_results_path = r'C:\Users\Maurizio\Documents\Risultati test\Face detection\Videolina-300I\Check_eye_positions_true'
face_detection_results_path = r'C:\Active\Risultati test\Face detection\Videolina-300I\Check_eye_positions_true'
scale_factor = 1.1
# TODO CHANGE
# test_set_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-300I' # Portatile MP
test_set_path = r'C:\Active\Dataset\Videolina-300I' # Palladium

max_eye_angle = 0.125
min_eye_distance = 0.25
nose_detection_classifier = 'haarcascade_mcs_nose.xml'
use_nose_pos_in_detection = False

# Variable parameters

# face_detection_algorithms = ['HaarCascadeFrontalFaceAlt',
#                              'HaarCascadeFrontalFaceAltTree',
#                              'HaarCascadeFrontalFaceAlt2',
#                              'HaarCascadeFrontalFaceDefault',
#                              'HaarCascadeProfileFace',
#                              'HaarCascadeFrontalAndProfileFaces',
#                              'LBPCascadeFrontalface',
#                              'LBPCascadeProfileFace',
#                              'LBPCascadeFrontalAndProfileFaces',
#                              'HaarCascadeFrontalAndProfileFaces2']

face_detection_algorithms = ['LBPCascadeProfileFace',
                             'LBPCascadeFrontalAndProfileFaces',
                             'HaarCascadeFrontalAndProfileFaces2']

for face_detection_algorithm in face_detection_algorithms:

    print face_detection_algorithm

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

    fd_experiments(params, False)
