import os
import cv2
import cv2.cv as cv
import math
import numpy as np
from collections import Counter
from Constants import *
from FaceModelsLBP import FaceModelsLBP

USE_WEIGHTED_REGIONS = True

USE_NBNN = False

CALCULATE_K_FROM_FEATURES = False

USE_WEIGHTED_KNN = False

# Weights for 7 x 7 grid

WEIGHT_0_REGIONS = [17, 21, 24, 27, 28, 34, 35, 41, 42, 48]

WEIGHT_2_REGIONS = [0, 6, 7, 13]

WEIGHT_4_REGIONS = [8, 9, 11, 12]

ALFA = 1

def calculate_w_reg_distance(query_hist, train_hist):
    
    nr_regions = FACE_RECOGNITION_GRID_X * FACE_RECOGNITION_GRID_Y
    
    len_reg_hist = 2**FACE_RECOGNITION_NEIGHBORS
    
    diff = 0
    
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
        
    return diff

def calculate_NBNN_distance(
query_hist, train_histograms, train_labels, im_w, im_h, people_nr):
    
    nr_regions = FACE_RECOGNITION_GRID_X * FACE_RECOGNITION_GRID_Y
    
    len_reg_hist = 2**FACE_RECOGNITION_NEIGHBORS
    
    reg_w = float(im_w) / FACE_RECOGNITION_GRID_X
    reg_h = float(im_h) / FACE_RECOGNITION_GRID_Y
    
    for r in range(0, nr_regions):
        
        #print('len query hist', len(query_hist))
        
        # Calculate region position for query image

        reg_x_counter = r % FACE_RECOGNITION_GRID_X
        
        reg_y_counter = r / FACE_RECOGNITION_GRID_Y
        
        q_x = reg_x_counter * reg_w / im_w
        
        q_y = reg_y_counter * reg_h / im_h
        
        first_idx = r * len_reg_hist
        
        last_idx = (r + 1) * len_reg_hist
        
        query_reg_hist = query_hist[first_idx:last_idx]
        
        for p in range(0,people_nr):
            
            # Consider all images of training subject p

            for t in range(0, len(train_labels)):
                
                if(train_labels[t] == p):
                    
                    t_hist = train_histograms[t][0]
                    
                    for r2 in range(0, nr_regions):
                        
                        fi = r2 * len_reg_hist
        
                        li = (r2 + 1) * len_reg_hist
                        
                        t_reg_hist = t_hist[fi:li]
                        
                        hist_diff = cv2.compareHist(
                        query_reg_hist, t_reg_hist, cv.CV_COMP_CHISQR)
                        
                        # Calculate region position for train image
                        
                        reg_x_counter = r2 % FACE_RECOGNITION_GRID_X
                        
                        reg_y_counter = r2 / FACE_RECOGNITION_GRID_Y
                        
                        t_x = reg_x_counter * reg_w / im_w
                        
                        t_y = reg_y_counter * reg_h / im_h
                        
                        pos_diff_x = math.pow(q_x - t_x, 2)
                        pos_diff_y = math.pow(q_y - t_y, 2)
                        pos_diff = ALFA * (pos_diff_x + pos_diff_y)
                        
                        reg_diff = hist_diff + pos_diff
                        
                        print ('hist_diff', hist_diff)
                        print ('pos_diff', pos_diff)
                        
                        cv2.waitKey(0)

def recognize_face_from_model_files(face, face_models, params, show_results):
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
    
    #train_histograms = fm.model.getMatVector("histograms")
    
    #train_labels = fm.model.getMat("labels")
           
    query_model = cv2.createLBPHFaceRecognizer(
    FACE_RECOGNITION_RADIUS, FACE_RECOGNITION_NEIGHBORS, 
    FACE_RECOGNITION_GRID_X, FACE_RECOGNITION_GRID_Y)
        
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
    
    print('result', result)

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return result;

def recognize_face_from_models_file(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''

    cv2.imshow('face', face)

    K = 1

    fm = face_models;
    if(face_models == None):
        fm = FaceModelsLBP();

    start_time = cv2.getTickCount();
    
    label = -1
    
    confidence = -1
    
    train_histograms = fm.model.getMatVector("histograms")
    
    train_labels = fm.model.getMat("labels")
    
    w, h = face.shape
           
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
            
            diff = calculate_w_reg_distance(query_hist, train_hist)
                            
        elif(USE_NBNN):
            
            people_nr = fm.get_people_nr()
            
            diff = calculate_NBNN_distance(
            query_hist, train_histograms, train_labels, w, h, people_nr)
        
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
    
def recognize_face(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''
    
    result = None
    
    if(USE_ONE_FILE_FOR_FACE_MODELS):
        
        result = recognize_face_from_models_file(
        face, face_models, params, show_results)
        
    else:
        
        result = recognize_face_from_model_files(
        face, face_models, params, show_results)

    return result
