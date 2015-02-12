import copy

import cv2

import cv2.cv as cv

import face_detection as fd

import yaml

import math

import numpy as np

import os

import pickle as pk

import shutil

import sys

from Constants import *

from Utils import aggregate_frame_results, get_hist_difference, get_shot_changes, is_rect_similar, load_YAML_file, save_YAML_file

class FaceExtractor(object):
    '''
    Tool for detecting and recognizing faces in images and video
    '''
    
    def __init__(self, params = None):
        '''
        Initialize the face extractor
        
        :type  params: dictionary 
        :param params: configuration parameters (see table)        
        '''
        
        self.anal_times = {} # Dictionary with times for analysis
        
        self.cloth_threshold = 0 # Threshold for clothing recognition
        
        self.cut_idxs = [] # List of frame indexes where new shots begin
        
        self.detected_faces = [] # List of detected faces 
        
        # List of tracked faces not considered
        self.disc_tracked_faces = [] 
        
        self.frame_list = [] # List of frame paths
        
        self.fps = 0 # Bitrate of video in frames per second
        
        self.hist_diffs = [] # List with histogram differences
        
        self.nose_pos_list = {} # List with nose positions
        
        self.params = params
        
        self.recognized_faces = [] # List of recognized faces
        
        self.resource_name = None # Name of resource being analyzed
        
        self.saved_frames = 0 # Number of saved and analyzed frames
        
        self.track_threshold = 0 # Threshold for tracking interruption
        
        self.tracked_faces = [] # List of tracked faces
        
        self.video_frames = 0 # Number of original frames in video
       
    
    def analizeVideo(self, resource):
        '''
        Analyze video
        
        :type resource: string
        :param resource: file path of resource
        '''
        
        # Get name of resource
        res_name = os.path.basename(resource) 
        
        self.resource_name = res_name
        
        # Check if a file with parameters of this video exists   
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        file_name = res_name + '_parameters.YAML'
        
        file_path = os.path.join(video_path, file_name)
        
        # Try to load YAML file with video parameters
        if(os.path.exists(file_path)):
            
            print 'Loading YAML file with video parameters'
            
            param_dict = load_YAML_file(file_path)
            
            if(param_dict):
            
                self.fps = param_dict[VIDEO_FPS_KEY]
                
                saved_frames = param_dict[VIDEO_SAVED_FRAMES_KEY]
                
                self.saved_frames = float(saved_frames)
                
                tot_frames = param_dict[VIDEO_TOT_FRAMES_KEY]
                
                self.video_frames = float(tot_frames)
                    
                print 'YAML file with video parameters loaded'
                
        # Check if a file with times for analysis of this video exists 
        file_name = res_name + '_anal_times.YAML'
        
        file_path = os.path.join(video_path, file_name)
        
        # Try to load YAML file with times for analysis
        if(os.path.exists(file_path)):
            
            print 'Loading YAML file with analysis times'
            
            anal_dict = load_YAML_file(file_path)
            
            if(anal_dict):
            
                self.anal_times = anal_dict
                    
                print 'YAML file with analysis times loaded'               
        
        self.getFrameList(resource)
        
        self.detectFacesInVideo()       
        
        self.trackFacesInVideo()
        
        self.saveTrackingSegments() # TEST ONLY
        
        self.saveDiscTrackingSegments() # TEST ONLY
        
        self.recognizeFacesInVideo()

        self.saveRecPeople(True) # TEST ONLY
        
        self.recognizeClothesInVideo()
        
        self.saveRecPeople(False) # TEST ONLY
        
        self.saveTempPeopleFiles()
        
        self.showRecPeople()
        
        self.readUserAnnotations()
        
        self.savePeopleFiles()
        
        
    def detectFacesInVideo(self):
        '''
        Detect faces on analyzed video.
        It works by using list of extracted frames
        '''
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for detection results
        det_path = os.path.join(video_path, FACE_DETECTION_DIR) 
        
        align_path = os.path.join(det_path, ALIGNED_FACES_DIR)        
        
        det_file_path = os.path.join(det_path, file_name)
        
        det_loaded = False
        
        # Try to load YAML file with detection results
        if(os.path.exists(det_file_path)):
            
            print 'Loading YAML file with detection results'
            
            det_faces = load_YAML_file(det_file_path)
            
            if(det_faces):
                
                self.detected_faces = det_faces
                
                print 'YAML file with detection results loaded'
                
                det_loaded = True
                
        if(not(det_loaded)):
        
            # Directory for frame list
            frames_path = os.path.join(video_path, FRAMES_DIR)  
                
            frames_file_path = os.path.join(frames_path, file_name)
            
            # Check existence of frame list
            if(len(self.frame_list) == 0):
                
                # Try to load YAML file with frame list
                if(os.path.exists(frames_file_path)):
                    
                    print 'Loading YAML file with frame list'
                    
                    f_list = load_YAML_file(frames_file_path)
                    
                    if(f_list):
                        
                        self.frame_list = f_list
                        
                        print 'YAML file with frame list loaded'
                        
                    else:
                        
                        print 'Warning! Error in loading file!'
                        
                else:
                    
                    print 'Warning! No frame list found!'
                    
                    return         
            
            print '\n\n### Face detection ###\n'
            
            # Save processing time
            start_time = cv2.getTickCount()
            
            error = None
            
            detection_params = None
            
            if self.params is not None:
                
                detection_params = self.params[FACE_DETECTION_KEY]
            
            if(not(os.path.exists(det_path))):
                
                # Create directory for this video 
                
                os.makedirs(det_path)
                
            if(not(os.path.exists(align_path))):
                    
                # Create directory with aligned faces 
                
                os.makedirs(align_path)
            
            frame_counter = 0
            self.detected_faces = []
            
            # Iterate through frames in frame_list
            for frame_dict in self.frame_list:
                
                self.progress = 100 * (frame_counter / self.saved_frames)
        
                print('progress: ' + str(self.progress) + ' %          \r'),
                
                frame_path = frame_dict[FRAME_PATH_KEY] 
                
                #print('frame_path: ' + os.path.basename(frame_path))
                
                detection_result = fd.detect_faces_in_image(
                frame_path, align_path, detection_params, False)
    
                detection_error = detection_result[ERROR_KEY]
                
                detection_dict = {}
                
                detection_dict[FRAME_PATH_KEY] = frame_path
                
                detection_dict[FRAME_COUNTER_KEY] = frame_counter
                
                elapsed_s = frame_dict[ELAPSED_VIDEO_TIME_KEY]
                detection_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
                
                faces = []
                if(not(detection_error)):
                    
                    det_faces = detection_result[FACES_KEY]
                    
                    for det_face in det_faces:
                        
                        face_dict = {}
                        
                        face_dict[BBOX_KEY] = det_face[BBOX_KEY]
                        
                        if(USE_EYES_POSITION):
                        
                            face_dict[LEFT_EYE_POS_KEY] = (
                            det_face[LEFT_EYE_POS_KEY])
                            
                            face_dict[RIGHT_EYE_POS_KEY] = (
                            det_face[RIGHT_EYE_POS_KEY])
                            
                            face_dict[NOSE_POSITION_KEY] = (
                            det_face[NOSE_POSITION_KEY])
                        
                        faces.append(face_dict)                 
                        
                detection_dict[FACES_KEY] = faces
                    
                self.detected_faces.append(detection_dict)
                
                frame_counter = frame_counter + 1
       
                if(self.video_frames == 0):
                    
                    print 'Warning! Number of frames is zero'
                    
                    break   
            
            # Save detection results in YAML file
            
            save_YAML_file(det_file_path, self.detected_faces)      
            
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            print 'Time for face detection: ', time_in_seconds, 's\n'
            
            self.anal_times[FACE_DETECTION_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
            
            
    def getFrameList(self, resource):
        '''
        Get frames from the video resource.
        '''   
        
        res_name = self.resource_name
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for frame_list
        frames_path = os.path.join(video_path, FRAMES_DIR) 
        
        file_name = res_name + '.YAML'
        
        frames_file_path = os.path.join(frames_path, file_name)
        
        frames_loaded = False
        
        # Try to load YAML file with frame list
        if(os.path.exists(frames_file_path)):
            
            print 'Loading YAML file with frame list'
            
            f_list = load_YAML_file(frames_file_path)
            
            if(f_list):
                
                self.frame_list = f_list
                
                print 'YAML file with frame_list loaded'
                
                frames_loaded = True
                
        if(not(frames_loaded)):        
        
            print '\n\n### Frame extraction ###\n'
    
            # Save processing time
            start_time = cv2.getTickCount() 
               
            res_name = self.resource_name   
            
            if(not(os.path.exists(frames_path))):
                
                os.makedirs(frames_path)   
                 
            # Counter for all frames
            frame_counter = 0       
            
            # Value of frame_counter for last analyzed frame
            last_anal_frame = 0
            
            # Open video file
            capture = cv2.VideoCapture(resource)
            
            self.frame_list = []
            
            # Save parameters for this video
            param_dict = {}
            
            if capture is None or not capture.isOpened():
                
                error = 'Error in opening video file'
                
                print error
                
                return
    
            else:
                
                video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
                
                param_dict[VIDEO_FPS_KEY] = video_fps
                
                # Original number of frames
                tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
                
                param_dict[VIDEO_TOT_FRAMES_KEY] = tot_frames
                
                self.fps = video_fps
                
                self.video_frames = float(tot_frames)
                
                # Saved frames
                saved_frames = 0
                
                while True:
                    
                    # Read frame
                    ret, frame = capture.read()
                    
                    # If not frame is read, abort
                    if(not(ret)):
                        
                        break
                        
                    # Next frame to be analyzed
                    next_frame = last_anal_frame + (video_fps/(USED_FPS+1))
                    
                    if(USE_ORIGINAL_FPS or (frame_counter > next_frame)):
                    
                        # Frame position in video in milliseconds
                        elapsed_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                        
                        #print 'elapsed video s =', elapsed_video_s             
                        
                        fr_name = '%07d.png' % frame_counter
                        
                        frame_path = os.path.join(frames_path, fr_name)
                        
                        # Resize frame
                        if(not(USE_ORIGINAL_RES)):
                            
                            fx = USED_RES_SCALE_FACTOR
                            
                            fy = USED_RES_SCALE_FACTOR
                            
                            interp = cv2.INTER_AREA
                            
                            frame = cv2.resize(src = frame, dsize = (0, 0), 
                            fx = fx, fy = fy, interpolation = interp)
                        
                        cv2.imwrite(frame_path, frame, [cv.CV_IMWRITE_PNG_COMPRESSION, 0])
                        
                        frame_dict = {}
                        
                        frame_dict[FRAME_PATH_KEY] = frame_path
                        
                        frame_dict[ELAPSED_VIDEO_TIME_KEY] = int(elapsed_ms)
                        
                        self.frame_list.append(frame_dict) 
                        
                        last_anal_frame = frame_counter
                        
                        saved_frames = saved_frames + 1
                        
                    frame_counter = frame_counter + 1 
                    
                    self.progress = 100 * (frame_counter / self.video_frames)
        
                    print('progress: ' + str(self.progress) + ' %      \r'),             
    
            self.saved_frames = float(saved_frames)
    
            param_dict[VIDEO_SAVED_FRAMES_KEY] = self.saved_frames
    
            # Save frame list in YAML file
            save_YAML_file(frames_file_path, self.frame_list)
            
            # Save video parameters in YAML file
            file_name = res_name + '_parameters.YAML'
            
            file_path = os.path.join(video_path, file_name)
            
            save_YAML_file(file_path, param_dict) 
    
            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            print 'Time for frame extraction:', str(time_in_seconds), 's\n'

            self.anal_times[FRAME_EXTRACTION_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)


    def trackFacesInVideo(self):
        '''
        Track faces on analyzed video.
        It works by using list of detected faces
        '''
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for tracking results
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        track_file_path = os.path.join(track_path, file_name)
        
        track_loaded = False
        
        # Try to load YAML file with tracking results
        if(os.path.exists(track_file_path)):
            
            print 'Loading YAML file with tracking results'
            
            track_faces = load_YAML_file(track_file_path)
            
            if(track_faces):
                
                self.tracked_faces = track_faces
                
                print 'YAML file with tracking results loaded'
                
                track_loaded = True
                
        if(not(track_loaded)):
        
            # Check existence of detection results
            det_path = os.path.join(video_path, FACE_DETECTION_DIR) 
    
            if(len(self.detected_faces) == 0):
                
                file_path = os.path.join(det_path, file_name)
                
                # Try to load YAML file
                if(os.path.exists(file_path)):
                    
                    print 'Loading YAML file with detection results'
                    
                    with open(file_path) as f:
        
                        self.detected_faces = yaml.load(f) 
                        
                    print 'YAML file with detection results loaded'
                        
                else:
                    
                    print 'Warning! No detection results found!'
                    
                    return              
            
            # Get shot cuts
            self.calcHistDiff()
            
            print '\n\n### Face tracking ###\n'
            
            # Save processing time
            start_time = cv2.getTickCount()
                    
            self.tracked_faces = []
            
            self.disc_tracked_faces = []
            
            # Counter for frames with detected faces
            frame_counter = 0
            
            # Minimum duration of a segment in frames
            min_segment_frames = int(
            math.ceil(self.fps * MIN_SEGMENT_DURATION))
            
            # If a reduced bitrate is used, frames are less
            if(not(USE_ORIGINAL_FPS)):
                
                min_segment_frames = int(
                math.ceil((USED_FPS+1) * MIN_SEGMENT_DURATION))
            
            # Make copy of detected faces
            detection_list = list(self.detected_faces)
            
            # Iterate through frames in detected_faces
            for detection_dict in detection_list:
                
                self.progress = 100 * (frame_counter / self.saved_frames)
        
                print('progress: ' + str(self.progress) + ' %          \r'),
                
                elapsed_s = detection_dict[ELAPSED_VIDEO_TIME_KEY]
                
                frame_path = detection_dict[FRAME_PATH_KEY]
                
                # Read image from given path
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                
                # Convert image to hsv
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                
                mask = cv2.inRange(
                hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                
                faces = detection_dict[FACES_KEY]
                
                face_counter = 0
                
                # Iterate though faces in frame
                for face_dict in faces:
                    
                    track_window = face_dict[BBOX_KEY]
                    
                    left_eye_pos = face_dict[LEFT_EYE_POS_KEY]
                    
                    right_eye_pos = face_dict[RIGHT_EYE_POS_KEY]
                    
                    nose_pos = face_dict[NOSE_POSITION_KEY] 
                    
                    # Start new segment
                    segment_dict = {}
                    
                    segment_dict[SEGMENT_START_KEY] = elapsed_s
                    
                    segment_face_counter = 1 # Counter for faces in segment
                    
                    # Counter for detected faces in segment
                    #det_face_counter = 1 
                    
                    segment_frame_list = []
                    
                    segment_frame_dict = {}
                    segment_frame_dict[FRAME_COUNTER_KEY] = frame_counter
                    segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
                    segment_frame_dict[DETECTION_BBOX_KEY] = track_window
                    segment_frame_dict[TRACKING_BBOX_KEY] = track_window
                    segment_frame_dict[LEFT_EYE_POS_KEY] = left_eye_pos
                    segment_frame_dict[RIGHT_EYE_POS_KEY] = right_eye_pos
                    segment_frame_dict[NOSE_POSITION_KEY] = nose_pos
                    segment_frame_dict[DETECTED_KEY] = True
                    
                    segment_frame_dict[FRAME_PATH_KEY] = frame_path
                    segment_frame_list.append(segment_frame_dict)
                                    
                    x0 = track_window[0]
                    y0 = track_window[1]
                    w = track_window[2]
                    h = track_window[3]
                    x1 = x0 + w
                    y1 = y0 + h
                    
                    prev_det_bbox = track_window
                    
                    # Set up the Region Of Interest for tracking
                    hsv_roi = hsv[y0:y1, x0:x1]
                   
                    mask_roi = mask[y0:y1, x0:x1]
                        
                    hist = cv2.calcHist(
                    [hsv_roi], [0], mask_roi, [16], [0, 180])
                    
                    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                    hist = hist.reshape(-1)
                    
                    # Face should not be considered anymore
                    del (detection_list[frame_counter]
                    [FACES_KEY][face_counter])
                    
                    sub_frame_counter = frame_counter + 1
                    
                    missed_det_counter = 0
                    
                    # Iterate through subsequent frames
                    for sub_det_dict in detection_list[sub_frame_counter:]:
                
                        # TODO: TO BE DELETED
                        #use_fixed_threshold = True
                        
                        #if(use_fixed_threshold):
                            
                            ## Check if histogram difference for this frame
                            ## is greater than the threshold
                            #if(self.track_threshold > 0):
                                
                                #diff = self.hist_diffs[sub_frame_counter]
                                
                                #if(diff != -1):
                                    
                                    #if(diff > self.track_threshold):
                                        
                                        #break 
                                        
                        #else:
                            
                        # Check if a new shot begins
                        if(sub_frame_counter in self.cut_idxs):
                                
                            break
                
                        sub_frame_path = sub_det_dict[FRAME_PATH_KEY]
                    
                        # Read image from given path
                        sub_image = cv2.imread(
                        sub_frame_path, cv2.IMREAD_COLOR)
                
                        # Convert image to hsv
                        sub_hsv = cv2.cvtColor(sub_image, cv2.COLOR_BGR2HSV)
                
                        sub_mask = cv2.inRange(sub_hsv, 
                        np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                        
                        # Apply meanshift to get the new location
                        prob = cv2.calcBackProject(
                        [sub_hsv], [0], hist, [0, 180], 1)
                        prob &= sub_mask
                        term_crit = (cv2.TERM_CRITERIA_EPS 
                        | cv2.TERM_CRITERIA_COUNT, 10, 1)
    
                        track_box, track_window = cv2.CamShift(
                        prob, track_window, term_crit)
                        
                        track_x0 = track_window[0]
                        track_y0 = track_window[1]
                        track_w = track_window[2]
                        track_h = track_window[3]
                        track_x1 = track_x0 + track_w
                        track_y1 = track_y0 + track_h
                        
                        # Check size of track window
                        if((track_w <= FACE_DETECTION_MIN_SIZE_WIDTH) 
                        or (track_h <= FACE_DETECTION_MIN_SIZE_HEIGHT)):                    

                            break
                            
                        segment_frame_dict = {}
                        
                        track_list = (
                        int(track_x0), int(track_y0), int(track_w), int(track_h))
                        
                        segment_frame_dict[TRACKING_BBOX_KEY] = track_list 
                        
                        sub_faces = sub_det_dict[FACES_KEY]
                
                        sub_face_counter = 0
                        
                        sim = False
                        
                        sub_face = None
                        
                        det_bbox = None
                        
                        for sub_face_dict in sub_faces:
    
                            det_bbox = sub_face_dict[BBOX_KEY]
                        
                            # If track window corresponds to 
                            # a detected face, 
                            # delete detection from list
                            
                            sim = is_rect_similar(
                            track_window, det_bbox, TRACKING_MIN_INT_AREA)
                            
                            if(sim):
                                
                                #det_face_counter = det_face_counter + 1
                                
                                track_window = det_bbox
                                
                                break
                                
                            sub_face_counter = sub_face_counter + 1 
                            
                        t_x0 = track_window[0]
                        t_y0 = track_window[1]
                        t_w = track_window[2]
                        t_h = track_window[3]
                        t_x1 = t_x0 + t_w
                        t_y1 = t_y0 + t_h
                        
                        ## Check difference between histograms
                        
                        #sub_hsv_roi = hsv[t_y0:t_y1, t_x0:t_x1]
               
                        #sub_mask_roi = mask[t_y0:t_y1, t_x0:t_x1]
                    
                        #sub_hist = cv2.calcHist(
                        #[sub_hsv_roi], [0], sub_mask_roi, [16], [0, 180])
                
                        #cv2.normalize(
                        #sub_hist, sub_hist, 0, 255, cv2.NORM_MINMAX)
                        #sub_hist = sub_hist.reshape(-1)  
                            
                        #diff = abs(cv2.compareHist(
                        #sub_hist, hist, cv.CV_COMP_CHISQR))
                        
                        #if(diff > TRACKING_DIFF_THRESHOLD):
                            
                            #break
                            
                        segment_frame_dict[DETECTION_BBOX_KEY] = det_bbox               
                    
                        # If a detected face corresponds to track window
                        # delete detected face from detection list
                        
                        if(sim):
                        
                            missed_det_counter = 0
                        
                            segment_frame_dict[DETECTED_KEY] = True
                            
                            segment_frame_dict[LEFT_EYE_POS_KEY] = (
                            sub_face_dict[LEFT_EYE_POS_KEY])
                            segment_frame_dict[RIGHT_EYE_POS_KEY] = (
                            sub_face_dict[RIGHT_EYE_POS_KEY])
                            segment_frame_dict[NOSE_POSITION_KEY] = (
                            sub_face_dict[NOSE_POSITION_KEY])
                            
                            del (detection_list[sub_frame_counter]
                            [FACES_KEY][sub_face_counter])                             
                            
                        else:
                            
                            # Check if distance from last detection
                            # is too big
                            missed_det_counter = missed_det_counter + 1
                            
                            if(missed_det_counter > MAX_FR_WITH_MISSED_DET):
                                
                                # Remove last frames and 
                                # interrupt tracking
                                for i in range(0, MAX_FR_WITH_MISSED_DET):
                                
                                    segment_frame_list.pop()
                                    
                                segment_face_counter = (
                                segment_face_counter - MAX_FR_WITH_MISSED_DET)
                                
                                break
                            
                            segment_frame_dict[DETECTED_KEY] = False  
                            
                        elapsed_ms = sub_det_dict[ELAPSED_VIDEO_TIME_KEY]  
                            
                        # Update list of frames for segment
                        segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter
                        segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_ms
                        
                        track_list = (
                        int(t_x0), int(t_y0), int(t_w), int(t_h))
                        
                        segment_frame_dict[TRACKING_BBOX_KEY] = track_list
                        segment_frame_dict[FRAME_PATH_KEY] = sub_frame_path
                        
                        segment_frame_list.append(segment_frame_dict)
                        
                        sub_frame_counter = sub_frame_counter + 1   
                        
                        segment_face_counter = segment_face_counter + 1                 
                    
                    # Segment must be considered only if its number 
                    # of frames is greater or equals than a minimum
                    if(segment_face_counter >= min_segment_frames):
                    
                        segments = self.divideSegmentByFace(segment_frame_list)
    
                        if(len(segments) > 0):
                            
                            self.tracked_faces.extend(segments)
                            
                    else:
                        
                        segment_dict = {}
            
                        segment_dict[FRAMES_KEY] = segment_frame_list
                        
                        self.disc_tracked_faces.append(segment_dict)
                        
                        #print 'segment_face_counter:', segment_face_counter
                        
                        #print 'det_face_counter:', det_face_counter
    
                        #det_pct = (float(det_face_counter) / 
                                   #segment_face_counter)
                        
                        #print 'det pct: ', det_pct
                        
                        #if(det_pct >= MIN_DETECTION_PCT):
                        
                            #self.tracked_faces.append(segment_dict)
                        
                        #else:
                            
                            #self.disc_tracked_faces.append(segment_dict)
                            
                        # Check histograms of detected faces and 
                        # divide segment accordingly   
                    
                    face_counter = face_counter + 1  
                    
                frame_counter = frame_counter + 1
    
            # Create directory for this video  
            
            if(not(os.path.exists(track_path))):
                
                os.makedirs(track_path)   
    
            # Save tracking result in YAML file
            file_name = res_name + '.YAML'
                
            file_path = os.path.join(track_path, file_name)
            
            save_YAML_file(track_file_path, self.tracked_faces) 
    
            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            print 'Time for face tracking:', time_in_seconds, 's\n'
 
            self.anal_times[FACE_TRACKING_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
            
    
    def createClothModel(self, person_dict):
        '''
        Create cloth model of one person.
        
        :type person_dict: dictionary
        :param person_dict: dictionary relative to one person
        '''
    
        # List of color histograms
        model = []
        
        # Extract list of segments from dictionary
        segment_list = person_dict[SEGMENTS_KEY]
        
        # Iterate through list of segments
        for segment_dict in segment_list:
        
            # Extract list of frames
            frame_list = segment_dict[FRAMES_KEY]
            
            for frame_dict in frame_list:
                
                detected = frame_dict[DETECTED_KEY]
                
                # Consider only detected faces
                if(detected):
  
                    frame_path = frame_dict[FRAME_PATH_KEY]
                    
                    face_bbox = frame_dict[DETECTION_BBOX_KEY]
                    
                    # Get region of interest for clothes
                    x0 = face_bbox[0]
                    x1 = x0 + face_bbox[2]
                    y0 = face_bbox[1] + face_bbox[3]
                    y1 = y0 + face_bbox[3]
                    
                    im = cv2.imread(frame_path)
                    
                    roi = im[y0:y1, x0:x1]
                    
                    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
                    mask = cv2.inRange(roi_hsv, 
                    np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                    
                    hists = []
            
                    for ch in range(0, 3):
                
                        hist = cv2.calcHist(
                        [roi_hsv], [ch], mask, [16], [0, 255])
                
                        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                        
                        hist.reshape(-1)
                        
                        hists.append(hist)
                        
                    model.append(hists)
                
        return model
        

    def createFaceModel(self, segment_dict):
        '''
        Create face model of one tracked face.
        
        :type segment_dict: dictionary
        :param segment_dict: video segment relative to tracked face
        ''' 

        #print 'Creating model'
        
        # Extract list of frames from dictionary
        segment_frame_list = segment_dict[FRAMES_KEY]
        
        c = 0
        X, y = [], [] 
        
        offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y)
        dest_sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for recognition results
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
        align_path = os.path.join(rec_path, ALIGNED_FACES_DIR)   
 
        if(not(os.path.exists(align_path))):
                
            # Create directory with aligned faces 
            
            os.makedirs(align_path) 
        
        # Iterate through list of frames
        face_counter = 0
        segment_nose_pos_dict = {}
        for segment_frame_dict in segment_frame_list:
            
            face = self.getFaceFromSegmentFrame(
            segment_frame_dict, align_path)
            
            if(face is not None):
                
                #cv2.imshow('face', face)
                #cv2.waitKey(0)
                X.append(np.asarray(face, dtype = np.uint8))
                y.append(c)
                
                if(USE_NOSE_POS_IN_RECOGNITION):  
                    
                    # Save nose position in segment dictionary
                    nose_pos = segment_frame_dict[NOSE_POSITION_KEY]
                    segment_nose_pos_dict[c] = nose_pos
                    
                face_counter = face_counter + 1
                c = c + 1
            
            # If maximum number of faces is reached, stop adding them
            if(face_counter >= MAX_FACES_IN_MODEL):
                
                print 'Warning! Maximum number of faces in model reached'
                break               
             
        model = cv2.createLBPHFaceRecognizer(
        LBP_RADIUS, LBP_NEIGHBORS, LBP_GRID_X, LBP_GRID_Y)
        model.train(np.asarray(X), np.asarray(y))
        
        if(USE_NOSE_POS_IN_RECOGNITION):
        
            # Save nose positions for this segment in dictionary
            self.nose_pos_list.append(segment_nose_pos_dict)
        
        return model
        
    
    def saveClothModels(self, people):
        '''
        Save cloth models for each people recognized by face
        
        :type people: list
        :param people: list of people
        '''
        
        print '\n\n### Creating cloth models ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 

        res_name = self.resource_name
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for cloth models
        models_path = os.path.join(video_path, CLOTH_MODELS_DIR)
        
        if(not(os.path.exists(models_path))):
                
            os.makedirs(models_path) 
        
        counter = 0
        
        for person_dict in people:
            
            model = self.createClothModel(person_dict)
            
            db_path =  os.path.join(models_path, str(counter))

            with open(db_path, 'w') as f:
                
                pk.dump(model, f)
            
            counter = counter + 1
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
        print 'Time for calculating cloth models:', str(time_in_seconds), 's\n'    
            
        self.anal_times[CLOTH_MODELS_CREATION_TIME_KEY] = time_in_seconds
        
        anal_file_name = res_name + '_anal_times.YAML'
        
        anal_file_path = os.path.join(video_path, anal_file_name)
        
        save_YAML_file(anal_file_path, self.anal_times)
                         
        
    def saveFaceModels(self, segments):
        '''
        Save face models for each tracked face
        
        :type segments: list
        :param segments: list of segments
        '''
        
        print '\n\n### Creating face models ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 

        res_name = self.resource_name
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for face models
        models_path = os.path.join(video_path, FACE_MODELS_DIR) 
        
        if(not(os.path.exists(models_path))):
                
            os.makedirs(models_path) 
        
        counter = 0
        
        self.nose_pos_list = []
        
        for segment_dict in segments:
            
            model = self.createFaceModel(segment_dict)
            
            db_path =  os.path.join(models_path, str(counter))

            model.save(db_path)
            
            counter = counter + 1
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
        print 'Time for calculating face models:', str(time_in_seconds), 's\n'    
            
        self.anal_times[FACE_MODELS_CREATION_TIME_KEY] = time_in_seconds
        
        anal_file_name = res_name + '_anal_times.YAML'
        
        anal_file_path = os.path.join(video_path, anal_file_name)
        
        save_YAML_file(anal_file_path, self.anal_times)
                
            
    def searchClothes(self, ann_people, segment_list, train_model, idx):
        '''        
        Search people that have similar clothes to model
        
        :type ann_people: list
        :param ann_people: list of already checked people
        
        :type segment_list: list
        :param segment_list: list of segments related to the same person
        
        :type train_model: list
        :param train_model: list of color histograms of train clothes
        
        :type idx: int
        :param idx: index of person used for creating model
        '''     
 
        res_name = self.resource_name

        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for cloth models
        models_path = os.path.join(video_path, CLOTH_MODELS_DIR) 
        
        counter = 0
        
        for person_dict in self.recognized_faces:

            if(counter not in ann_people):
                
                # Check if at list one segment in person_dict 
                # overlaps in time with at least one segment in the list
                
                overlap = False
                
                p_segment_list = person_dict[SEGMENTS_KEY]
                
                for p_segment_dict in p_segment_list:
                
                    seg_start = p_segment_dict[SEGMENT_START_KEY]
                    
                    seg_dur = p_segment_dict[SEGMENT_DURATION_KEY]
                    
                    seg_end = seg_start + seg_dur
                    
                    for l_segment_dict in segment_list:
                        
                        l_seg_start = l_segment_dict[SEGMENT_START_KEY]
                        
                        l_seg_dur = l_segment_dict[SEGMENT_DURATION_KEY]
                        
                        l_seg_end = l_seg_start + l_seg_dur
                        
                        if(((seg_start >= l_seg_start) and 
                        (seg_start <= l_seg_end)) or 
                        ((seg_end >= l_seg_start) and 
                        (seg_end <= l_seg_end))):
                            
                            overlap = True
                            break
                            
                    if(overlap):
                        
                        break
                        
                if(overlap):
                
                    counter = counter + 1
                        
                    continue
                
                
                db_path= os.path.join(models_path, str(counter))
                        
                if(os.path.isfile(db_path)):
                    
                    model = None
                    
                    with open(db_path) as f:
                
                        model = pk.load(f) 
                
                    if(model):  
                        
                        intra_dist1 = self.getMeanIntraDistance(train_model)
                        
                        intra_dist2 = self.getMeanIntraDistance(model)
                        
                        dist = self.getMeanInterDistance(train_model, model)
                        
                        print('idx', idx)
                        print('counter', counter)
                        print('dist', dist)
                        
                        if(dist < min(intra_dist1, intra_dist2)):
                            
                            person_segments = person_dict[SEGMENTS_KEY]
                            
                            segment_list.extend(person_segments)
                            
                            ann_people.append(counter)
                            
            counter = counter + 1               
         
        return ann_people 
                        
    
    def searchFace(self, ann_segments, segment_list, train_model, idx):
        '''        
        Search tracked faces that are similar to face in model
        
        :type ann_segments: list
        :param ann_segments: list of already checked segments
        
        :type segment_list: list
        :param segment_list: list of segments related to the same person
        
        :type train_model: LBPHFaceRecognizer
        :param train_model: model of searched face
        
        :type idx: int
        :param idx: index of segment used for creating model
        '''

        res_name = self.resource_name

        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for face models
        models_path = os.path.join(video_path, FACE_MODELS_DIR)

        # Get histograms from model
        
        train_hists = train_model.getMatVector("histograms")
        
        # Get labels from model
        
        train_labels = train_model.getMat("labels")

        sub_counter = 0
        for sub_segment_dict in self.tracked_faces:
            
            #print('ann_segments', ann_segments)
            
            if(sub_counter not in ann_segments):
                
                # Check that this segment do not overlap in time
                # with the other segments in the list
                
                seg_start = sub_segment_dict[SEGMENT_START_KEY]
                
                seg_dur = sub_segment_dict[SEGMENT_DURATION_KEY]
                
                seg_end = seg_start + seg_dur
                
                # If true, segment do overlap
                overlap_seg = False
                
                for l_segment_dict in segment_list:
                    
                    l_seg_start = l_segment_dict[SEGMENT_START_KEY]
                    
                    l_seg_dur = l_segment_dict[SEGMENT_DURATION_KEY]
                    
                    l_seg_end = l_seg_start + l_seg_dur
                    
                    if(((seg_start >= l_seg_start) and 
                    (seg_start <= l_seg_end)) or 
                    ((seg_end >= l_seg_start) and 
                    (seg_end <= l_seg_end))):
                        
                        overlap_seg = True
                        break
                        
                if(overlap_seg):
                    
                    sub_counter = sub_counter + 1
                    
                    continue
                
                db_path= os.path.join(models_path, str(sub_counter))
                        
                if(os.path.isfile(db_path)):
                    
                    model = cv2.createLBPHFaceRecognizer()
                    
                    model.load(db_path)
                
                    if(model):
                        
                        # Get histograms from model
                                
                        model_hists = model.getMatVector("histograms")
                        
                        # Get labels from model
                        
                        model_labels = model.getMat("labels")
                        
                        # Iterate through models related to this segment
                        
                        final_tag = UNDEFINED_TAG
                        
                        final_conf = sys.maxint
                        
                        if(USE_AGGREGATION):
                            
                            frames =  []
                            
                            for i in range(0,len(model_hists)):
                    
                                hist = model_hists[i][0]
                                
                                label = model_labels[i][0]
                                
                                nose_pos = None
                                
                                if(USE_NOSE_POS_IN_RECOGNITION):
                                    
                                    nose_pos = (
                                    self.nose_pos_list[sub_counter][label])
                                
                                # Confidence value
                                conf = sys.maxint
                        
                                # Iterate through LBP histograms 
                                # in training model
                                for t in range(0, len(train_hists)):
                                    
                                    train_hist = train_hists[t][0]
                                    
                                    train_label = train_labels[t][0]
                                    
                                    train_nose_pos = None
                                    
                                    if(USE_NOSE_POS_IN_RECOGNITION):
                                        
                                        train_nose_pos = (
                                        self.nose_pos_list[idx][train_label])
                                    
                                    if(USE_NOSE_POS_IN_RECOGNITION):
                                        
                                        # Compare only faces with
                                        # similar nose position
                                        if((nose_pos is None) or
                                        (train_nose_pos is None)):
                                            
                                            continue
                                            
                                        nose_diff_x = (
                                        abs(nose_pos[0] - train_nose_pos[0]))
                                        
                                        nose_diff_y = (
                                        abs(nose_pos[1] - train_nose_pos[1]))
                                        
                                        if((nose_diff_x > MAX_NOSE_DIFF)
                                        or (nose_diff_y > MAX_NOSE_DIFF)):
                                            
                                            ### TEST ONLY ###
                                            if(sub_counter == -1):
                                                print('\n')
                                                print('Nose position diff too big!')
                                                print('sub_counter', sub_counter)
                                                print('label', label)
                                                print('idx', idx)
                                                print('train_label', train_label)
                                                print('nose_diff_x', nose_diff_x)
                                                print('nose_diff_y', nose_diff_y)
                                                
                                                query_frames_list = sub_segment_dict[FRAMES_KEY]
                                                query_dict = query_frames_list[sub_counter]
                                                query_frame_path = query_dict[FRAME_PATH_KEY]
                                                
                                                train_segment = self.tracked_faces[idx]
                                                train_frames_list = train_segment[FRAMES_KEY]
                                                train_dict = train_frames_list[t]
                                                train_frame_path = train_dict[FRAME_PATH_KEY]
                                                
                                                query_face = fd.detect_faces_in_image(query_frame_path, None, True)
                                                
                                                train_face = fd.detect_faces_in_image(train_frame_path, None, True)
                                                
                                                both = np.hstack((query_face, train_face))
                                                
                                                cv2.imshow('Different faces', both)
                                                cv2.waitKey(0)
                                            
                                            ##################                                            
                                            
                                            continue
                                            
                                        else:
                                            
                                            ### TEST ONLY ###
                                            if(sub_counter == -1):
                                                print('\n')
                                                print('Nose position diff is good')
                                                print('sub_counter', sub_counter)
                                                print('label', label)
                                                print('idx', idx)
                                                print('train_label', train_label)
                                                print('nose_diff_x', nose_diff_x)
                                                print('nose_diff_y', nose_diff_y)
                                                
                                                query_frames_list = sub_segment_dict[FRAMES_KEY]
                                                query_dict = query_frames_list[sub_counter]
                                                query_frame_path = query_dict[FRAME_PATH_KEY]
                                                
                                                train_segment = self.tracked_faces[idx]
                                                train_frames_list = train_segment[FRAMES_KEY]
                                                train_dict = train_frames_list[t]
                                                train_frame_path = train_dict[FRAME_PATH_KEY]
                                                
                                                query_face = fd.detect_faces_in_image(query_frame_path, None, True)
                                                
                                                train_face = fd.detect_faces_in_image(train_frame_path, None, True)
                                                
                                                both = np.hstack((query_face, train_face))
                                                
                                                cv2.imshow('Similar faces', both)
                                                cv2.waitKey(0)
                                            
                                            ################## 
                                
                                    diff = cv2.compareHist(
                                    hist, train_hist, cv.CV_COMP_CHISQR)
                                    
                                    if(diff < conf):
                                        
                                        conf = diff
                                
                                #print ('conf', conf)
                                frame_dict = {}
                                frame_dict[CONFIDENCE_KEY] = conf
                                ass_tag = UNDEFINED_TAG
                                
                                if(conf < CONF_THRESHOLD):
                                    
                                    ass_tag = TRACKED_PERSON_TAG
                                    
                                frame_dict[ASSIGNED_TAG_KEY] = ass_tag
                                
                                frames.append(frame_dict)
                        
                            tgs = (TRACKED_PERSON_TAG, UNDEFINED_TAG)
                            
                            [final_tag, final_conf, pct] = (
                            aggregate_frame_results(frames, tags = tgs))
                            
                            print('train index', idx)
                            print('query index', sub_counter)
                            print('final_tag', final_tag)
                            print('confidence', final_conf)
                            print('number of frames', len(frames))
                            print('Percentage', pct)
                            print('\n')
                            
                        else:
                            
                            for i in range(0,len(model_hists)):
                    
                                hist = model_hists[i][0]
                        
                                # Iterate through LBP histograms in training model
                                for t in range(0, len(train_hists)):
                                    
                                    train_hist = train_hists[t][0]
                                
                                    diff = cv2.compareHist(
                                    hist, train_hist, cv.CV_COMP_CHISQR)
                                    
                                    if(diff < final_conf):
                                        
                                        final_conf = diff                           
                        
                            if(final_conf < CONF_THRESHOLD):
                                    
                                final_tag = TRACKED_PERSON_TAG
                                    
                        #print('final_tag', final_tag)
                        #print('final_confidence', final_conf)
                            
                        # Person in segment is recognized
                        if(final_tag ==  TRACKED_PERSON_TAG):
                            
                            segment_dict = {}
                            
                            sub_fr_list = sub_segment_dict[FRAMES_KEY]
                            
                            segment_dict[FRAMES_KEY] = sub_fr_list
                            
                            segment_dict[ASSIGNED_TAG_KEY] = final_tag
                            
                            segment_dict[CONFIDENCE_KEY] = final_conf
                            
                            # Start of segment in milliseconds 
                            # of elapsed time in video
                            
                            start = sub_segment_dict[SEGMENT_START_KEY]
                            
                            segment_dict[SEGMENT_START_KEY] = start
                            
                            # Duration of segment in milliseconds
                            
                            duration = sub_segment_dict[SEGMENT_DURATION_KEY]
                            
                            segment_dict[SEGMENT_DURATION_KEY] = duration
                            
                            segment_list.append(segment_dict) 
                            
                            # Do not consider this segment anymore
                            ann_segments.append(sub_counter)      
                     
            #print('sub_counter', sub_counter)                            
            sub_counter = sub_counter + 1
    
        return ann_segments


    def recognizeClothesInVideo(self):
        '''
        Recognize distinct people on analyzed video
        by using cloth color, 
        assigning a generic tag to each person.
        It works by using a list of people recognized by using faces
        '''
        
        res_name = self.resource_name

        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for recognition results
        rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR)  
        
        # Directory for face models
        models_path = os.path.join(video_path, CLOTH_MODELS_DIR)
        
        rec_file_path = os.path.join(rec_path, file_name)
        
        rec_loaded = False      

        # Try to load YAML file with clothin recognition results
        if(os.path.exists(rec_file_path)):
            
            print 'Loading YAML file with recognition results'
            
            rec_faces = load_YAML_file(rec_file_path)
            
            if(rec_faces):
                
                self.recognized_faces = rec_faces
                
                print 'YAML file with recognition results loaded'
                
                rec_loaded = True
                
        if(not(rec_loaded)):
        
            # Check existence of face recognition results
            track_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
            
            file_name = res_name + '.YAML'
                
            file_path = os.path.join(track_path, file_name)
            
            if(len(self.recognized_faces) == 0):
                
                # Try to load YAML file
                if(os.path.exists(file_path)):
                    
                    print 'Loading YAML file with face recognition results'
                    
                    with open(file_path) as f:
        
                        self.recognized_faces = yaml.load(f) 
                        
                    print 'YAML file with face recognition results loaded'
                        
                else:
                    
                    print 'Warning! No face recognition results found!'
                    
                    return   
                    
            # Make copy of recognized faces
            face_rec_list = list(self.recognized_faces)
            
            # Save clothing models
            self.saveClothModels(face_rec_list)
            
            print '\n\n### Clothing Recognition ###\n'
            
            # Save processing time
            start_time = cv2.getTickCount()
            
            rec_faces = []
            
            # Get threshold
            self.getClothThreshold()
            
            # List of people already analyzed and annotated
            ann_same_face_people = []
            
            # Iterate through tracked faces
    
            same_face_person_counter = 0
            tag = 0
  
            same_face_people_nr = float(len(face_rec_list))
            
            for same_face_person_dict in face_rec_list:
                
                self.progress = 100 * (
                same_face_person_counter / same_face_people_nr)
        
                print('progress: ' + str(self.progress) + ' %          \r'), 
                
                if(same_face_person_counter not in ann_same_face_people):
                        
                    # Save all segments relative 
                    # to one person in person_dict
                    person_dict = {}
                    
                    person_dict[ASSIGNED_TAG_KEY] = tag
                    
                    ann_same_face_people.append(same_face_person_counter)
                    
                    segment_list = []
                    
                    same_face_segments = same_face_person_dict[SEGMENTS_KEY]
                    
                    for same_face_segment in same_face_segments:
                    
                        segment_list.append(same_face_segment)
                    
                    db_path= os.path.join(
                    models_path, str(same_face_person_counter))
                    
                    if(os.path.isfile(db_path)):
                    
                        with open(db_path) as f:
                    
                            model = pk.load(f) 
                    
                        if(model):
                            
                            # Use model of this person's clothes
                            # to recognize other people
                            
                            if(self.cloth_threshold > 0):
                            
                                ann_same_face_people = self.searchClothes(
                                ann_same_face_people, segment_list, 
                                model, same_face_person_counter)
                            
                            # Add segments to person dictionary
                            
                            person_dict[SEGMENTS_KEY] = segment_list
                            
                            # Save total duration of video in milliseconds
                            
                            tot_duration = self.video_frames * 1000.0 / self.fps
                            
                            person_dict[VIDEO_DURATION_KEY] = tot_duration

                            rec_faces.append(person_dict)
                            
                            tag = tag + 1
                    
                same_face_person_counter = same_face_person_counter + 1 
            
            if(not(os.path.exists(rec_path))):
                
                # Create directory for this video
                os.makedirs(rec_path) 
            
            self.recognized_faces = rec_faces
            
            # Save recognition result in YAML file
            save_YAML_file(rec_file_path, self.recognized_faces) 
            
            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            print 'Time for clothing recognition:', time_in_seconds, 's\n'
            
            self.anal_times[CLOTHIN_RECOGNITION_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
    
    
    def recognizeFacesInVideo(self):       
        '''
        Recognize distinct faces on analyzed video,
        assigning a generic tag to each face.
        It works by using a list of tracked faces
        '''   
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for recognition results
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR)  
        
        # Directory for face models
        models_path = os.path.join(video_path, FACE_MODELS_DIR)
        
        rec_file_path = os.path.join(rec_path, file_name)
        
        rec_loaded = False
        
        # Try to load YAML file with recognition results
        if(os.path.exists(rec_file_path)):
            
            print 'Loading YAML file with recognition results'
            
            rec_faces = load_YAML_file(rec_file_path)
            
            if(rec_faces):
                
                self.recognized_faces = rec_faces
                
                print 'YAML file with recognition results loaded'
                
                rec_loaded = True
                
        if(not(rec_loaded)):
        
            # Check existence of tracking results
            track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
            
            file_name = res_name + '.YAML'
                
            file_path = os.path.join(track_path, file_name)
            
            if(len(self.tracked_faces) == 0):
                
                # Try to load YAML file
                if(os.path.exists(file_path)):
                    
                    print 'Loading YAML file with tracking results'
                    
                    with open(file_path) as f:
        
                        self.tracked_faces = yaml.load(f) 
                        
                    print 'YAML file with tracking results loaded'
                        
                else:
                    
                    print 'Warning! No tracking results found!'
                    
                    return              
            
            # Make copy of tracked faces
            tracking_list = list(self.tracked_faces)
            
            # Save face models
            self.saveFaceModels(tracking_list)
            
            print '\n\n### Face Recognition ###\n'
            
            # Save processing time
            start_time = cv2.getTickCount()
            
            self.recognized_faces = []
            
            # List of segments already analyzed and annotated
            ann_segments = []
            
            # Iterate through tracked faces
    
            segment_counter = 0
            tag = 0
  
            tracked_faces_nr = float(len(tracking_list))
            
            for tracking_segment_dict in tracking_list:
                
                self.progress = 100 * (segment_counter / tracked_faces_nr)
        
                print('progress: ' + str(self.progress) + ' %          \r'), 
                
                if(segment_counter not in ann_segments):
                        
                    # Save all segments relative 
                    # to one person in person_dict
                    person_dict = {}
                    
                    person_dict[ASSIGNED_TAG_KEY] = tag
                    
                    segment_list = []
                    
                    segment_dict = {}
                    
                    segment_frame_list = tracking_segment_dict[FRAMES_KEY]
                    
                    segment_dict[FRAMES_KEY] = segment_frame_list
                    
                    segment_dict[ASSIGNED_TAG_KEY] = tag
                    
                    segment_dict[CONFIDENCE_KEY] = 0
                    
                    # Start of segment in milliseconds 
                    # of elapsed time in video
                    
                    start = tracking_segment_dict[SEGMENT_START_KEY]
                    
                    segment_dict[SEGMENT_START_KEY] = start
                    
                    # Duration of segment in milliseconds
                    
                    duration = tracking_segment_dict[SEGMENT_DURATION_KEY]
                    
                    segment_dict[SEGMENT_DURATION_KEY] = duration
                    
                    segment_list.append(segment_dict)
                    
                    ann_segments.append(segment_counter)
                    
                    db_path= os.path.join(models_path, str(segment_counter))
                    
                    if(os.path.isfile(db_path)):
                        
                        model = cv2.createLBPHFaceRecognizer()
                        
                        model.load(db_path)
                    
                        if(model):

                            # Use model of this segment 
                            # to recognize faces of remaining segments
                            ann_segments = self.searchFace(ann_segments, 
                            segment_list, model, segment_counter)
                            
                            # Add segments to person dictionary
                            
                            person_dict[SEGMENTS_KEY] = segment_list
                            
                            # Save total duration of video in milliseconds
                            
                            tot_duration = self.video_frames * 1000.0 / self.fps
                            
                            person_dict[VIDEO_DURATION_KEY] = tot_duration
                            
                            self.recognized_faces.append(person_dict)
                            
                            tag = tag + 1
                    
                segment_counter = segment_counter + 1 
            
            if(not(os.path.exists(rec_path))):
                
                # Create directory for this video
                os.makedirs(rec_path) 
            
            # Save recognition result in YAML file
            save_YAML_file(rec_file_path, self.recognized_faces) 
            
            # Save processing time
            time_in_clocks = cv2.getTickCount() - start_time
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            print 'Time for face recognition:', time_in_seconds, 's\n'
            
            self.anal_times[FACE_RECOGNITION_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
  
        
    def getFaceFromSegmentFrame(self, segment_frame_dict, align_path):
        '''
        Get face from frame of one tracking segment.
        
        :type segment_frame_dict: dictionary
        :param segment_frame_dict: frame containing face
        
        :type align_path: string
        :param align_path: path of directory 
        where aligned faces are saved        
        ''' 
        
        result = None
        
        offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y)
        dest_sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
        
        frame_path = segment_frame_dict[FRAME_PATH_KEY]
        
        image = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
        
        is_detected = segment_frame_dict[DETECTED_KEY]
        
        if(is_detected):
            
            # If face is detected, we know its eye positions
            
            left_eye_pos = segment_frame_dict[LEFT_EYE_POS_KEY] 
            right_eye_pos = segment_frame_dict[RIGHT_EYE_POS_KEY]
            
            eye_pos = (left_eye_pos[0], left_eye_pos[1],
                       right_eye_pos[0], right_eye_pos[1])
                       
            face = fd.get_cropped_face_using_eye_pos(
            frame_path, align_path, eye_pos, offset_pct, dest_sz)
            
            if(face is not None):
                
                result = face
                
        else:
            
            # Else, we know only the bounding box
            # If nose position is used, only detected faces can be used
            
            if(not(USE_NOSE_POS_IN_RECOGNITION)):
                
                bbox = segment_frame_dict[TRACKING_BBOX_KEY]
                
                x0 = bbox[0]
                x1 = x0 + bbox[2]
                y0 = bbox[1]
                y1 = y0 + bbox[3]
                
                tracked_face = image[y0:y1, x0:x1]
                
                cv2.imwrite(TMP_TRACKED_FACE_FILE_PATH, tracked_face)
    
                crop_result = fd.get_cropped_face(
                TMP_TRACKED_FACE_FILE_PATH, align_path, offset_pct, dest_sz, False)
                
                if(crop_result):
                    
                    face = crop_result[FACE_KEY]
                    
                    if(face is not None):
                        
                        result = face
                    
        return result


    def saveDiscTrackingSegments(self):
        '''
        Save frames from discarded tracking segments on disk.
        A folder contains the frames from one segment
        '''         
        
        print '\n\n### Saving discarded tracking segments ###\n'
        
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        segments_path = os.path.join(
        track_path, FACE_TRACKING_SEGMENTS_DIR)  
        
        segments_path = segments_path + '_discarded'
        
        # Delete already saved files
        if(os.path.exists(segments_path)):
            
            images_dirs = os.listdir(segments_path)
            
            for images_dir in images_dirs:
                
                images_dir_path = os.path.join(segments_path, images_dir)
                shutil.rmtree(images_dir_path)
        
        disc_tracked_faces_nr = float(len(self.disc_tracked_faces))
        
        segment_counter = 0
        
        for segment_dict in self.disc_tracked_faces:
            
            self.progress = 100 * (segment_counter / disc_tracked_faces_nr)
    
            print('progress: ' + str(self.progress) + ' %          \r'),
            
            segment_frame_list = segment_dict[FRAMES_KEY]
            
            segment_path = os.path.join(
            segments_path, str(segment_counter))
            
            if(not(os.path.exists(segment_path))):
                
                os.makedirs(segment_path)
            
            image_counter = 0
            
            for segment_frame_dict in segment_frame_list:
                
                frame_path = segment_frame_dict[FRAME_PATH_KEY]
                
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                
                # Add tracking window to image as red rectangle
                track_bbox = segment_frame_dict[TRACKING_BBOX_KEY]
                
                x0 = track_bbox[0]
                x1 = x0 + track_bbox[2]
                y0 = track_bbox[1]
                y1 = y0 + track_bbox[3]
                              
                cv2.rectangle(
                image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                # Add detection bbox to image as blue rectangle
                det_bbox = segment_frame_dict[DETECTION_BBOX_KEY]
                
                if(det_bbox is not None):
                    x0 = det_bbox[0]
                    x1 = x0 + det_bbox[2]
                    y0 = det_bbox[1]
                    y1 = y0 + det_bbox[3]
                                  
                    cv2.rectangle(
                    image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)
                
                file_name = '%07d.bmp' % image_counter
                
                face_path = os.path.join(segment_path, file_name)
                
                cv2.imwrite(face_path, image)
                
                image_counter = image_counter + 1
                
            segment_counter = segment_counter + 1 


    def saveTrackingSegments(self):
        '''
        Save frames from tracking segments on disk.
        A folder contains the frames from one segment
        '''         
        
        print '\n\n### Saving tracking segments ###\n'
        
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        segments_path = os.path.join(
        track_path, FACE_TRACKING_SEGMENTS_DIR)  
        
        # Delete already saved files
        if(os.path.exists(segments_path)):
            
            images_dirs = os.listdir(segments_path)
            
            for images_dir in images_dirs:
                
                images_dir_path = os.path.join(segments_path, images_dir)
                shutil.rmtree(images_dir_path)
        
        tracked_faces_nr = float(len(self.tracked_faces))
        
        segment_counter = 0
        
        face_counter = 0
        
        for segment_dict in self.tracked_faces:
            
            self.progress = 100 * (segment_counter / tracked_faces_nr)
    
            print('progress: ' + str(self.progress) + ' %          \r'),
            
            segment_frame_list = segment_dict[FRAMES_KEY]
            
            segment_path = os.path.join(
            segments_path, str(segment_counter))
            
            if(not(os.path.exists(segment_path))):
                
                os.makedirs(segment_path)
            
            image_counter = 0
            
            for segment_frame_dict in segment_frame_list:
                
                frame_path = segment_frame_dict[FRAME_PATH_KEY]
                
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

                # Add tracking window to image as red rectangle
                track_bbox = segment_frame_dict[TRACKING_BBOX_KEY]
                
                x0 = track_bbox[0]
                x1 = x0 + track_bbox[2]
                y0 = track_bbox[1]
                y1 = y0 + track_bbox[3]
                   
                # Used to save face images
                image_copy = copy.copy(image)   
                              
                cv2.rectangle(
                image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)

                # Add detection bbox to image as blue rectangle
                det_bbox = segment_frame_dict[DETECTION_BBOX_KEY]
                
                if(det_bbox is not None):
                    x0 = det_bbox[0]
                    x1 = x0 + det_bbox[2]
                    y0 = det_bbox[1]
                    y1 = y0 + det_bbox[3]
                                  
                    cv2.rectangle(
                    image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)
                    
                    # Save face image on disk
                        
                    file_name = '%07d.bmp' % face_counter
                    
                    faces_path = os.path.join(video_path, 'Faces')
                    
                    if(not(os.path.exists(faces_path))):
                
                        os.makedirs(faces_path)
                    
                    face_path = os.path.join(faces_path, file_name)
                    
                    face = image_copy[y0:y1, x0:x1]
            
                    cv2.imwrite(face_path, face)
                    
                    # Save cloth image on disk
                    
                    clothes_path = os.path.join(video_path, 'Clothes')
                    
                    if(not(os.path.exists(clothes_path))):
                
                        os.makedirs(clothes_path)
                    
                    cloth_path = os.path.join(clothes_path, file_name)
                    
                    #print('cloth_path', cloth_path)
                    
                    #raw_input("Press Enter to continue...")
                    
                    old_y0 = y0
                
                    y0 = y1
                
                    y1 = y1 + (y1-old_y0)
                    
                    cloth = image_copy[y0:y1, x0:x1]
            
                    cv2.imwrite(cloth_path, cloth)
                
                # Add rectangle for clothes             
                cv2.rectangle(
                image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                
                file_name = '%07d.bmp' % image_counter
                
                face_path = os.path.join(segment_path, file_name)
                
                cv2.imwrite(face_path, image)
                
                image_counter = image_counter + 1
                
                face_counter = face_counter + 1
                
            segment_counter = segment_counter + 1  
 
 
    def saveRecPeople(self, use_face_rec_dir):
        '''
        Save frames for recognized people on disk.
        A folder contains the segments from one person
        
        :type use_face_rec_dir: boolean
        :param use_face_rec_dir: if true, use FACE_RECOGNITION_DIR, 
        otherwise use CLOTHIN_RECOGNITION_DIR
        '''  
        
        print '\n\n### Saving recognized people ###\n'
               
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)        
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR)
        
        if(not(use_face_rec_dir)):
            
            rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR)
        
        people_path = os.path.join(rec_path, FACE_RECOGNITION_PEOPLE_DIR)
        
        # Delete already saved files
        if(os.path.exists(people_path)):
            
            images_dirs = os.listdir(people_path)
            
            for images_dir in images_dirs:
                
                images_dir_path = os.path.join(people_path, images_dir)
                shutil.rmtree(images_dir_path)    
        
        for person_dict in self.recognized_faces:
            
            tag = person_dict[ASSIGNED_TAG_KEY]
            
            person_path = os.path.join(people_path, str(tag))
            
            segment_list = person_dict[SEGMENTS_KEY]
            
            segment_counter = 0
            
            for segment_dict in segment_list:
                
                track_segment_dict = segment_dict
                
                segment_frame_list = segment_dict[FRAMES_KEY]
                
                segment_path = os.path.join(
                person_path, str(segment_counter))
                
                if(not(os.path.exists(segment_path))):
                    
                    os.makedirs(segment_path)
                
                image_counter = 0
                
                for segment_frame_dict in segment_frame_list:
                    
                    frame_path = segment_frame_dict[FRAME_PATH_KEY]
                    
                    image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                                  
                    # Add tracking window to image as red rectangle
                    track_bbox = segment_frame_dict[TRACKING_BBOX_KEY]
                    
                    x0 = track_bbox[0]
                    x1 = x0 + track_bbox[2]
                    y0 = track_bbox[1]
                    y1 = y0 + track_bbox[3]
                                  
                    cv2.rectangle(
                    image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
    
                    det = segment_frame_dict[DETECTED_KEY]
                    
                    if(det):
    
                        # Add detection bbox to image as blue rectangle
                        det_bbox = segment_frame_dict[DETECTION_BBOX_KEY]
                        
                        x0 = det_bbox[0]
                        x1 = x0 + det_bbox[2]
                        y0 = det_bbox[1]
                        y1 = y0 + det_bbox[3]
                                      
                        cv2.rectangle(
                        image, (x0, y0), (x1, y1), (255, 0, 0), 3, 8, 0)
                    
                    file_name = '%07d.bmp' % image_counter
                    
                    face_path = os.path.join(segment_path, file_name)
                    
                    cv2.imwrite(face_path, image)
                    
                    image_counter = image_counter + 1
                    
                segment_counter = segment_counter + 1 
                
                
    def showRecPeople(self):
        '''
        Show and save one image for each recognized people in video
        ''' 
        
        # If show is True, show image
        show = False 
        
        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
        key_frames_path = os.path.join(
        rec_path, FACE_RECOGNITION_KEY_FRAMES_DIR)
        
        if(not(os.path.exists(key_frames_path))):
            
            os.makedirs(key_frames_path)

        file_name = res_name + '.YAML'
            
        file_path = os.path.join(rec_path, file_name)
        
        if(len(self.recognized_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with recognition results'
                
                with open(file_path) as f:
    
                    self.recognized_faces = yaml.load(f) 
                    
                print 'YAML file with recgnition results loaded'
                    
            else:
                
                print 'Warning! No recognition results found!'
                
                return                      
        
        p_counter = 0
        
        for person_dict in self.recognized_faces:
            
            segment_list = person_dict[SEGMENTS_KEY]
            
            # Get first segment
            if(len(segment_list) >= 1):
                
                first_segment = segment_list[0]
                
                frame_list = first_segment[FRAMES_KEY]      
        
                # Choose central frame in segment
                frames_nr = len(frame_list)
                
                if(frames_nr >= 1):
                    
                    middle_idx = int(math.ceil(frames_nr/2.0) - 1)
                    
                    middle_frame_dict = frame_list[middle_idx]
                    
                    frame_path = middle_frame_dict[FRAME_PATH_KEY]
                    
                    image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                    
                    # Add tracking window to image as red rectangle
                    track_bbox = middle_frame_dict[TRACKING_BBOX_KEY]
                    
                    x0 = track_bbox[0]
                    x1 = x0 + track_bbox[2]
                    y0 = track_bbox[1]
                    y1 = y0 + track_bbox[3]
                                  
                    cv2.rectangle(
                    image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                    
                    # Save image
                    fr_name = '%07d.png' % p_counter
                    
                    fr_path = os.path.join(key_frames_path, fr_name)
                    
                    cv2.imwrite(
                    fr_path, image, [cv.CV_IMWRITE_PNG_COMPRESSION, 0])
                    
                    if(show):
                        
                        person_dict[ANN_TAG_KEY] = UNDEFINED_TAG
                    
                        w_name = WINDOW_PERSON + ' ' + str(p_counter + 1)
                        
                        cv2.imshow(w_name, image)
                        
                        cv2.waitKey(0)
                        
                        final_tag = UNDEFINED_TAG
                        
                        print '### ' + w_name + ' ###\n'
                        ans = ''
                        
                        # Ask contributor if shown person is known
                        while((ans != ANSWER_YES) and (ans != ANSWER_NO)):
                            
                            ans = raw_input(IS_KNOWN_PERSON_ASK)
                            
                        if(ans == ANSWER_YES):
                            name = raw_input(PERSON_NAME + ': ')
                            surname = raw_input(PERSON_SURNAME + ': ')
                            final_tag = surname + '_' + name
                            
                        print '\n'
                        
                        person_dict[ANN_TAG_KEY] = final_tag
                    
                    p_counter = p_counter + 1
                    
        #print(self.recognized_faces)

    def readUserAnnotations(self):
        '''
        Read annotations by user from disk
        '''

        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 

        file_name = res_name + '.YAML'
            
        file_path = os.path.join(rec_path, file_name)
        
        if(len(self.recognized_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with recognition results'
                
                with open(file_path) as f:
    
                    self.recognized_faces = yaml.load(f) 
                    
                print 'YAML file with recgnition results loaded'
                    
            else:
                
                print 'Warning! No recognition results found!'
                
                return 

        user_ann_path = os.path.join(
        rec_path, FACE_RECOGNITION_USER_ANNOTATIONS)
        
        # Create directory for user annotations
        
        if(not(os.path.exists(user_ann_path))):
            
            os.makedirs(user_ann_path)                 
        
        print '\n\n### User annotations ###\n'
        
        raw_input("Press Enter when you are ready to order key frames...")
        
        # Save processing time
        start_time = cv2.getTickCount() 
        
        raw_input("Order key frames, than press Enter to continue...")
    
        auto_p_counter = 0
        
        user_rec_faces = []
        
        # Iterate through automatic recognized faces
        for auto_p_dict in self.recognized_faces:
            
            found = False
            # Search person in directory with user annotations
            for user_tag in os.listdir(user_ann_path):
            
                user_p_path = os.path.join(user_ann_path, user_tag)
                
                # Iterate though all images in directory
                for user_p_image in os.listdir(user_p_path):
                    
                    user_p_counter = os.path.splitext(user_p_image)[0]
                    
                    formatted_auto_p_counter = '%07d' % auto_p_counter
                    
                    if(user_p_counter == formatted_auto_p_counter):
                        
                        auto_p_dict[ANN_TAG_KEY] = user_tag
                        
                        user_rec_faces.append(auto_p_dict)
                        
                        found = True
                        
                        break
                        
                if(found):
                    
                    break
                        
            auto_p_counter = auto_p_counter + 1          
                    
        self.recognized_faces = user_rec_faces
        
        # Save recognition result in YAML file
        save_YAML_file(file_path, self.recognized_faces) 
        
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for user annotation:', time_in_seconds, 's\n'

        self.anal_times[USER_ANNOTATION_TIME_KEY] = time_in_seconds
        
        anal_file_name = res_name + '_anal_times.YAML'
        
        anal_file_path = os.path.join(video_path, anal_file_name)
        
        save_YAML_file(anal_file_path, self.anal_times)
        
    
    def calcHistDiff(self):
        '''
        Calculate histogram differences between consecutive frames
        '''
        
        # Check existence of frame list
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        frame_path = os.path.join(video_path, FRAMES_DIR) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(frame_path, file_name)
        
        if(len(self.frame_list) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with frame list'
                
                with open(file_path) as f:
    
                    self.frame_list = yaml.load(f) 
                    
                print 'YAML file with frame list loaded'
                    
            else:
                
                print 'Warning! No frame list found!'
                
                return         
        
        print '\n\n### Calculating histogram differences ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 

        # List with histogram differences (all frames)
        self.hist_diffs = []
        
        prev_hists = None
        
        counter = 0
        
        # Iterate through all frames
        for frame_dict in self.frame_list:
            
            self.progress = 100 * (counter / self.saved_frames)
    
            print('progress: ' + str(self.progress) + ' %          \r'),
                
            frame_path = frame_dict[FRAME_PATH_KEY]
                
            image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                    
            #Calculate difference between histograms
            [tot_diff, prev_hists] = get_hist_difference(
            image, prev_hists)
            
            if(tot_diff is not None):
                           
                self.hist_diffs.append(tot_diff)
            
            counter = counter + 1 
                
        # Calculate shot cuts
        #print 'diff_list', diff_list
        
        if(len(self.hist_diffs) > 0):
            
            ## Calculate size of sliding window
            #half_w_size = int(
            #math.floor(self.fps * MIN_SEGMENT_DURATION / 2)) 
            
            ## If a reduced bitrate is used, sliding window is smaller
            #if(not(USE_ORIGINAL_FPS)):
                
                #half_w_size = int(math.floor(
                #(USED_FPS+1) * MIN_SEGMENT_DURATION / 2))
            
            self.cut_idxs = get_shot_changes(
            self.hist_diffs, HALF_WINDOW_SIZE, STD_MULTIPLIER_FRAME)    
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for calculation of histogram differences:', time_in_seconds, 's\n'
        
        self.anal_times[SHOT_CUT_DETECTION_TIME_KEY] = time_in_seconds
            
        anal_file_name = res_name + '_anal_times.YAML'
            
        anal_file_path = os.path.join(video_path, anal_file_name)
            
        save_YAML_file(anal_file_path, self.anal_times)                              
           
    
    def saveTempPeopleFiles(self): 
        '''
        Save annotation files for people in this video
        with temporary tags
        '''
        
        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(rec_path, file_name)
        
        if(len(self.recognized_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with recognition results'
                
                with open(file_path) as f:
    
                    self.recognized_faces = yaml.load(f) 
                    
                print 'YAML file with recgnition results loaded'
                    
            else:
                
                print 'Warning! No recognition results found!'
                
                return      
            
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)        
        
        # Create or empty directory with complete annotations
        compl_ann_path = os.path.join(video_path, FACE_TEMP_ANN_DIR)
        
        # Delete already saved files
        if(os.path.exists(compl_ann_path)):
            
            ann_files = os.listdir(compl_ann_path)
            
            for ann_file in ann_files:
                
                ann_file_path = os.path.join(compl_ann_path, ann_file)
                os.remove(ann_file_path)  
                
        else:
            
            os.makedirs(compl_ann_path)
            
        # Create or empty directory with simple annotations
        simple_ann_path = os.path.join(video_path, FACE_TEMP_SIMPLE_ANN_DIR)
        
        # Delete already saved files
        if(os.path.exists(simple_ann_path)):
            
            ann_files = os.listdir(simple_ann_path)
            
            for ann_file in ann_files:
                
                ann_file_path = os.path.join(simple_ann_path, ann_file)
                os.remove(ann_file_path)  
                
        else:
            
            os.makedirs(simple_ann_path)              
        
        counter = 0
         
        for temp_person_dict in self.recognized_faces:
            
            # Create complete annotations
            person_dict = {}
            
            # Create simple annotations
            simple_dict = {}
            
            person_dict[ANN_TAG_KEY] = str(counter)
            
            simple_dict[ANN_TAG_KEY] = str(counter)
            
            segment_list = []
            
            simple_segment_list = []
            
            tot_duration = 0
            
             # Iterate through all recognized people in video
                    
            temp_segment_list = temp_person_dict[SEGMENTS_KEY]
            
            for segment_dict in temp_segment_list:
                
                segment_list.append(segment_dict)
        
                simple_segment_dict = {}
                
                start = segment_dict[SEGMENT_START_KEY]
                
                simple_segment_dict[SEGMENT_START_KEY] = start
                
                duration = segment_dict[SEGMENT_DURATION_KEY]
                
                tot_duration = tot_duration + duration
                
                simple_segment_dict[SEGMENT_DURATION_KEY] = duration
                
                simple_segment_list.append(simple_segment_dict)       
                    
            simple_dict[SEGMENTS_KEY] = simple_segment_list
            
            person_dict[TOT_SEGMENT_DURATION_KEY] = tot_duration
            
            simple_dict[TOT_SEGMENT_DURATION_KEY] = tot_duration
            
            file_name = str(counter) + '.YAML'
            
            # Save complete annotations
            
            file_path = os.path.join(compl_ann_path, file_name)
            
            save_YAML_file(file_path, person_dict)
      
            # Save simple annotations
            
            file_path = os.path.join(simple_ann_path, file_name)
            
            save_YAML_file(file_path, simple_dict)
            
            counter = counter + 1
    
    
    def savePeopleFiles(self): 
        '''
        Save annotation files for people in this video
        '''
        
        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(rec_path, file_name)
        
        if(len(self.recognized_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with recognition results'
                
                with open(file_path) as f:
    
                    self.recognized_faces = yaml.load(f) 
                    
                print 'YAML file with recgnition results loaded'
                    
            else:
                
                print 'Warning! No recognition results found!'
                
                return      
            
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)        
        
        # Create or empty directory with complete annotations
        compl_ann_path = os.path.join(video_path, FACE_ANNOTATION_DIR)
        
        # Delete already saved files
        if(os.path.exists(compl_ann_path)):
            
            ann_files = os.listdir(compl_ann_path)
            
            for ann_file in ann_files:
                
                ann_file_path = os.path.join(compl_ann_path, ann_file)
                os.remove(ann_file_path)  
                
        else:
            
            os.makedirs(compl_ann_path)
            
        # Create or empty directory with simple annotations
        simple_ann_path = os.path.join(video_path, FACE_SIMPLE_ANNOTATION_DIR)
        
        # Delete already saved files
        if(os.path.exists(simple_ann_path)):
            
            ann_files = os.listdir(simple_ann_path)
            
            for ann_file in ann_files:
                
                ann_file_path = os.path.join(simple_ann_path, ann_file)
                os.remove(ann_file_path)  
                
        else:
            
            os.makedirs(simple_ann_path)              
            
        # Save unique tags
        tags = []
        
        for person_dict in self.recognized_faces:
            
            ann_tag = person_dict[ANN_TAG_KEY]
            
            if(ann_tag not in tags):
                
                tags.append(ann_tag)
        
        annotated_faces = []
         
        for tag in tags:
            
            # Create complete annotations
            person_dict = {}
            
            # Create simple annotations
            simple_dict = {}
            
            person_dict[ANN_TAG_KEY] = tag
            
            simple_dict[ANN_TAG_KEY] = tag
            
            segment_list = []
            
            simple_segment_list = []
            
            tot_duration = 0
            
             # Iterate through all recognized people in video
            for temp_person_dict in self.recognized_faces:
                
                ann_tag = temp_person_dict[ANN_TAG_KEY]
                
                if(ann_tag == tag):
                    
                    temp_segment_list = temp_person_dict[SEGMENTS_KEY]
                    
                    for segment_dict in temp_segment_list:
                        
                        segment_list.append(segment_dict)
                
                        simple_segment_dict = {}
                        
                        start = segment_dict[SEGMENT_START_KEY]
                        
                        simple_segment_dict[SEGMENT_START_KEY] = start
                        
                        duration = segment_dict[SEGMENT_DURATION_KEY]
                        
                        tot_duration = tot_duration + duration
                        
                        simple_segment_dict[SEGMENT_DURATION_KEY] = duration
                        
                        simple_segment_list.append(simple_segment_dict)
                    
            person_dict[SEGMENTS_KEY] = segment_list        
                    
            simple_dict[SEGMENTS_KEY] = simple_segment_list
            
            person_dict[TOT_SEGMENT_DURATION_KEY] = tot_duration
            
            simple_dict[TOT_SEGMENT_DURATION_KEY] = tot_duration
            
            file_name = tag + '.YAML'
            
            # Save complete annotations
            
            file_path = os.path.join(compl_ann_path, file_name)
            
            save_YAML_file(file_path, person_dict)
      
            # Save simple annotations
            
            file_path = os.path.join(simple_ann_path, file_name)
            
            save_YAML_file(file_path, simple_dict)


    def divideSegmentByFace(self, segment_frame_list):
        '''
        Divide segment accordingly to face change
        
        :type segment_frame_list: list
        :param segment_frame_list: list of frames in segment
        '''
        
        # List with histogram differences between consecutive frames
        diff_list = []
        
        # List with histogram differences between consecutive detections
        det_diff_list = []
        
        # List that will contain new lists of frames
        sub_segment_list = [] 
        
        prev_hists = None
        
        frame_counter = 0
        
        det_counter = 0
        
        # Dictionary for storing correspondence between counter
        counter_dict = {}
        
        for frame_dict in segment_frame_list:
            
            sim = frame_dict[DETECTED_KEY]
            
            if(sim):
                
                # Tracking window corresponds to detected face
                frame_path = frame_dict[FRAME_PATH_KEY]
            
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                
                bbox = frame_dict[DETECTION_BBOX_KEY]
                
                x0 = bbox[0]
                y0 = bbox[1]
                w = bbox[2]
                h = bbox[3]
                x1 = x0 + w
                y1 = y0 + h
                
                face = image[y0:y1, x0:x1]
                
                [tot_diff, prev_hists] = get_hist_difference(
                face, prev_hists)
                
                if(tot_diff is not None):
                        
                    det_diff_list.append(tot_diff)
                    
                    diff_list.append(tot_diff)
                    
                    counter_dict[det_counter] = frame_counter
                    
                    det_counter = det_counter + 1
                    
                else:
                    
                    diff_list.append(-1)
            
            else:
                
                diff_list.append(-1)
                
            frame_counter = frame_counter + 1
        
        segment_divided = False
                    
        if(len(det_diff_list) > 0):
            
            #half_w_size = int(
            #math.floor(self.fps * MIN_SEGMENT_DURATION / 2)) 
            
            ## If a reduced bitrate is used, sliding window is smaller
            #if(not(USE_ORIGINAL_FPS)):
                
                #half_w_size = int(math.floor(
                #(USED_FPS+1) * MIN_SEGMENT_DURATION / 2))
            
            face_cut_idxs_temp = get_shot_changes(
            det_diff_list, HALF_WINDOW_SIZE, STD_MULTIPLIER_FACE) 
            
            if(len(face_cut_idxs_temp) > 0):
                
                segment_divided = True
                
                # Get real counters
                face_cut_idxs = []
                
                for idx_temp in face_cut_idxs_temp:
                    
                    face_cut_idxs.append(counter_dict[idx_temp])
                    
                # Counter for all frames in original segment
                counter = 0
                
                # Counter for frames with detections in new segment
                det_counter = 0
                
                sub_frame_list = []
                
                for frame_dict in segment_frame_list:
                    
                    if(counter in face_cut_idxs):
                        
                        sub_segment_list.append(sub_frame_list)
                        
                        sub_frame_list = []
                        
                    sub_frame_list.append(frame_dict)
                    
                    counter = counter + 1
                    
                if(len(sub_frame_list) > 0):
                    
                    sub_segment_list.append(sub_frame_list)
        
        # If segment has not been divided, 
        # list will contain only original segment

        if(not(segment_divided)):
            
            sub_segment_list.append(segment_frame_list)
            
        new_segments = []   
            
        # Minimum duration of a segment in frames
        min_segment_frames = int(
        math.ceil(self.fps * MIN_SEGMENT_DURATION))   
        
        # If a reduced bitrate is used, frames are less
        if(not(USE_ORIGINAL_FPS)):
            
            min_segment_frames = int(
            math.ceil((USED_FPS+1) * MIN_SEGMENT_DURATION)) 
            
        # Iterate through new sub segments
        for sub_frame_list in sub_segment_list:
            
            frame_counter = len(sub_frame_list)
            
            segment_dict = {}
        
            segment_dict[FRAMES_KEY] = sub_frame_list
        
            segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = frame_counter         
        
            # Segment duration in milliseconds
            
            duration = frame_counter * 1000.0 / self.fps
            
            # If a reduced bitrate is used, frames are less
            
            if(not(USE_ORIGINAL_FPS)):
            
                duration = frame_counter * 1000.0 / (USED_FPS+1)
        
            segment_dict[SEGMENT_DURATION_KEY] = duration
        
            segment_dict[ASSIGNED_TAG_KEY] = 'Undefined'
        
            segment_dict[CONFIDENCE_KEY] = -1
            
            # Segment must be considered only if its number 
            # of frames is greater or equals than a minimum
            if(frame_counter >= min_segment_frames):
                
                # Start of segment in millisecond
                first_frame_dict = sub_frame_list[0]
                
                segment_start = first_frame_dict[ELAPSED_VIDEO_TIME_KEY]
                
                segment_dict[SEGMENT_START_KEY] = segment_start
                
                det_counter = 0
                
                for frame_dict in sub_frame_list:
                    
                    sim = frame_dict[DETECTED_KEY]
                        
                    if(sim):
                            
                        det_counter = det_counter + 1
                        
                # Check percentage of detection
                det_pct = (float(det_counter) / frame_counter)
                    
                if(det_pct >= MIN_DETECTION_PCT):   
            
                    new_segments.append(segment_dict)
                    
                else:
                    
                    self.disc_tracked_faces.append(segment_dict)
            else:
                
                self.disc_tracked_faces.append(segment_dict)
            
        return new_segments
        
    
    def getClothThreshold(self):
        '''
        Calculate threshold for cloth recognition.
        '''
        
        res_name = self.resource_name

        # Directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        # Directory for cloth models
        models_path = os.path.join(video_path, CLOTH_MODELS_DIR) 
        
        # Get mean intra-person distances
        intra_dist_list = []
        inter_dist_list = []
        
        counter = 0
        
        for person_dict in self.recognized_faces:
            
            #print('counter', counter)
                
            db_path= os.path.join(models_path, str(counter))
                    
            if(os.path.isfile(db_path)):
                
                model = None
                
                with open(db_path) as f:
            
                    model = pk.load(f) 
            
                if(model):
                    
                    print('counter', counter)
                    
                    # Get mean distance between histograms in model
                    dist= self.getMeanIntraDistance(model)
                    
                    print('intra dist', dist)
                    
                    intra_dist_list.append(dist)
                    
                    # Get mean inter-person distances
                    sub_counter = 0
                    
                    for sub_person_dict in self.recognized_faces:
                        
                        if(sub_counter != counter):
                            
                            # Check if at least one segment related 
                            # to person "sub_counter" overlaps in time 
                            # with at least one segment related 
                            # to person "counter"
                            
                            overlap = False
                            
                            segment_list = person_dict[SEGMENTS_KEY]
                            
                            for segment_dict in segment_list:
                                
                                start = segment_dict[SEGMENT_START_KEY]
                                
                                dur = segment_dict[SEGMENT_DURATION_KEY]
                                
                                end = start + dur
                                
                                sub_list = sub_person_dict[SEGMENTS_KEY]
                                
                                for sub_dict in sub_list:
                                    
                                    sub_start = sub_dict[SEGMENT_START_KEY]
                                
                                    sub_dur = sub_dict[SEGMENT_DURATION_KEY]
                                
                                    sub_end = sub_start + sub_dur
                                    
                                    if(((start >= sub_start) and 
                                    (start <= sub_end)) or 
                                    ((end >= sub_start) and 
                                    (end <= sub_end))):
                                
                                        overlap = True
                                        break
                                        
                                if(overlap):
                                    
                                    break
                                    
                            if(overlap):
                                
                                #print('sub_counter', sub_counter)
                                
                                # Get mean distance between histograms 
                                # in  two models
                                sub_db_path= os.path.join(
                                models_path, str(sub_counter))
                    
                                if(os.path.isfile(sub_db_path)):
                
                                    sub_model = None
                
                                    with open(sub_db_path) as f:
            
                                        sub_model = pk.load(f) 
            
                                    if(sub_model):
                                        
                                        # Get mean distance between 
                                        # histograms in two models
                                        dist= self.getMeanInterDistance(
                                        model, sub_model)
                                        
                                        inter_dist_list.append(dist)
                        
                        sub_counter = sub_counter + 1
                    
            counter = counter + 1
            
        mean_intra_dist = np.mean(intra_dist_list)
        
        print('mean_intra_dist', mean_intra_dist)
        
        mean_inter_dist = np.mean(inter_dist_list)
        
        print('mean_inter_dist', mean_inter_dist)
        
        threshold = 0
        
        if(mean_inter_dist > mean_intra_dist):
            
            threshold = mean_intra_dist
            
            print('threshold', threshold)
      
        self.cloth_threshold = threshold
        
        
    def getFaceThreshold(self):
        '''
        Calculate threshold for face recognition.
        Only faces with similar nose position are considered.
        Calculated threshold minimizes the number of 
        same-tracked-segment face pairs whose LBPH difference 
        is over the threshold and the number of same-frame face pairs 
        whose LBPH difference is below the threshold
        '''
        
        
    def getMeanInterDistance(self, model1, model2):
        '''
        Calculate mean distance between histograms in two models
        
        :type model1: list
        :param model1: list of color histograms of clothes
        
        :type model2: list
        :param model2: list of color histograms of clothes 
        to be compared with those of model1
        '''
        
        mean = 0
        
        counter1 = 0
        len_model1 = len(model1)
        len_model2 = len(model2)
        diff_list = []
        
        for counter1 in range(0, len_model1):
            
            hists1 = model1[counter1]
            
            counter2 = 0
            
            for counter2 in range(0, len_model2):
                
                hists2 = model2[counter2]
                
                tot_diff = 0
        
                for ch in range(0, 3):
                    
                    diff = abs(cv2.compareHist(
                    hists1[ch], hists2[ch], cv.CV_COMP_CHISQR))
                    
                    tot_diff = tot_diff + diff  
                    
                diff_list.append(tot_diff)
        
        if(len(diff_list) > 0):
        
                mean = np.mean(diff_list)
        
        return mean 
        
    
    def getMeanIntraDistance(self, model):
        '''
        Calculate mean distance between histograms in model
        
        :type model: list
        :param model: list of color histograms of clothes
        '''
        
        mean = 0
        
        counter = 0
        len_model = len(model)
        diff_list = []
        
        for counter in range(0, len_model):
            
            hists = model[counter]
            
            for sub_counter in range(counter + 1, len_model):
                
                sub_hists = model[sub_counter]
            
                tot_diff = 0
        
                for ch in range(0, 3):
                    
                    diff = abs(cv2.compareHist(
                    hists[ch], sub_hists[ch], cv.CV_COMP_CHISQR))
                    
                    tot_diff = tot_diff + diff
                    
                #print('\n')
                #print('diff', tot_diff)
                #print('counter', counter)
                #print('sub_counter', sub_counter)
            
                diff_list.append(tot_diff)
                
        if(len(diff_list) > 0):
        
                mean = np.mean(diff_list)
        
        return mean
        
        
