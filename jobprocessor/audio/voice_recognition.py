import os
import math
import numpy as np
import sys
from collections import Counter
from Constants import *


def recognize_voice_from_model_files(voice, voice_models, params, show_results):
    '''Recognize given voice using the voice recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''

    fm = face_models
    if(face_models == None):
        fm = FaceModelsLBP()

    start_time = cv2.getTickCount()
    
    label = -1
    
    confidence = -1
    
    #train_histograms = fm.model.getMatVector("histograms")
    
    #train_labels = fm.model.getMat("labels")
           
    query_model = cv2.createLBPHFaceRecognizer(
    LBP_RADIUS, LBP_NEIGHBORS, 
    LBP_GRID_X, LBP_GRID_Y)
        
    query_model.train(
    np.asarray([np.asarray(face, dtype=np.uint8)]), np.asarray(0))
    
    query_histograms = query_model.getMatVector("histograms")
    
    query_hist = query_histograms[0][0]
    
    diff_list = []
    
    #for i in range(0,len(train_histograms)):
        
    train_labels = []
        
    for model_file in os.listdir(DB_MODELS_PATH):
        
        model_file_path = os.path.join(DB_MODELS_PATH, model_file)
        
        ok = fm.load_model(model_file_path)
        
        if(ok):
        
            model_histograms = fm.model.getMatVector("histograms")
            
            model_labels = fm.model.getMat("labels")
            
            for i in range(0,len(model_histograms)):
            
                train_hist = model_histograms[i][0]
                
                diff = 0
                
                if(USE_WEIGHTED_REGIONS):
                    
                    diff = calculate_w_reg_distance(query_hist, train_hist)
                    
                elif(USE_NBNN):
                    
                    people_nr = fm.get_people_nr()
                    
                    #diff = calculate_NBNN_distance()
                    print "No implemented yet!"
                
                else:
            
                    diff = cv2.compareHist(
                    query_hist, train_hist, cv.CV_COMP_CHISQR)  
                    
                diff_list.append(diff)
                
            train_labels.extend(model_labels)  
        
    # Get K nearest histograms
    
    idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]
    
    K = KNN_NEIGHBORS
    
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
    
    tag = fm.get_tag(label)
    
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency()

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {} 
    result[ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds
    result[ERROR_KEY] = ''
    result[ASSIGNED_LABEL_KEY] = label
    result[ASSIGNED_TAG_KEY] = tag
    result[CONFIDENCE_KEY] = confidence

    return result

def recognize_voice_from_models_file(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''
    
    fm = face_models
    if(face_models == None):
        
        fm = FaceModelsLBP()

    start_time = cv2.getTickCount()
    
    label = -1
    
    confidence = -1
    
    train_histograms = fm.model.getMatVector("histograms")
    
    train_labels = fm.model.getMat("labels")
    
    w, h = face.shape
           
    query_model = cv2.createLBPHFaceRecognizer(
    LBP_RADIUS, LBP_NEIGHBORS, 
    LBP_GRID_X, LBP_GRID_Y)
        
    query_model.train(
    np.asarray([np.asarray(face, dtype=np.uint8)]), np.asarray(0))
    
    query_histograms = query_model.getMatVector("histograms")
    
    query_hist = query_histograms[0][0]
    
    if(USE_NBNN):
        
        people_nr = fm.get_people_nr()
                
        [label, confidence] = recognize_with_NBNN_distance(
        query_hist, train_histograms, train_labels, w, h, people_nr)
        
    else:
        
        diff_list = []
    
        for i in range(0,len(train_histograms)):
            
            train_hist = train_histograms[i][0]
            
            diff = 0
            
            if(USE_WEIGHTED_REGIONS):
                
                diff = calculate_w_reg_distance(query_hist, train_hist)
                                
            else:
        
                diff = cv2.compareHist(
                query_hist, train_hist, cv.CV_COMP_CHISQR)  
                
            diff_list.append(diff)  
            
        # Get K nearest histograms
        
        idxs = [i[0] for i in sorted(enumerate(diff_list), key=lambda x:x[1])]
        
        K = KNN_NEIGHBORS
        
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
                
                label = train_labels[idx][0]
                
                if(USE_WEIGHTED_KNN):
                
                    weight = 0
                    
                    if(diff < 1):
                        
                        weight = 100
                        
                    elif(diff > 100):
                        
                        weight = 1
                        
                    else:
                        
                        weight = int(round(100 / diff))
                    
                    for t in range(0, weight):
                    
                        nearest_labels_list.append(label)
                        
                else:
                    
                    nearest_labels_list.append(label)
                    
                #print 'tag = %s diff =%.2f' % (tag, diff)
                
            # Find most common label in K nearest ones
            data = Counter(nearest_labels_list)
            
            label = data.most_common(1)[0][0]
            
            counter = data.most_common(1)[0][1]
            
            confidence = counter
        
    tag = fm.get_tag(label)
    
    print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency()

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {} 
    result[ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds
    result[ERROR_KEY] = ''
    result[ASSIGNED_LABEL_KEY] = label
    result[ASSIGNED_TAG_KEY] = tag
    result[CONFIDENCE_KEY] = confidence

    if(show_results):
        cv2.imshow(str(label), face)
        cv2.waitKey(0) 

    return result


    
def recognize_voice(voice, voice_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''
    
    result = None
    
    if(USE_ONE_FILE_FOR_FACE_MODELS):
        
        #result = recognize_face_from_models_file(
        #face, face_models, params, show_results)
        result = recognize_face_old(
        face, face_models, params, show_results)
        
    else:
        
        result = recognize_face_from_model_files(
        face, face_models, params, show_results)

    return result
