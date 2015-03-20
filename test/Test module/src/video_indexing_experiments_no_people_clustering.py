import numpy
import os
import sys
import winsound

from video_indexing_test import video_indexing_experiments

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.Utils import * 

#man_ann_path = r'C:\Users\Maurizio\Documents\Face summarization\Annotations\fic.02 Test' # Portatile MP
man_ann_path = r'C:\Active\Face summarization\Annotations\fic.02' #Palladium

#resource_path = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg' # Portatile MP
resource_path = r'C:\Active\RawVideos\fic.02.mpg' # Palladium

#video_idx_path_base = r'C:\Users\Maurizio\Documents\Face summarization\Test' # Portatile MP
video_idx_path_base = r'C:\Active\Face summarization' # Palladium

#test_counter = 0 # Portatile MP
test_counter = 0 # Palladium

use_nose_pos = True # Palladim    
			
dir_name = 'TEST ID ' + str(test_counter)

conf_threshold = 0

#video_idx_path = os.path.join(video_idx_path_base, dir_name)
video_idx_path = video_idx_path_base

params = {}

# Definition of parameters

params[ANNOTATIONS_PATH_KEY] = man_ann_path

#params[CODE_VERSION_KEY] = -1 # Portatile MP
params[CODE_VERSION_KEY] = 280# Palladium

# Face detection

#params[CLASSIFIERS_DIR_PATH_KEY] = r'C:\Opencv\opencv\sources\data\haarcascades' # Portatile MP
params[CLASSIFIERS_DIR_PATH_KEY] = r'C:\opencv\sources\data\haarcascades' # Palladium

params[EYE_DETECTION_CLASSIFIER_KEY] = 'haarcascade_mcs_lefteye.xml'

params[FACE_DETECTION_ALGORITHM_KEY] = 'HaarCascadeFrontalAndProfileFaces2'

params[FLAGS_KEY] = 'DoCannyPruning'

params[MIN_NEIGHBORS_KEY] = 5

params[MIN_SIZE_HEIGHT_KEY] = 20

params[MIN_SIZE_WIDTH_KEY] = 20

params[SCALE_FACTOR_KEY] = 1.1

params[NOSE_DETECTION_CLASSIFIER_KEY] = 'nose_detection_classifier'

params[USE_NOSE_POS_IN_DETECTION_KEY] = False

params[MIN_SIZE_HEIGHT_KEY] = 20

params[MIN_SIZE_WIDTH_KEY] = 20

# Face recognition

params[OFFSET_PCT_X_KEY] = 0.20

params[OFFSET_PCT_Y_KEY] = 0.50

params[CROPPED_FACE_WIDTH_KEY] = 200

params[CROPPED_FACE_HEIGHT_KEY] = 400

params[FACE_MODEL_ALGORITHM_KEY] = 'LBP'

params[LBP_RADIUS_KEY] = 1
params[LBP_NEIGHBORS_KEY] = 8
params[LBP_GRID_X_KEY] = 4
params[LBP_GRID_Y_KEY]  = 8

params[USE_EYES_POSITION_KEY] = True

# Video indexing
params[CONF_THRESHOLD_KEY] = conf_threshold

params[HALF_WINDOW_SIZE_KEY] = 10

params[MAX_FACES_IN_MODEL_KEY] = 1000

params[MAX_FR_WITH_MISSED_DET_KEY] = 5

params[MAX_NOSE_DIFF_KEY] = 0.05

params[MIN_DETECTION_PCT_KEY] = 0.3

params[MIN_SEGMENT_DURATION_KEY] = 1

params[STD_MULTIPLIER_FACE_KEY] = 20

params[STD_MULTIPLIER_FRAME_KEY] = 20

params[TRACKING_MIN_INT_AREA_KEY] = 0.5

params[USE_CLOTHING_RECOGNITION_KEY] = False

params[USED_FPS_KEY] = 5

params[USE_NOSE_POS_IN_RECOGNITION_KEY] = use_nose_pos

params[USE_ORIGINAL_FPS_KEY] = False

params[USE_ORIGINAL_RES_KEY] = True

params[USE_PEOPLE_CLUSTERING_KEY] = False

# Aggregation
params[USE_MAJORITY_RULE_KEY] = True
params[USE_MIN_CONFIDENCE_RULE_KEY] = True
params[USE_MEAN_CONFIDENCE_RULE_KEY] = False

params[VIDEO_INDEXING_PATH_KEY] = video_idx_path

params[SIMULATE_USER_ANNOTATIONS_KEY] = False

test_counter = test_counter + 1

video_indexing_experiments(resource_path, params)
    
