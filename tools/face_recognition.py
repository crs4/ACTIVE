import os
import cv2
import cv2.cv as cv
import math
import numpy as np
from collections import Counter
from Constants import *
from FaceModelsLBP import FaceModelsLBP

CALCULATE_K_FROM_FEATURES = False

USE_WEIGHTED_KNN = True

USE_WEIGHTED_REGIONS = True

# Weights for 7 x 7 grid

WEIGHT_0_REGIONS = [17, 21, 24, 27, 28, 34, 35, 41, 42, 48]

WEIGHT_2_REGIONS = [0, 6, 7, 13]

WEIGHT_4_REGIONS = [8, 9, 11, 12]

def recognize_face(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''

    K = 1

    fm = face_models;
    if(face_models == None):
        fm = FaceModelsLBP();

    start_time = cv2.getTickCount();
    
    label = -1
    
    confidence = -1
    
    if((K == 1) and not(USE_WEIGHTED_REGIONS)):
        
        [label, confidence] = fm.model.predict(np.asarray(face, dtype=np.uint8));
   
    else:
    
        train_histograms = fm.model.getMatVector("histograms")
        
        train_labels = fm.model.getMat("labels")
               
        query_model = cv2.createLBPHFaceRecognizer(
        FACE_RECOGNITION_RADIUS, FACE_RECOGNITION_NEIGHBORS, 
        FACE_RECOGNITION_GRID_X, FACE_RECOGNITION_GRID_Y)
            
        query_model.train(
        np.asarray([np.asarray(face, dtype=np.uint8)]), np.asarray(0))
        
        query_histograms = query_model.getMatVector("histograms")
        
        query_hist = query_histograms[0][0]
        
        diff_list = []
        
        for i in range(0,len(train_histograms)):
            
            train_hist = train_histograms[i][0]
            
            diff = 0
            
            if(USE_WEIGHTED_REGIONS):
                
                nr_regions = FACE_RECOGNITION_GRID_X * FACE_RECOGNITION_GRID_Y
                
                len_reg_hist = 2**FACE_RECOGNITION_NEIGHBORS
                
                for r in range(0, nr_regions):
                    
                    #print('len query hist', len(query_hist))
                    
                    first_idx = r * len_reg_hist
                    
                    last_idx = (r + 1) * len_reg_hist
                    
                    query_reg_hist = query_hist[first_idx:last_idx]
                    
                    #print('len query reg list', len(query_reg_hist))
                    
                    train_reg_hist = train_hist[first_idx:last_idx]
                    
                    #print('len train reg list', len(train_reg_hist))
                    
                    reg_diff = 0
                    
                    if(r in WEIGHT_0_REGIONS):
                        
                        pass
                        
                    elif(r in WEIGHT_2_REGIONS):
                        
                        reg_diff = 2 * cv2.compareHist(
                        query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
                        
                    elif(r in WEIGHT_4_REGIONS):
                        
                        reg_diff = 4 * cv2.compareHist(
                        query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
                        
                    else:
                        
                        reg_diff = cv2.compareHist(
                        query_reg_hist, train_reg_hist, cv.CV_COMP_CHISQR)
                        
                    diff = diff + reg_diff
                
            else:
        
                diff = cv2.compareHist(
                query_hist, train_hist, cv.CV_COMP_CHISQR)  
                
            diff_list.append(diff)  
            
        # Get K nearest histograms
        
        idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]
        
        if(CALCULATE_K_FROM_FEATURES):
            
            nr_features = 2**FACE_RECOGNITION_NEIGHBORS * FACE_RECOGNITION_GRID_X * FACE_RECOGNITION_GRID_Y
            
            K = int(round(math.sqrt(nr_features)))
        
        if(K == 1):
            
            idx = idxs[0]
            
            confidence = diff_list[idx]
            
            label = train_labels[idx][0]
            
        else:
            
            nearest_labels_list = []
            
            # K cannot be greater than number of training items
            if(K > len(idxs)):
                
                K = len(idxs)
            
            for i in range(0, K):
                
                idx = idxs[i]
                
                diff = diff_list[idx]
                
                weight = 0
                
                if(diff < 1):
                    
                    weight = 100
                    
                elif(diff > 100):
                    
                    weight = 1
                    
                else:
                    
                    weight = int(round(100 / diff))
                
                label = train_labels[idx][0]
                
                for t in range(0, weight):
                
                    nearest_labels_list.append(label)
                
                #print 'tag = %s diff =%.2f' % (tag, diff)
                
            # Find most common label in K nearest ones
            data = Counter(nearest_labels_list)
            
            label = data.most_common(1)[0][0]
            
            counter = data.most_common(1)[0][1]
            
            confidence = counter
        
    tag = fm.get_label(label);
    
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time;
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency();

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {}; 
    result[FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds;
    result[FACE_RECOGNITION_ERROR_KEY] = '';
    result[PERSON_ASSIGNED_LABEL_KEY] = label;
    result[PERSON_ASSIGNED_TAG_KEY] = tag;
    result[PERSON_CONFIDENCE_KEY] = confidence;

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return result;
    
def recognize_face_old(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''

    fm = face_models;
    if(face_models == None):
        fm = FaceModelsLBP();

    start_time = cv2.getTickCount();
    
    [label, confidence] = fm.model.predict(np.asarray(face, dtype=np.uint8));

    tag = fm.get_label(label);
    
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time;
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency();

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {}; 
    result[FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds;
    result[FACE_RECOGNITION_ERROR_KEY] = '';
    result[PERSON_ASSIGNED_LABEL_KEY] = label;
    result[PERSON_ASSIGNED_TAG_KEY] = tag;
    result[PERSON_CONFIDENCE_KEY] = confidence;

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return result;
