import cv2
import numpy as np
import os
from caption_recognition import get_tag_from_image
from constants import *
from face_detection import get_detected_cropped_face
from Utils import load_YAML_file, save_model_file, save_YAML_file

ASSIGNED_LABEL_KEY = 'assigned_label'

def analyze_image(image_path): 
#def analyze_image(image_path, image_counter):    # TEST ONLY
    face = None
    
    label = -1
    
    tag = -1
    
    # Face detection
    face = get_detected_cropped_face(image_path, False)
    
    if(face is not None):
        
        image = cv2.imread(image_path)
            
        cap_rec_res = get_tag_from_image(image_path)
        
        label = cap_rec_res[ASSIGNED_LABEL_KEY]
        
        tag = cap_rec_res[ASSIGNED_TAG_KEY]           

    return [label, tag, face]
    
    

def train_by_images(path, db_file_name):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    model = None
    
    X, y = [], []
    tags = {}
    
    image_counter = 0
     
    for image in os.listdir(path):
    
        image_complete_path = path + os.sep + image
        
        print(image)
                
        [label, tag, face] = analyze_image(image_complete_path, image_counter)
        
        if(label != -1):
            
            X.append(np.asarray(face, dtype = np.uint8))
            y.append(label)
            tags[label] = tag
            
            image_counter = image_counter + 1
    
    # Save file with face models
    
    if(USE_ONE_FILE_FOR_FACE_MODELS):
            
        model=cv2.createLBPHFaceRecognizer(
        LBP_RADIUS, 
        LBP_NEIGHBORS, 
        LBP_GRID_X, 
        LBP_GRID_Y)
        model.train(np.asarray(X), np.asarray(y))
        model.save(db_file_name)
        
    else:
        
        y_set = set(y)
            
        for label in y_set:
            
            person_X = []
            person_y = []
            
            for i in range(0, len(y)):
                
                if(y[i] == label):
                    
                    person_X.append(X[i])
                    person_y.append(label)
                       
        save_model_file(person_X, person_y, db_file_name)
    
    # Save labels in YAML file
    save_YAML_file(db_file_name + "-Tags", tags)     
        
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Creation time: ' + str(time_in_s) + ' s\n');
    
    return [model, tags]

def train_by_captions(video_path, db_file_name):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    model = None
    
    error = None
    
    tags = {}
     
    capture = cv2.VideoCapture(video_path)
    
    print(video_path)
    
    # Counter for all frames
    frame_counter = 0
    
    # Counter for analyzed frames
    anal_frame_counter = 0
    
    # Value of frame_counter for last analyzed frame
    last_anal_frame = 0
    
    if capture is None or not capture.isOpened():
        
        error = 'Error in opening video file'
        
        print error
        
    else:
        
        video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
        
        tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)        
        
        X, y = [], [] 
        
        while True:
            
            ret, frame = capture.read()
            
            if(not(ret)):
                
                break;
            
            # Next frame to be analyzed
            next_frame = last_anal_frame + (video_fps/USED_FPS_IN_TRAINING)
            if(USE_ORIGINAL_FPS_IN_TRAINING or (frame_counter > next_frame)):
                
                # Frame position in video in seconds
                elapsed_video_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                elapsed_video_s = elapsed_video_ms / 1000
                
                progress = 100 * (frame_counter / tot_frames)
                
                print('progress: ' + str(progress) + '%')
                
                cv2.imwrite(TMP_FRAME_FILE_PATH, frame)
                
                [label, tag, face] = analyze_image(TMP_FRAME_FILE_PATH)
                
                if(label != -1):
            
                    print('label', label)
                    print('tag', tag)
                    
                    X.append(np.asarray(face, dtype = np.uint8))
                    y.append(label)
                    tags[label] = tag
                            
                anal_frame_counter = anal_frame_counter + 1
                
                last_anal_frame = frame_counter
            
            frame_counter = frame_counter + 1
            
            # Save file with face models
    
        if(USE_ONE_FILE_FOR_FACE_MODELS):
                
            model=cv2.createLBPHFaceRecognizer(
            LBP_RADIUS, 
            LBP_NEIGHBORS, 
            LBP_GRID_X, 
            LBP_GRID_Y)
            model.train(np.asarray(X), np.asarray(y))
            model.save(db_file_name)
            
        else:
            
            y_set = set(y)
            
            for label in y_set:
                
                person_X = []
                person_y = []
                
                for i in range(0, len(y)):
                    
                    if(y[i] == label):
                        
                        person_X.append(X[i])
                        person_y.append(label)
                        
                save_model_file(person_X, person_y, db_file_name)
        
        # Save labels in YAML file
        save_YAML_file(db_file_name + "-Tags", tags)                      
    
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Creation time: ' + str(time_in_s) + ' s\n');
    
    return [model, tags]
