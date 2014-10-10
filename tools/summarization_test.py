import cv2
import cv2.cv as cv
import numpy as np
import os
import shutil
from Constants import *
from face_detection import detect_faces_in_image

def calculate_threshold(path):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    prev_hists = None
    
    diff_list = []
    
    for im_file in os.listdir(path):
        
        #print(im_file)
        
        im_path = path + os.sep + im_file
        
        im_bgr = cv2.imread(im_path, cv2.CV_LOAD_IMAGE_COLOR)
        
        im_hsv = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HSV)
        
        tot_diff = 0
        hists = []
        for ch in range(0,3):
            hist = cv2.calcHist([im_hsv],[ch],None,[256],[0,256])
            #cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
            hists.append(hist)
            if(prev_hists is not None):
                # Skip first image 
                diff = cv2.compareHist(
                prev_hists[ch], hist, cv.CV_COMP_CHISQR)
                tot_diff = tot_diff + abs(diff)
        
        if(prev_hists is not None):
            # Not for first frame
            diff_list.append(tot_diff)
        
        prev_hists = hists
        
    # Discard 10 % of values
    sorted_diff_list = sorted(diff_list)
    
    last_idx = int(len(sorted_diff_list)*9.0/10.0)
    
    red_diff_list = sorted_diff_list[0:last_idx]
                
    mean = np.mean(red_diff_list)
    std = np.std(red_diff_list)
    
    return [mean, std]
    
def divide_images_in_shots(path, save_path = None):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    prev_hists = None
    
    diff_list = []
    
    for im_file in os.listdir(path):
        
        print(im_file)
        
        im_path = path + os.sep + im_file
        
        im_bgr = cv2.imread(im_path, cv2.CV_LOAD_IMAGE_COLOR)
        
        im_hsv = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HSV)
        
        tot_diff = 0
        hists = []
        for ch in range(0,3):
            hist = cv2.calcHist([im_hsv],[ch],None,[256],[0,256])
            #cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
            hists.append(hist)
            if(prev_hists is not None):
                # Skip first image 
                diff = cv2.compareHist(
                prev_hists[ch], hist, cv.CV_COMP_CHISQR)
                tot_diff = tot_diff + abs(diff)
             
        # First frame
        if(prev_hists is None):
            prev_hists = hists

        if(tot_diff > HSV_HIST_DIFF_THRESHOLD):
            
            cv2.imshow(im_file, im_bgr)
            cv2.waitKey(0)
            prev_hists = hists
        
def divide_video_in_shots(path, save_path = None):

    # Save processing time
    start_time = cv2.getTickCount()
    
    prev_hists = None
    
    if(save_path is None):
        save_path = SAVE_PATH_ALL_KEY_FRAMES

    capture = cv2.VideoCapture(path)
    
    # Counter for all frames
    frame_counter = 1
    
    # Counter for analyzed frames
    anal_frame_counter = 1
    
    # Value of frame_counter for last analyzed frame
    last_anal_frame = 1
    
    key_frame_list = []
    hist_list = []
    
    if capture is None or not capture.isOpened():
        
        error = 'Error in opening video file'
        
        print error
        
    else:
        
        video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
        
        tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        
        while True:
            
            ret, frame = capture.read()
            
            if(not(ret)):
                
                break
                
            # Next frame to be analyzed
            next_frame = last_anal_frame + (video_fps/USED_FPS_IN_TRAINING)
            if(USE_ORIGINAL_FPS_IN_SHOT_DETECTIN or (frame_counter > next_frame)):
                
                # Frame position in video in seconds
                elapsed_video_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                elapsed_video_s = elapsed_video_ms / 1000
                
                progress = 100 * (frame_counter / tot_frames)
                
                print('progress: ' + str(progress) + '%')
                
                im_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                tot_diff = 0
                hists = []
                for ch in range(0,3):
                    hist = cv2.calcHist([im_hsv],[ch],None,[256],[0,256])
                    #cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
                    hists.append(hist)
                    if(prev_hists is not None):
                        # Skip first image 
                        diff = cv2.compareHist(
                        prev_hists[ch], hist, cv.CV_COMP_CHISQR)
                        tot_diff = tot_diff + abs(diff)
                
                # If this is the first frame or if difference
                # is greater than threshold    
                if((prev_hists is None) or (tot_diff > HSV_HIST_DIFF_THRESHOLD)):
                    print('diff', tot_diff)
                    # Save frame
                    frame_path = save_path + os.sep + str(frame_counter) + '.bmp'
                    cv2.imwrite(frame_path, frame)
                    
                    key_frame_list.append(frame_path)
                    hist_list.append(hists)    
                        
                    prev_hists = hists
  
                anal_frame_counter = anal_frame_counter + 1
                
                last_anal_frame = frame_counter
            
            frame_counter = frame_counter + 1
            
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Processing time (divide video in shots): ' + str(time_in_s) + ' s\n')
    
    return [key_frame_list, hist_list]
          
def group_shots(im_list, hist_list, save_path = None):
    
    # Save processing time
    start_time = cv2.getTickCount()
        
    if(save_path is None):
        save_path = SAVE_PATH_KEY_FRAMES
        
    chosen_im_hist_list = []
    
    im_counter = 0  
        
    for im_path in im_list:
        
        im_hists = hist_list[im_counter]
        
        min_diff = HSV_HIST_DIFF_THRESHOLD
        
        for hists in chosen_im_hist_list:
            
            tot_diff = 0
            for ch in range(0,3):
                
                diff = cv2.compareHist(
                hists[ch], im_hists[ch], cv.CV_COMP_CHISQR)
                tot_diff = tot_diff + abs(diff)
             
            if(tot_diff < min_diff):
                min_diff = tot_diff
                break
        
        # If no similare image was found, 
        # consider image as key frame  
        if(min_diff == HSV_HIST_DIFF_THRESHOLD):
            
            [path, im_name] = os.path.split(im_path)
            
            new_im_path = os.path.join(save_path, im_name)
            
            im = cv2.imread(im_path, cv2.IMREAD_COLOR)
            cv2.imwrite(new_im_path, im)
            
            chosen_im_hist_list.append(im_hists)
        
        im_counter = im_counter + 1
        
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Processing time (group shots): ' + str(time_in_s) + ' s\n')
            
def get_all_faces_from_images(path = None, params = None, save_path = None):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    model = None
    
    if(path is None):
        path = SAVE_PATH_KEY_FRAMES
        
    if(save_path is None):
        save_path = SAVE_PATH_ALL_FACES
    
    X, y = [], []
    tags = {}
    
    frame_counter = 1
    
    all_faces = []
     
    for image in os.listdir(path):
    
        image_path = path + os.sep + image

        # Face detection
        det_params = None
        rec_params = None
        if params is not None:
            
            det_params = params[FACE_DETECTION_KEY]
            rec_params = params[FACE_RECOGNITION_KEY]

        detection_result = detect_faces_in_image(image_path, det_params, False)

        detection_error = detection_result[ERROR_KEY]
        
        if(not(detection_error)):
            
            face_bboxes = detection_result[FACES_KEY]
            face_images = detection_result[FACE_IMAGES_KEY]
            
            image_counter = 1
            
            for face in face_images:

                #TEST ONLY
                
                if(save_path is not None):
                    face_path = save_path + os.sep + str(frame_counter) + '-' + str(image_counter) + '.bmp'
                    cv2.imwrite(face_path, face)
                    
                X = [np.asarray(face, dtype = np.uint8)]
                y = [0]
        
                model=cv2.createLBPHFaceRecognizer(
                LBP_RADIUS, 
                LBP_NEIGHBORS, 
                LBP_GRID_X, 
                LBP_GRID_Y)
                model.train(np.asarray(X), np.asarray(y))
                
                face_dict = {}
                face_dict[FACE_KEY] = face
                bbox = face_bboxes[image_counter -1]
                face_dict[BBOX_KEY] = bbox
                face_dict[IMAGE_PATH_KEY] = image_path
                face_dict[FRAME_COUNTER_KEY] = frame_counter
                face_dict[IMAGE_COUNTER_KEY] = image_counter
                face_dict[FACE_MODEL_KEY] = model
                face_dict[CHECKED_KEY] = False
                
                all_faces.append(face_dict)
                
                image_counter = image_counter + 1
            
        frame_counter = frame_counter + 1
        
        #if(frame_counter > 200):
            
        #    break    
            
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Processing time (get all faces from images): ' + str(time_in_s) + ' s\n')
    
    return all_faces
    
def group_faces(all_faces, save_path = None):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    if(save_path is None):
        save_path = SAVE_PATH_FACE_GROUPS
    
    group_counter = 1
    
    for face_dict in all_faces:
        
        checked = face_dict[CHECKED_KEY]
        
        if(not checked):
            
            face_dict[CHECKED_KEY] = True
                    
            frame_counter = face_dict[FRAME_COUNTER_KEY]
        
            image_counter = face_dict[IMAGE_COUNTER_KEY]
        
            ref_model = face_dict[FACE_MODEL_KEY]
            
            ref_hists = ref_model.getMatVector("histograms")
    
            ref_hist = ref_hists[0][0]
            
            group_path = None
            if(save_path is not None):
                group_path = save_path + os.sep + str(group_counter)
                os.makedirs(group_path)
                face_path = group_path + os.sep + str(frame_counter) + '-' + str(image_counter) + '.bmp'
                #face = face_dict [FACE_KEY]
                #cv2.imwrite(face_path, face)
                
                im_path = face_dict [IMAGE_PATH_KEY]
                bbox = face_dict[BBOX_KEY]
                x = bbox[0]
                y = bbox[1]
                w = bbox[2]
                h = bbox[3]
                im = cv2.imread(im_path, cv2.IMREAD_COLOR)
                cv2.rectangle(im, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0)
                cv2.imwrite(face_path, im)
        
            for face_dict2 in all_faces:
                
                checked = face_dict2[CHECKED_KEY]
                
                if(not checked):
                            
                    frame_counter = face_dict2[FRAME_COUNTER_KEY]
                
                    image_counter = face_dict2[IMAGE_COUNTER_KEY]             
        
                    model = face_dict2[FACE_MODEL_KEY]
                    
                    hists = model.getMatVector("histograms")
                    
                    hist = hists[0][0]
                    
                    diff = cv2.compareHist(
                    ref_hist, hist, cv.CV_COMP_CHISQR) 
                    
                    if(diff < LBP_HIST_DIFF_THRESHOLD):
                        
                        face_dict2[CHECKED_KEY] = True
                        
                        if(group_path is not None):
                        
                            face_path = group_path + os.sep + str(frame_counter) + '-' + str(image_counter) + '-diff-' + str(diff) + '.bmp'
                            #face = face_dict2[FACE_KEY]
                            #cv2.imwrite(face_path, face)
                            im_path = face_dict2[IMAGE_PATH_KEY]
                            bbox = face_dict2[BBOX_KEY]
                            x = bbox[0]
                            y = bbox[1]
                            w = bbox[2]
                            h = bbox[3]
                            im = cv2.imread(im_path, cv2.IMREAD_COLOR)
                            cv2.rectangle(im, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0)
                            cv2.imwrite(face_path, im)
                    
            group_counter = group_counter + 1
            
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Processing time (group faces): ' + str(time_in_s) + ' s\n')
            
def get_key_faces_from_video(path, save_path = None):
    
    # Save processing time
    start_time = cv2.getTickCount()
    
    [key_frame_list, hist_list] = divide_video_in_shots(TEST_VIDEO_PATH)
    
    group_shots(key_frame_list, hist_list)
    
    all_faces = get_all_faces_from_images()
    
    group_faces(all_faces)
    
    # Calculate processing time in seconds
    time_in_clocks = cv2.getTickCount() - start_time
    time_in_s = time_in_clocks / cv2.getTickFrequency()
    
    print('Processing time (get_key_faces_from_video): ' + str(time_in_s) + ' s\n')

# Delete previous files

path = SAVE_PATH_ALL_KEY_FRAMES
for im in os.listdir(path):
    im_path = os.path.join(path, im)
    os.remove(im_path)

path = SAVE_PATH_KEY_FRAMES
for im in os.listdir(path):
    im_path = os.path.join(path, im)
    os.remove(im_path)
    
path = SAVE_PATH_ALL_FACES
for im in os.listdir(path):
    im_path = os.path.join(path, im)
    os.remove(im_path)
    
path = SAVE_PATH_FACE_GROUPS
for folder in os.listdir(path):
    folder_path = os.path.join(path, folder)
    shutil.rmtree(folder_path)

get_key_faces_from_video(TEST_VIDEO_PATH)
