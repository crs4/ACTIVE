from fr_test import fr_experiments
import sys
sys.path.append("../../..")
from tools.Constants import *


for power in range(0,5):
    
    images_height = 112
    images_width = 92
    scale_factor = pow(2,power)
    cropped_face_height = int(round(images_height / scale_factor))
    cropped_face_width = int(round(images_width / scale_factor))
    print('scale_factor', scale_factor) 
    print('cropped_face_height', cropped_face_height)
    print('cropped_face_width', cropped_face_width)
        
    for training_images_nr in range(1,10):
    
        params = {}
        
        params[ALIGNED_FACES_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\tools\Aligned faces'
        
        params[DATASET_ALREADY_DIVIDED_KEY] = False
        
        params[DATASET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Dataset AT&T'
        
        params[DB_NAME_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T\Face Models\ATT-8-' + str(cropped_face_width) + '-' + str(cropped_face_height) + '-' + str(training_images_nr)
        
        params[FACE_MODEL_ALGORITHM_KEY] = 'LBP'
        
        params[FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T'
    
        params[LBP_GRID_X_KEY] = 4
        
        params[LBP_GRID_Y_KEY] = 4
    
        params[LBP_NEIGHBORS_KEY] = 8
        
        params[LBP_RADIUS_KEY] = 1
        
        params[OFFSET_PCT_X_KEY] = 0.20
        
        params[OFFSET_PCT_Y_KEY] = 0.20
        
        params[PERSON_IMAGES_NR_KEY] = 10
        
        params[TRAINING_IMAGES_NR_KEY] = training_images_nr
        
        params[USE_CAPTIONS_KEY] = False
        
        params[USE_EYE_DETECTION_KEY] = False
        
        params[USE_EYE_DETECTION_IN_TRAINING_KEY] = False
        
        params[USE_EYES_POSITION_KEY] = False
        
        params[USE_EYES_POSITION_IN_TRAINING_KEY] = False
        
        params[USE_FACE_DETECTION_IN_TRAINING_KEY] = False
        
        params[USE_ONE_FILE_FOR_FACE_MODELS_KEY] = True
        
        params[USE_RESIZING_KEY] = True
        
        params[CROPPED_FACE_HEIGHT_KEY] = cropped_face_height
        
        params[CROPPED_FACE_WIDTH_KEY] = cropped_face_width
        
        fr_experiments(params, False)


#algorithms = ['Eigenfaces', 'Fisherfaces', 'LBP']

#for lbp_grid in range(2,9,2):

    #for radius in range(1,3):
        
        #for training_images_nr in range(1,10):
        
            #params = {}
            
            #params[ALIGNED_FACES_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\tools\Aligned faces'
            
            #params[DATASET_ALREADY_DIVIDED_KEY] = False
            
            #params[DATASET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Dataset AT&T'
            
            #params[DB_NAME_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T\Face Models\ATT-8-' + str(lbp_grid) + '-' + str(radius) + '-' + str(training_images_nr)
            
            #params[FACE_MODEL_ALGORITHM_KEY] = 'LBP'
            
            #params[FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T'
        
            #params[LBP_GRID_X_KEY] = lbp_grid
            
            #params[LBP_GRID_Y_KEY] = lbp_grid
        
            #params[LBP_NEIGHBORS_KEY] = 8
            
            #params[LBP_RADIUS_KEY] = radius
            
            #params[OFFSET_PCT_X_KEY] = 0.20
            
            #params[OFFSET_PCT_Y_KEY] = 0.20
            
            #params[PERSON_IMAGES_NR_KEY] = 10
            
            #params[TRAINING_IMAGES_NR_KEY] = training_images_nr
            
            #params[USE_CAPTIONS_KEY] = False
            
            #params[USE_EYE_DETECTION_KEY] = False
            
            #params[USE_EYE_DETECTION_IN_TRAINING_KEY] = False
            
            #params[USE_EYES_POSITION_KEY] = False
            
            #params[USE_EYES_POSITION_IN_TRAINING_KEY] = False
            
            #params[USE_FACE_DETECTION_IN_TRAINING_KEY] = False
            
            #params[USE_ONE_FILE_FOR_FACE_MODELS_KEY] = True
            
            #params[USE_RESIZING_KEY] = False
            
            #fr_experiments(params, False)

#for lbp_grid in range(2,7,2):

    #for radius in range(1,3):
        
        #for training_images_nr in range(1,10):
        
            #params = {}
            
            #params[ALIGNED_FACES_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\tools\Aligned faces'
            
            #params[DATASET_ALREADY_DIVIDED_KEY] = False
            
            #params[DATASET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Dataset AT&T'
            
            #params[DB_NAME_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T\Face Models\ATT-12-' + str(lbp_grid) + '-' + str(radius) + '-' + str(training_images_nr)
            
            #params[FACE_MODEL_ALGORITHM_KEY] = 'LBP'
            
            #params[FACE_RECOGNITION_RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\AT&T'
        
            #params[LBP_GRID_X_KEY] = lbp_grid
            
            #params[LBP_GRID_Y_KEY] = lbp_grid
        
            #params[LBP_NEIGHBORS_KEY] = 12
            
            #params[LBP_RADIUS_KEY] = radius
            
            #params[OFFSET_PCT_X_KEY] = 0.20
            
            #params[OFFSET_PCT_Y_KEY] = 0.20
            
            #params[PERSON_IMAGES_NR_KEY] = 10
            
            #params[TRAINING_IMAGES_NR_KEY] = training_images_nr
            
            #params[USE_CAPTIONS_KEY] = False
            
            #params[USE_EYE_DETECTION_KEY] = False
            
            #params[USE_EYE_DETECTION_IN_TRAINING_KEY] = False
            
            #params[USE_EYES_POSITION_KEY] = False
            
            #params[USE_EYES_POSITION_IN_TRAINING_KEY] = False
            
            #params[USE_FACE_DETECTION_IN_TRAINING_KEY] = False
            
            #params[USE_ONE_FILE_FOR_FACE_MODELS_KEY] = True
            
            #params[USE_RESIZING_KEY] = False
            
            #fr_experiments(params, False)

    
