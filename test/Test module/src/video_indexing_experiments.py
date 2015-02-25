import numpy
import os
import sys

from video_indexing_test import video_indexing_experiments

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.Utils import * 

man_ann_path = r'C:\Active\Face summarization\Annotations\fic.02'

resource_path = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg'

video_idx_path_base = r'C:\Users\Maurizio\Documents\Face summarization\Test\Soglia variabile'

use_aggregation_list = [True, False]

use_nose_pos_list = [False] # TEST ONLY

test_counter = 0

for use_aggregation in use_aggregation_list:
    
    for use_nose_pos in use_nose_pos_list:

        #for conf_threshold in range(5,31,5):
        for conf_threshold in range(10,31,10): 
            
            dir_name = 'TEST ID ' + str(test_counter)
            
            video_idx_path = os.path.join(video_idx_path_base, dir_name)
            
            params = {}
            
            # Definition of parameters
            
            params[CODE_VERSION_KEY] = 1000
            
            # Face detection
            
            params[CLASSIFIERS_DIR_PATH_KEY] = r'C:\Opencv\opencv\sources\data\haarcascades'
            
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
            
            params [OFFSET_PCT_Y_KEY] = 0.50
            
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
            
            params[USE_AGGREGATION_KEY] = use_aggregation
            
            params[USE_CLOTHING_RECOGNITION_KEY] = False
            
            params[USED_FPS_KEY] = 5
            
            params[USE_NOSE_POS_IN_RECOGNITION_KEY] = use_nose_pos
            
            params[USE_ORIGINAL_FPS_KEY] = False
            
            params[USE_ORIGINAL_RES_KEY] = True
            
            params[USE_PEOPLE_CLUSTERING_KEY] = True
            
            params[VIDEO_INDEXING_PATH_KEY] = video_idx_path
            
            params[VIDEO_INDEXING_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\Results'
            
            test_counter = test_counter + 1
    
            video_indexing_experiments(resource_path, params)
