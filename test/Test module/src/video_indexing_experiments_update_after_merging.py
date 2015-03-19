import gc
import numpy
import os
import sys
import winsound

from video_indexing_test import video_indexing_experiments

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.Utils import * 

#resource_paths = [r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg'] # Portatile MP
resource_paths = [r'C:\Active\RawVideos\MONITOR072011.mpg'] # Palladium

#video_idx_path_base = r'C:\Users\Maurizio\Documents\Face summarization\Test\Soglia variabile' # Portatile MP
video_idx_path_base = r'C:\Active\Face summarization\Nuovi' # Palladium

#test_counter = 0 # Portatile MP
test_counter = 93 # Palladium
     
#update_after_merging = True # Portatile MP
update_after_merging = True # Palladium

#use_majority_rule_list = [True, False] # Portatile MP
use_majority_rule_list = [True, False] # Palladium
            
#use_aggregation = False # Portatile MP
use_aggregation = False # Palladium

#use_nose_pos_list = [True, False] # Portatile MP
use_nose_pos_list = [False, True] # Palladium

#conf_threshold_list = [120] # Portatile MP
conf_threshold_list = [5, 10, 15, 20] # Palladium
for resource_path in resource_paths:
    
    res_name = os.path.basename(resource_path) 
    
    for use_majority_rule in use_majority_rule_list:
        for use_nose_pos in use_nose_pos_list:
        
            for conf_threshold in conf_threshold_list:
                
                if(test_counter <= 104):
                    
                    test_counter = test_counter + 1
                    
                    continue
                    
                print('test_counter', test_counter)    
                    
                objs = gc.collect()                
                print('Unreachable objects', objs)
             
                # Make beep
                frequency = 404
                duration = 2000
                winsound.Beep(frequency, duration)
                
                print('conf_threshold', conf_threshold)
                            
                dir_name = 'TEST ID ' + str(test_counter)
                
                video_idx_path = os.path.join(video_idx_path_base, dir_name)
                
                params = {}
                
                # Definition of parameters
        
                #params[CODE_VERSION_KEY] = 1000 # Portatile MP
                params[CODE_VERSION_KEY] = 280 # Palladium
                
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
                
                params[UPDATE_FACE_MODEL_AFTER_MERGING_KEY] = update_after_merging
                
                params[USE_AGGREGATION_KEY] = use_aggregation
                
                params[USE_CLOTHING_RECOGNITION_KEY] = False
                
                params[USED_FPS_KEY] = 5
                
                params[USE_NOSE_POS_IN_RECOGNITION_KEY] = use_nose_pos
                
                params[USE_ORIGINAL_FPS_KEY] = False
                
                params[USE_ORIGINAL_RES_KEY] = True
                
                params[USE_PEOPLE_CLUSTERING_KEY] = True
                
                # Aggregation
                params[USE_MAJORITY_RULE_KEY] = use_majority_rule
                params[USE_MIN_CONFIDENCE_RULE_KEY] = True
                params[USE_MEAN_CONFIDENCE_RULE_KEY] = False
                
                params[VIDEO_INDEXING_PATH_KEY] = video_idx_path
                
                if(res_name == 'fic.02.mpg'):
                    
                    #params[VIDEO_INDEXING_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\Results' # Portatile MP
                    params[VIDEO_INDEXING_RESULTS_PATH_KEY] = r'C:\Active\Face summarization\File YAML e CSV con risultati' # Palladium
                    
                    #params[VIDEO_PARAMS_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\fic.02.mpg_parameters.YAML' # Portatile MP
                    params[VIDEO_PARAMS_FILE_PATH_KEY] = r'C:\Active\Face summarization\fic.02.mpg\fic.02.mpg_parameters.YAML' # Palladium
                    
                    #params[FACE_TRACKING_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\Face tracking\fic.02.mpg.YAML' # Portatile MP
                    params[FACE_TRACKING_FILE_PATH_KEY] = r'C:\Active\Face summarization\fic.02.mpg\Face tracking\fic.02.mpg.YAML' # Palladium
                    
                    #params[FACE_MODELS_DIR_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\Face models' # Portatile MP
                    params[FACE_MODELS_DIR_PATH_KEY] = r'C:\Active\Face summarization\fic.02.mpg\Face models' # Palladium
                    
                    #params[NOSE_POS_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\noses' # Portatile MP
                    params[NOSE_POS_FILE_PATH_KEY] = r'C:\Active\Face summarization\fic.02.mpg\noses' # Palladium
                    
                    #man_ann_path = r'C:\Users\Maurizio\Documents\Face summarization\Annotations\fic.02 Test' # Portatile MP
                    man_ann_path = r'C:\Active\Face summarization\Annotations\fic.02' #Palladium
                    
                    params[ANNOTATIONS_PATH_KEY] = man_ann_path
                    
                elif(res_name == 'MONITOR072011.mpg'):
                    
                    #params[VIDEO_INDEXING_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\Results' # Portatile MP
                    params[VIDEO_INDEXING_RESULTS_PATH_KEY] = r'C:\Active\Face summarization\File YAML e CSV con risultati' # Palladium
                    
                    #params[VIDEO_PARAMS_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\fic.02.mpg_parameters.YAML' # Portatile MP
                    params[VIDEO_PARAMS_FILE_PATH_KEY] = r'C:\Active\Face summarization\MONITOR072011.mpg\MONITOR072011.mpg_parameters.YAML' # Palladium
                    
                    #params[FACE_TRACKING_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\Face tracking\fic.02.mpg.YAML' # Portatile MP
                    params[FACE_TRACKING_FILE_PATH_KEY] = r'C:\Active\Face summarization\MONITOR072011.mpg\Face tracking\MONITOR072011.mpg.YAML' # Palladium
                    
                    #params[FACE_MODELS_DIR_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\Face models' # Portatile MP
                    params[FACE_MODELS_DIR_PATH_KEY] = r'C:\Active\Face summarization\MONITOR072011.mpg\Face models' # Palladium
                    
                    #params[NOSE_POS_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Face summarization\Test\fic.02.mpg\noses' # Portatile MP
                    params[NOSE_POS_FILE_PATH_KEY] = r'C:\Active\Face summarization\MONITOR072011.mpg\noses' # Palladium
                    
                    #man_ann_path = r'C:\Users\Maurizio\Documents\Face summarization\Annotations\fic.02 Test' # Portatile MP
                    man_ann_path = r'C:\Active\Face summarization\Annotations\MONITOR072011' #Palladium
                    
                    params[ANNOTATIONS_PATH_KEY] = man_ann_path         
                
                params[SIMULATE_USER_ANNOTATIONS_KEY] = True
                
                test_counter = test_counter + 1
                
                video_indexing_experiments(resource_path, params)
                
                # Make beep
                winsound.Beep(frequency, duration)
    
