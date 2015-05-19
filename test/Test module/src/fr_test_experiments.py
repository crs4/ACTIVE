from fr_test import fr_experiments
import os
import sys
sys.path.append("../../..")
import tools.Constants as c
from tools.Utils import save_YAML_file

#lbp_parameters_list = ((1,8,4,4,0.20,0.20), (1,8,4,4,0.30,0.30),(1,8,8,8,0.20,0.20), (1,8,8,8,0.30,0.30), (1,8,4,8,0.20,0.50))
#face_height_list = (200, 200, 200, 200, 400)

lbp_parameters_list =  ((1,8,4,8,0.20,0.50),)
face_height_list = (400,)
    
counter = 0 
for lbp_parameters in lbp_parameters_list:

    lbp_radius = lbp_parameters[0]
    lbp_neighbors = lbp_parameters[1]
    lbp_grid_x = lbp_parameters[2]
    lbp_grid_y = lbp_parameters[3]
    offset_pct_x = lbp_parameters[4]
    offset_pct_y = lbp_parameters[5]
    
    #for num_people in [5,10,20,40,80]:
    for num_people in [80]:
    
        params = {}
        
        # Face detection
        
        params[c.CLASSIFIERS_DIR_PATH_KEY] = r'C:\OpenCV\opencv\sources\data\haarcascades' # Portatile MP
        #params[c.CLASSIFIERS_DIR_PATH_KEY] = r'C:\opencv\sources\data\haarcascades' # Palladium
        
        params[c.EYE_DETECTION_CLASSIFIER_KEY] = 'haarcascade_mcs_lefteye.xml'
        
        params[c.FACE_DETECTION_ALGORITHM_KEY] = 'HaarCascadeFrontalAndProfileFaces2'
        
        #params[c.ANNOTATIONS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-300I' # Portatile MP
        
        params[c.FLAGS_KEY] = 'DoCannyPruning'
        
        params[c.MIN_NEIGHBORS_KEY] = 5
        
        params[c.MIN_SIZE_HEIGHT_KEY] = 20
        
        params[c.MIN_SIZE_WIDTH_KEY] = 20
        
        #params[c.RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face detection\Videolina-300I' # Portatile MP
        
        params[c.SCALE_FACTOR_KEY] = 1.1
        
        #params[c.TEST_SET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-300I' # Portatile MP
        
        params[c.MOUTH_DETECTION_CLASSIFIER_KEY] = 'haarcascade_mcs_mouth.xml'
        
        params[c.NOSE_DETECTION_CLASSIFIER_KEY] = 'haarcascade_mcs_nose.xml'
        
        #params[c.SOFTWARE_TEST_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\SoftwareTestingFiles\Arnold.jpg' # Portatile MP
        
        params[c.USE_NOSE_POS_IN_DETECTION_KEY] = False
        
        # Face recognition
        
        params[c.ALIGNED_FACES_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\Aligned faces 2' # Portatile MP
        #params[c.ALIGNED_FACES_PATH_KEY] = r'C:\Active\Dataset\Videolina-960I-80P-whole_images\Aligned faces' # Palladium
        
        params[c.CROPPED_FACE_HEIGHT_KEY] = face_height_list[counter]
        
        params[c.CROPPED_FACE_WIDTH_KEY] = 200
        
        params[c.DATASET_ALREADY_DIVIDED_KEY] = True
        
        params[c.DATASET_PATH_KEY] = ''
        
        path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\Face models' # Portatile MP
        #path = r'C:\Active\Dataset\Videolina-960I-80P-whole_images\Face models' # Palladium
        
        name = ('Videolina-960I-80P-whole_images_' + str(num_people) + 
        '_people_' + str(lbp_radius) + '_' + str(lbp_neighbors) + '_' + 
        str(lbp_grid_x) + '_' + str(lbp_grid_y) + '_' + 
        str(offset_pct_x) + '_' + str(offset_pct_y) )
        
        params[c.DB_NAME_KEY] = os.path.join(path, name)
        
        params[c.DB_MODELS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\Face models' # Portatile MP
        #params[c.DB_MODELS_PATH_KEY] = r'C:\Active\Dataset\Videolina-960I-80P-whole_images\Face models' # Palladium
        
        params[c.FACE_MODEL_ALGORITHM_KEY] = 'LBP'
        
        #params[c.FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\Videolina-798I-28P' # Portatile MP
        #params[c.FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Active\Risultati test\Face recognition\Videolina-80I-80P-whole_images' # Palladium
        params[c.FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Dummy test'
        
        #params[c.TEST_SET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-798I-28P' # Portatile MP
        params[c.TEST_SET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-80I-80P-whole_images\\' + str(num_people) + ' persone' # Portatile MP
        #params[c.TEST_SET_PATH_KEY] = r'C:\Active\Dataset\Videolina-80I-80P-whole_images\\' + str(num_people) + ' persone' # Palladium
        
        params[c.TRAINING_SET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\\' + str(num_people) + ' persone' # Portatile MP
        #params[c.TRAINING_SET_PATH_KEY] = r'C:\Active\Dataset\Videolina-960I-80P-whole_images\\' + str(num_people) + ' persone' # Palladium
        
        params[c.LBP_GRID_X_KEY] = lbp_grid_x
        
        params[c.LBP_GRID_Y_KEY] = lbp_grid_y
        
        params[c.LBP_NEIGHBORS_KEY] = lbp_neighbors
        
        params[c.LBP_RADIUS_KEY] = lbp_radius
        
        params[c.OFFSET_PCT_X_KEY] = offset_pct_x
        
        params[c.OFFSET_PCT_Y_KEY] = offset_pct_y
        
        params[c.PERSON_IMAGES_NR_KEY] = 13
        
        params[c.SOFTWARE_TEST_FILE_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\SoftwareTestingFiles\Arnold.jpg' # Portatile MP
        #params[c.SOFTWARE_TEST_FILE_PATH_KEY] = r'C:\Active\Mercurial\test\Test files\Face detection\SoftwareTestingFiles\Test.jpg' # Palladium
        
        params[c.TRAINING_IMAGES_NR_KEY] = 12
        
        params[c.USE_EYE_DETECTION_KEY] = True
        
        params[c.USE_EYE_DETECTION_IN_TRAINING_KEY] = True
        
        params[c.USE_EYES_POSITION_KEY] = True
        
        params[c.USE_EYES_POSITION_IN_TRAINING_KEY] = True
        
        params[c.USE_FACE_DETECTION_IN_TRAINING_KEY] = True
        
        params[c.USE_ONE_FILE_FOR_FACE_MODELS_KEY] = True
        
        params[c.USE_RESIZING_KEY] = True
        
        fr_experiments(params, False)
        
        ## Save yaml file with parameters
        #yaml_file_path = r'C:\Users\Maurizio\Documents\Parametri\Face detection\face_detection.yml'
        
        #save_YAML_file(yaml_file_path, params)
        
    counter = counter + 1
    
    
