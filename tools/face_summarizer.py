import copy

import cv2

import cv2.cv as cv

import face_detection as fd

import math

import matplotlib.pyplot as plt

import numpy as np

import os

import pickle as pk

import shutil

from Constants import *

from Utils import aggregate_frame_results, get_hist_difference, get_shot_changes, is_rect_similar, save_YAML_file

class FaceSummarizer(object):
    '''
    Tool for detecting different faces in video
    '''
    
    def __init__(self, params = None):
        '''
        Initialize the face summarizer
        
        :type  params: dictionary 
        :param params: configuration parameters (see table)        
        '''
        
        self.cut_idxs = [] # List of frame indexes where new shots begin
        
        self.detected_faces = [] # List of detected faces 
        
        # List of tracked faces not considered
        self.disc_tracked_faces = [] 
        
        self.frame_list = [] # List of frame paths
        
        self.fps = 0 # Bitrate of video in frames per second
        
        self.hist_diffs = [] # List with histogram differences
        
        self.params = params
        
        self.recognized_faces = [] # List of recognized faces
        
        self.resource_name = None # Name of resource being analyzed
        
        self.track_threshold = 0 # Threshold for tracking interruption
        
        self.tracked_faces = [] # List of tracked faces
        
        self.video_frames = 0 # Number of frames in video
       
    
    def analizeVideo(self, resource):
        '''
        Analyze video
        
        :type resource: string
        :param resource: file path of resource
        '''
        
        self.getFrameList(resource)
        
        self.detectFacesInVideo()       
    
        self.calcHistDiff()
        
        self.trackFacesInVideo()
        
        self.saveTrackingSegments()
        
        self.recognizeFacesInVideo()
        
        self.saveRecPeople()
        
        self.showRecPeople()
        
        self.savePeopleFiles()
        
        
    def detectFacesInVideo(self):
        '''
        Detect faces on analyzed video.
        It works by using list of extracted frames
        '''
        
        # Check existence of frame list
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        frames_path = os.path.join(video_path, FRAMES_DIR_PATH)  
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(frames_path, file_name)
        
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
        
        print '\n\n### Face detection ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        error = None
        
        detection_params = None
        
        if self.params is not None:
            
            detection_params = self.params[FACE_DETECTION_KEY]
        
        frame_counter = 0
        self.detected_faces = []
        
        # Iterate through frames in frame_list
        for frame_dict in self.frame_list:
            
            self.progress = 100 * (frame_counter / self.video_frames)
    
            print('progress: ' + str(self.progress) + ' %          \r'),
            
            frame_path = frame_dict[FRAME_PATH_KEY] 
            
            #print('frame_path: ' + os.path.basename(frame_path))
            
            detection_result = fd.detect_faces_in_image(
            frame_path, detection_params, False)

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
                    
                    face_dict[LEFT_EYE_POS_KEY] = (
                    det_face[LEFT_EYE_POS_KEY])
                    
                    face_dict[RIGHT_EYE_POS_KEY] = (
                    det_face[RIGHT_EYE_POS_KEY])
                    
                    faces.append(face_dict)                 
                    
            detection_dict[FACES_KEY] = faces
                
            self.detected_faces.append(detection_dict)
            
            frame_counter = frame_counter + 1
   
            if(self.video_frames == 0):
                
                print 'Warning! Number of frames is zero'
                
                break   
         
        det_path = os.path.join(video_path, FACE_DETECTION_DIR) 
        
        if(not(os.path.exists(det_path))):
            
            # Create directory for this video 
            
            os.makedirs(det_path) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(det_path, file_name)
        
        save_YAML_file(file_path, self.detected_faces)      
        
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for face detection: ', time_in_seconds, 's\n'
        
        
    def getFrameList(self, resource):
        '''
        Get frames from one video resource.
        
        :type resource: string
        :param resource: file path of resource
        '''   
        
        print '\n\n### Frame extraction ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        # Get name of resource
        res_name = os.path.basename(resource)
         
        # Save name of resource    
        self.resource_name = res_name     
             
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        frames_path = os.path.join(video_path, FRAMES_DIR_PATH) 
        
        if(not(os.path.exists(frames_path))):
            
            os.makedirs(frames_path)   
             
        # Counter for all frames
        frame_counter = 0       
        
        # Value of frame_counter for last analyzed frame
        last_anal_frame = 0
        
        # Open video file
        capture = cv2.VideoCapture(resource)
        
        self.frame_list = []
        
        if capture is None or not capture.isOpened():
            
            error = 'Error in opening video file'
            
            print error

        else:
            
            video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
            
            tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            
            self.fps = video_fps
            
            self.video_frames = float(tot_frames)
            
            while True:
                
                # Read frame
                ret, frame = capture.read()
                
                # If not frame is read, abort
                if(not(ret)):
                    
                    break
                    
                # Next frame to be analyzed
                next_frame = last_anal_frame + (video_fps/USED_FPS)
                
                if(USE_ORIGINAL_FPS or (frame_counter > next_frame)):
                
                    # Frame position in video in milliseconds
                    elapsed_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                    
                    #print 'elapsed video s =', elapsed_video_s             
                    
                    fr_name = '%07d.bmp' % frame_counter
                    
                    frame_path = os.path.join(frames_path, fr_name)
                    
                    # Resize frame
                    if(not(USE_ORIGINAL_RES)):
                        
                        fx = USED_RES_SCALE_FACTOR
                        
                        fy = USED_RES_SCALE_FACTOR
                        
                        interp = cv2.INTER_AREA
                        
                        frame = cv2.resize(src = frame, dsize = (0, 0), 
                        fx = fx, fy = fy, interpolation = interp)
                    
                    cv2.imwrite(frame_path, frame)
                    
                    frame_dict = {}
                    
                    frame_dict[FRAME_PATH_KEY] = frame_path
                    
                    frame_dict[ELAPSED_VIDEO_TIME_KEY] = int(elapsed_ms)
                    
                    self.frame_list.append(frame_dict) 
                    
                    last_anal_frame = frame_counter
                    
                frame_counter = frame_counter + 1 
                
                self.progress = 100 * (frame_counter / self.video_frames)
    
                print('progress: ' + str(self.progress) + ' %      \r'),             

        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(frames_path, file_name)
        
        save_YAML_file(file_path, self.frame_list) 

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for frame extraction:', str(time_in_seconds), 's\n'


    def trackFacesInVideo(self):
        '''
        Track faces on analyzed video.
        It works by using list of detected faces
        '''
        
        # Check existence of detection results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        det_path = os.path.join(video_path, FACE_DETECTION_DIR) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(det_path, file_name)
        if(len(self.detected_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with detection results'
                
                with open(file_path) as f:
    
                    self.detected_faces = yaml.load(f) 
                    
                print 'YAML file with detection results loaded'
                    
            else:
                
                print 'Warning! No detection results found!'
                
                return              
        
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
        
        # Make copy of detected faces
        detection_list = list(self.detected_faces)
        
        # Iterate through frames in detected_faces
        for detection_dict in detection_list:
            
            self.progress = 100 * (frame_counter / self.video_frames)
    
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
                    if((track_w <= 0) or (track_h <= 0)):                    
                        
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
                        
                    segment_frame_dict[DETECTION_BBOX_KEY] = det_bbox               
                
                    # If a detected face corresponds to track window
                    # delete detected face from detection list
                    
                    if(sim):
                    
                        segment_frame_dict[DETECTED_KEY] = True
                        
                        segment_frame_dict[LEFT_EYE_POS_KEY] = (
                        sub_face_dict[LEFT_EYE_POS_KEY])
                        segment_frame_dict[RIGHT_EYE_POS_KEY] = (
                        sub_face_dict[RIGHT_EYE_POS_KEY])
                        
                        del (detection_list[sub_frame_counter]
                        [FACES_KEY][sub_face_counter])                             
                        
                    else:
                        
                        segment_frame_dict[DETECTED_KEY] = False    
                      
                    elapsed_ms = sub_det_dict[ELAPSED_VIDEO_TIME_KEY]  
                        
                    # Update list of frames for segment
                    segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter
                    segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_ms
                    
                    track_x0 = track_window[0]
                    track_y0 = track_window[1]
                    track_w = track_window[2]
                    track_h = track_window[3]
                    
                    track_list = (
                    int(track_x0), int(track_y0), int(track_w), int(track_h))
                    
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
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        if(not(os.path.exists(track_path))):
            
            os.makedirs(track_path)   

        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(track_path, file_name)
        
        save_YAML_file(file_path, self.tracked_faces) 

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for face tracking:', time_in_seconds, 's\n'
 

    def trackFacesInVideo_old(self):
        '''
        Track faces on analyzed video.
        It works by using list of detected faces
        '''     
        
        print '### Face tracking ###'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        self.tracked_faces = []
        
        # Counter for frames with detected faces
        #det_frame_counter = 0
        frame_counter = 0
        
        # Minimum number of frames from detection 
        # before tracking interruption
        min_tracking_frames = int(
        math.ceil(self.fps * MIN_TRACKING_TIME))
        
        min_segment_frames = int(
        math.ceil(self.fps * MIN_SEGMENT_DURATION))
        
        # Make copy of detected faces
        detection_list = list(self.detected_faces)
        
        # Iterate through frames in detected_faces
        for detection_dict in detection_list:
            
            #det_frame_counter = detection_dict[FRAME_COUNTER_KEY]
            
            elapsed_ms = detection_dict[ELAPSED_VIDEO_TIME_KEY]
            
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
                
                #face = face_dict[FACE_KEY]
                
                left_eye_pos = face_dict[LEFT_EYE_POS_KEY]
                
                right_eye_pos = face_dict[RIGHT_EYE_POS_KEY]
                
                # Start new segment
                segment_dict = {}
                
                segment_face_counter = 1 # Counter for faces in segment
                
                # Counter for detected faces in segment
                det_face_counter = 1 
                
                segment_frame_list = []
                
                segment_frame_dict = {}
                segment_frame_dict[FRAME_COUNTER_KEY] = frame_counter
                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_ms
                segment_frame_dict[BBOX_KEY] = track_window
                #segment_frame_dict[FACE_KEY] = face
                segment_frame_dict[LEFT_EYE_POS_KEY] = left_eye_pos
                segment_frame_dict[RIGHT_EYE_POS_KEY] = right_eye_pos
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
                
                print('track_window', track_window)
                
                # Set up the Region Of Interest for tracking
                hsv_roi = hsv[y0:y1, x0:x1]
               
                mask_roi = mask[y0:y1, x0:x1]
                    
                hist = cv2.calcHist(
                [hsv_roi], [0], mask_roi, [16], [0, 180])
                
                # Use central portion of window
                #w_4 = int(w / 4.0)
                #h_4 = int(h / 4.0)  
                #hsv_roi = hsv[(y0+h_4):(y1-h_4), (x0+w_4):(x1-w_4)]
               
                #mask_roi = mask[(y0+h_4):(y1-h_4), (x0+w_4):(x1-w_4)]
                    
                #prev_hist = cv2.calcHist(
                #[hsv_roi], [0], mask_roi, [16], [0, 180]) 
                
                if(USE_3_CHANNELS):
                    # Calculate histograms for checking histogram 
                    # differences for all 3 channels and without mask
                    prev_hist = []
                    s_hist = cv2.calcHist(
                    [hsv_roi], [1], mask_roi, [16], [60, 255])
                    v_hist = cv2.calcHist(
                    [hsv_roi], [2], mask_roi, [16], [60, 255])
                    prev_hist = [copy.copy(hist), s_hist, v_hist] 
                    
                else:
                    # prev_hist is used for checking histogram differences,
                    # hist is used for tracking
                    #prev_hist = copy.copy(hist)
                    pass
                
                diff_list = [] # List with histogram differences
                
                ## Show image
                cv2.rectangle(
                image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                hist = hist.reshape(-1)
                
                prev_hist = hist
                
                # Face should not be considered anymore
                del (detection_list[frame_counter]
                [FACES_KEY][face_counter])
                
                sub_frame_counter = frame_counter + 1
                
                # Iterate through subsequent frames
                for sub_det_dict in detection_list[sub_frame_counter:]:
            
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
                    
                    #print('track_window before', track_window)
                    track_box, track_window = cv2.CamShift(
                    prob, track_window, term_crit)
                    #print('track_window after', track_window)
                    
                    track_x0 = track_window[0]
                    track_y0 = track_window[1]
                    track_w = track_window[2]
                    track_h = track_window[3]
                    track_x1 = track_x0 + track_w
                    track_y1 = track_y0 + track_h
                    
                    # Check size of track window
                    if((track_w <= 0) or (track_h <= 0)):
                        
                        #cv2.imshow('image', sub_image)
            
                        #cv2.waitKey(0)                      
                        
                        break
                    
                    # Show track window (red) and detection bbox ( blue)
                    cv2.rectangle(sub_image, (track_x0, track_y0), 
                    (track_x1, track_y1), (0, 0, 255), 3, 8, 0) 
                    
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
                            
                            det_face_counter = det_face_counter + 1
                            
                            #track_window = det_bbox
                            
                            #sub_face = sub_face_dict[FACE_KEY]
                            
                            #print('det_bbox', det_bbox)
                            
                            break
                            
                        sub_face_counter = sub_face_counter + 1 
                        
                    # Percentage of detected faces must be greater
                    # than MIN_DETECTION_PCT
                        
                    det_pct = (float(det_face_counter) / 
                              (segment_face_counter + 1))
                    
                    print 'det pct: ', det_pct
                
                    if(det_pct < MIN_DETECTION_PCT):
                        
                        #cv2.imshow('image', sub_image)
            
                        #cv2.waitKey(0) 
                
                        break
                      
                    # Check position, size and histogram difference  
                    # between two consecutive detections  
                    if(sim):
                        
                        x0 = det_bbox[0]
                        y0 = det_bbox[1]
                        w = det_bbox[2]
                        h = det_bbox[3]
                        x1 = x0 + w
                        y1 = y0 + h
                        
                        prev_x0 = prev_det_bbox[0]
                        prev_y0 = prev_det_bbox[1]
                        prev_w = prev_det_bbox[2]
                        prev_h = prev_det_bbox[3]
                        prev_x1 = prev_x0 + prev_w
                        prev_y1 = prev_y0 + prev_h                        
                        
                        delta_x = abs(x0 - prev_x0)/float(prev_w)
                        delta_y = abs(y0 - prev_y0)/float(prev_h)
                        delta_w = abs(w - prev_w)/float(prev_w)

                        #Check if delta is too big 
                        #(only in first frames of segment)
                        if(segment_face_counter <= min_tracking_frames):
                            if((delta_x > MAX_DELTA_PCT_X) 
                            or (delta_y > MAX_DELTA_PCT_Y) 
                            or (delta_w > MAX_DELTA_PCT_W)): 
                                
                                print('delta_x', delta_x)
                                print('delta_y', delta_y)
                                print('delta_w', delta_w)
                                
                                #cv2.imshow('image', sub_image)
                
                                #cv2.waitKey(0)   
                            
                                break
                            
                        prev_det_bbox = det_bbox
                        
                        cv2.rectangle(sub_image, (x0, y0), 
                        (x1, y1), (255, 0, 0), 3, 8, 0) 
                        
                        #x0 = track_window[0]
                        #y0 = track_window[1]
                        #w = track_window[2]
                        #h = track_window[3]
                        #x1 = x0 + w
                        #y1 = y0 + h    
                        
                    # Calculate new histogram
                    ## Use detection bounding box
                    #hsv_roi = sub_hsv[y0:y1, x0:x1]
                    #mask_roi = sub_mask[y0:y1, x0:x1]
                    # Use central portion of tracking window
                    #hsv_roi = sub_hsv[track_y0:track_y1, 
                                      #track_x0:track_x1]
                    #mask_roi = sub_mask[track_y0:track_y1, 
                                        #track_x0:track_x1] 
                             
                    #w_4 = int(track_w / 4.0)
                    #h_4 = int(track_h / 4.0)                    
                    #hsv_roi = sub_hsv[(track_y0 + h_4):(track_y1 - h_4), 
                                      #(track_x0 + w_4):(track_x1 - w_4)]
                    #mask_roi = sub_mask[(track_y0 + h_4):(track_y1 - h_4), 
                                      #(track_x0 + w_4):(track_x1 - w_4)]                                                                              
                               
                    hsv_roi = sub_hsv[track_y0:track_y1, track_x0:track_x1]
                    mask_roi = sub_mask[track_y0:track_y1, track_x0:track_x1]           
                                                     
                    new_hist = cv2.calcHist(
                    [hsv_roi], [0], mask_roi, [16], [0, 180])
                    
                    cv2.normalize(
                    new_hist, new_hist, 0, 255, cv2.NORM_MINMAX)
                    new_hist = new_hist.reshape(-1)
                    
                    # Calculate difference between histograms of 
                    # faces in two consecutive frames
                        
                    diff = 0
                    
                    if(USE_3_CHANNELS):
                        
                        h_diff = abs(cv2.compareHist(prev_hist[0], 
                        new_hist, cv.CV_COMP_CHISQR))
                        
                        new_s_hist = cv2.calcHist(
                        [hsv_roi], [1], mask_roi, [16], [60, 255])
                        
                        s_diff = abs(cv2.compareHist(prev_hist[1], 
                        new_s_hist, cv.CV_COMP_CHISQR))
                        
                        new_v_hist = cv2.calcHist(
                        [hsv_roi], [2], mask_roi, [16], [60, 255])
                        
                        v_diff = abs(cv2.compareHist(prev_hist[2],
                        new_v_hist, cv.CV_COMP_CHISQR)) 
                        
                        diff = h_diff + s_diff + v_diff
                        
                        prev_hist = [new_hist, new_s_hist, new_v_hist]
                        
                    else:
                        
                        diff = abs(cv2.compareHist(
                        prev_hist, new_hist,cv.CV_COMP_CHISQR))  
                        
                        prev_hist = new_hist                 
                    
                    print 'diff = ', diff
                    
                    #cv2.imshow('image', sub_image)
        
                    #cv2.waitKey(0) 
                      
                    if((segment_face_counter > min_tracking_frames)
                        and (len(diff_list) > 0)):
                        
                        mean = np.mean(diff_list)
                        std = np.std(diff_list)
                        
                        threshold = mean + STD_MULTIPLIER * std
                        
                        if(diff > threshold):   
                            
                            print 'threshold = ', threshold
                            
                            cv2.imshow('image', sub_image)
        
                            cv2.waitKey(0)    

                            break

                    # Do not consider first frames in tracking for
                    # threshold calculation    
                    if(segment_face_counter > FRAMES_TO_DISCARD):
                        
                        diff_list.append(diff)
                        
                    diff_list.append(diff)
                    
                    print 'diff = ', diff
                
                    # If a detected face corresponds to track window
                    # delete detected face from detection list
                    
                    segment_frame_dict = {}
                    
                    if(sim):
                        
                        #hist = new_hist
                    
                        segment_frame_dict[DETECTED_KEY] = True
                        
                        segment_frame_dict[LEFT_EYE_POS_KEY] = (
                        sub_face_dict[LEFT_EYE_POS_KEY])
                        segment_frame_dict[RIGHT_EYE_POS_KEY] = (
                        sub_face_dict[RIGHT_EYE_POS_KEY])
                    
                        #cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                        #hist = hist.reshape(-1)
                        
                        del (detection_list[sub_frame_counter]
                        [FACES_KEY][sub_face_counter])                             
                        
                    else:
                        
                        segment_frame_dict[DETECTED_KEY] = False    
                      
                    elapsed_ms = sub_det_dict[ELAPSED_VIDEO_TIME_KEY]  
                        
                    # Update list of frames for segment
                    segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter
                    segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_ms
                    segment_frame_dict[BBOX_KEY] = track_window
                    #segment_frame_dict[FACE_KEY] = sub_face
                    segment_frame_dict[FRAME_PATH_KEY] = sub_frame_path
                    segment_frame_list.append(segment_frame_dict)
                    
                    sub_frame_counter = sub_frame_counter + 1   
                    
                    segment_face_counter = segment_face_counter + 1                 
                
                # Segment must be considered only if its number 
                # of frames is greater or equals than a minimum
                if(segment_face_counter >= min_segment_frames):
                
                    segment_dict[FRAMES_KEY] = segment_frame_list
                    
                    segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = (
                    segment_face_counter)
                    
                    segment_dict[ASSIGNED_TAG_KEY] = 'Undefined'
                    
                    segment_dict[CONFIDENCE_KEY] = -1
                    
                    print 'segment_face_counter:', segment_face_counter
                    
                    det_pct = (float(det_face_counter) / 
                               segment_face_counter)
                    
                    print 'det pct: ', det_pct
                    
                    if(det_pct >= MIN_DETECTION_PCT):
                    
                        self.tracked_faces.append(segment_dict)
                
                face_counter = face_counter + 1  
                
            frame_counter = frame_counter + 1

        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        if(not(os.path.exists(track_path))):
            
            os.makedirs(track_path)   

        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(track_path, file_name)
        
        save_YAML_file(file_path, self.tracked_faces) 

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for face tracking:', time_in_seconds, 's\n'
  
        
    
    def createFaceModel(self, segment_dict):
        '''
        Create face model of one tracked face.
        
        :type segment_dict: dictionary
        :param segment_dict: video segment relative to tracked face
        ''' 
        
        print 'Creating model'
        
        # Extract list of frames from dictionary
        segment_frame_list = segment_dict[FRAMES_KEY]
        
        c = 0
        X, y = [], [] 
        
        offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y)
        dest_sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
        
        # Iterate through list of frames
        face_counter = 0
        for segment_frame_dict in segment_frame_list:
            
            face = self.getFaceFromSegmentFrame(segment_frame_dict)
            
            if(face is not None):
                
                #cv2.imshow('face', face)
                #cv2.waitKey(0)
                X.append(np.asarray(face, dtype = np.uint8))
                y.append(c)
                face_counter = face_counter + 1
            
            # If maximum number of faces is reached, stop adding them
            if(face_counter >= MAX_FACES_IN_MODEL):
                
                print 'Warning! Maximum number of faces in model reached'
                break               
             
        model = cv2.createLBPHFaceRecognizer(
        LBP_RADIUS, LBP_NEIGHBORS, LBP_GRID_X, LBP_GRID_Y)
        model.train(np.asarray(X), np.asarray(y))
        
        return model
        
    def recognizeFacesInVideo(self):       
        '''
        Recognize distinct faces on analyzed video,
        assigning a generic tag to each face
        It works by using list of tracked faces
        '''   
        
        # Check existence of tracking results
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        # Save detection result in YAML file
        file_name = res_name + '.YAML'
            
        file_path = os.path.join(track_path, file_name)
        
        if(len(self.tracked_faces) == 0):
            
            # Try to load YAML file
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with tracking results'
                
                with open(file_path) as f:
    
                    self.detected_faces = yaml.load(f) 
                    
                print 'YAML file with tracking results loaded'
                    
            else:
                
                print 'Warning! No tracking results found!'
                
                return              
        
        
        print '\n\n### Face Recognition ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        self.recognized_faces = []
        
        # List of segments already analyzed and annotated
        ann_segments = []
        
        # Iterate through tracked faces

        segment_counter = 0
        tag = 0
        
        # Make copy of tracked faces
        tracking_list = list(self.tracked_faces)
        
        tracked_faces_nr = len(tracking_list)
        
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
                
                model = self.createFaceModel(tracking_segment_dict)
                
                # Use model of this segment 
                # to recognize faces of remaining segments
                sub_segment_counter = 0
                for sub_segment_dict in self.tracked_faces:
                    
                    #print('ann_segments', ann_segments)
                    
                    if(sub_segment_counter not in ann_segments):
                    
                        segment_fr_list = sub_segment_dict[FRAMES_KEY]
                        
                        frames = []
                        
                        for segment_frame_dict in segment_fr_list:
                            
                            face = self.getFaceFromSegmentFrame(
                            segment_frame_dict)

                            if(face is not None):
                                
                                #cv2.imshow('face', face)
                                #cv2.waitKey(0)
                                
                                [label, conf] = model.predict(
                                np.asarray(face, dtype=np.uint8))
                                
                                #print ('conf', conf)
                                frame_dict = {}
                                frame_dict[CONFIDENCE_KEY] = conf
                                ass_tag = UNDEFINED_TAG
                                
                                if(conf < CONF_THRESHOLD):
                                    
                                    ass_tag = TRACKED_PERSON_TAG
                                    
                                frame_dict[ASSIGNED_TAG_KEY] = ass_tag
                                
                                frames.append(frame_dict)
                        
                        tgs = (TRACKED_PERSON_TAG, UNDEFINED_TAG)
                        
                        [final_tag, final_conf] = (
                        aggregate_frame_results(frames, tags = tgs))
                        
                        print('final_tag', final_tag)
                        print('final_confidence', final_conf)
                            
                        # Person in segment is recognized
                        if(final_tag ==  TRACKED_PERSON_TAG):
                            
                            segment_dict = {}
                            
                            sub_fr_list = sub_segment_dict[FRAMES_KEY]
                            
                            segment_dict[FRAMES_KEY] = sub_fr_list
                            
                            segment_dict[ASSIGNED_TAG_KEY] = tag
                            
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
                            ann_segments.append(sub_segment_counter)      
                             
                    print('sub_segment_counter', sub_segment_counter)                            
                    sub_segment_counter = sub_segment_counter + 1
                
                # Add segments to person dictionary
                
                person_dict[SEGMENTS_KEY] = segment_list
                
                # Save total duration of video in milliseconds
                
                tot_duration = self.video_frames * 1000.0 / self.fps
                
                person_dict[VIDEO_DURATION_KEY] = tot_duration
                
                self.recognized_faces.append(person_dict)
                
                tag = tag + 1
                
            segment_counter = segment_counter + 1
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
        if(not(os.path.exists(rec_path))):
            
            # Create directory for this video
            os.makedirs(rec_path) 
        
        # Save recognition result in YAML file
        file_name = self.resource_name + '.YAML'
            
        file_path = os.path.join(rec_path, file_name)
        
        save_YAML_file(file_path, self.recognized_faces) 
        
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for face recognition:', time_in_seconds, 's\n'


    def getFaceFromSegmentFrame(self, segment_frame_dict):
        '''
        Get face from frame of one tracking segment.
        
        :type segment_frame_dict: dictionary
        :param segment_frame_dict: frame containing face
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
            frame_path, eye_pos, offset_pct, dest_sz)
            
            if(face is not None):
                
                result = face
                
        else:
            
            # Else, we know only the bounding box
            bbox = segment_frame_dict[TRACKING_BBOX_KEY]
            
            x0 = bbox[0]
            x1 = x0 + bbox[2]
            y0 = bbox[1]
            y1 = y0 + bbox[3]
            
            tracked_face = image[y0:y1, x0:x1]
            
            cv2.imwrite(TMP_TRACKED_FACE_FILE_PATH, tracked_face)

            crop_result = fd.get_cropped_face(
            TMP_TRACKED_FACE_FILE_PATH, offset_pct, dest_sz, False)
            
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
                
                file_name = '%07d.bmp' % image_counter
                
                face_path = os.path.join(segment_path, file_name)
                
                cv2.imwrite(face_path, image)
                
                image_counter = image_counter + 1
                
                face_counter = face_counter + 1
                
            segment_counter = segment_counter + 1  
 
 
    def saveRecPeople(self):
        '''
        Save frames for recognized people on disk.
        A folder contains the segments from one person
        '''  
        
        print '\n\n### Saving recognized people ###\n'
               
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)        
        
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR)
        
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
        Show one image for each recognized people in video
        '''         
        
        p_counter = 1
        
        for person_dict in self.recognized_faces:
            
            person_dict[ANN_TAG_KEY] = UNDEFINED_TAG
            
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
                    
                    w_name = WINDOW_PERSON + ' ' + str(p_counter)
                    
                    cv2.imshow(w_name, image)
                    
                    cv2.waitKey(3)
                    
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

    def calcHistDiff(self):
        '''
        Calculate histogram differences between consecutive frames
        '''
        
        print '\n\n### Calculating histogram differences ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 

        # List with histogram differences (all frames)
        self.hist_diffs = []
        
        prev_hists = None
        
        counter = 0
        
        # Iterate through all frames
        for frame_dict in self.frame_list:
            
            self.progress = 100 * (counter / self.video_frames)
    
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
            
            # Calculate size of sliding window
            half_w_size = int(
            math.floor(self.fps * MIN_SEGMENT_DURATION / 2)) 
            
            # If a reduced bitrate is used, sliding window is smaller
            if(not(USE_ORIGINAL_FPS)):
                
                half_w_size = int(math.floor(
                self.fps * USED_FPS * MIN_SEGMENT_DURATION / 2))
            
            self.cut_idxs = get_shot_changes(
            self.hist_diffs, half_w_size, STD_MULTIPLIER_FRAME)    
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for calculation of histogram differences:', time_in_seconds, 's\n'              
                    
    
    def calcHistDiff_old(self):
        '''
        Calculate histogram differences between consecutive frames
        with faces and calculate threshold for tracking interruption
        '''
        
        print '\n\n### Calculating histogram differences ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 
        
        # List with histogram differences (only calculated values)
        diff_list = []
        
        # List with histogram differences (all frames)
        self.hist_diffs = []
        
        prev_hists = None
        
        counter = 0
        
        # Iterate through frames in detected_faces
        for detection_dict in self.detected_faces:
            
            self.progress = 100 * (counter / self.video_frames)
    
            print('progress: ' + str(self.progress) + ' %          \r'),
            
            tot_diff = -1
            
            faces = detection_dict[FACES_KEY]
            
            # Get number of faces in frame
            faces_nr = len(faces)
        
            #Calculate histograms only if there are faces in frame
            if(faces_nr >= 1):
                
                frame_path = detection_dict[FRAME_PATH_KEY]
                
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                
                [tot_diff, prev_hists] = get_hist_difference(
                image, prev_hists)
                
                if(tot_diff is not None):
                        
                    diff_list.append(tot_diff)
                
            else:
                
                # Calculate differences only between frames with faces
                prev_hists = None
                
            self.hist_diffs.append(tot_diff)
            
            counter = counter + 1
                
        # Calculate threshold
        #print 'diff_list', diff_list
        
        if(len(diff_list) > 0):
            
            use_fixed_threshold = True
        
            if(use_fixed_threshold):
            
                mean = np.mean(diff_list)
                
                std = np.std(diff_list)
                
                threshold = mean + STD_MULTIPLIER * std
                
                # If standard deviation is less than mean, 
                # there is only one shot in video
                
                if(std > mean):
                    
                    self.track_threshold = threshold
                
            else:
                
                # Minimum duration of a shot in frames
                min_shot_frames = int(
                math.ceil(self.fps * MIN_SHOT_DURATION))
                
                self.cut_idxs = get_shot_changes(
                diff_list, 0, min_shot_frames)    
            
        else:
            
            print 'No consecutive frames with faces in video'
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for calculation of histogram differences:', time_in_seconds, 's\n'              
            
    
    def savePeopleFiles(self): 
        '''
        Save annotation files for people in this video
        '''     
            
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
        simple_ann_path = os.path.join(video_path, FACE_ANNOTATION_DIR)
        
        # Delete already saved files
        if(os.path.exists(simple_ann_path)):
            
            ann_files = os.listdir(simple_ann_path)
            
            for ann_file in ann_files:
                
                ann_file_path = os.path.join(ann_path, ann_file)
                os.remove(ann_file_path)  
                
        else:
            
            os.makedirs(simple_ann_path)              
            
        # Iterate through all people in video
    
        for person_dict in self.recognized_faces:
            
            ann_tag = person_dict[ANN_TAG_KEY]
            
            file_name = ann_tag + '.YAML'
            
            # Save complete annotations
            
            file_path = os.path.join(compl_ann_path, file_name)
            
            save_YAML_file(file_path, person_dict)
            
            # Create and save simple annotations
            simple_dict = {}
            
            simple_dict[ANN_TAG_KEY] = ann_tag
            
            video_duration = person_dict[VIDEO_DURATION_KEY]
            
            simple_dict[VIDEO_DURATION_KEY] = video_duration
            
            segment_list = person_dict[SEGMENTS_KEY]
            
            simple_segment_list = []
            
            for segment_dict in segment_list:
                
                simple_segment_dict = {}
                
                start = segment_dict[SEGMENT_START_KEY]
                
                simple_segment_dict[SEGMENT_START_KEY] = start
                
                duration = segment_dict[SEGMENT_DURATION_KEY]
                
                simple_segment_dict[SEGMENT_DURATION_KEY] = duration
                
                simple_segment_list.append(simple_segment_dict)
                
            simple_dict[SEGMENTS_KEY] = simple_segment_list
            
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
            
            half_w_size = int(
            math.floor(self.fps * MIN_SEGMENT_DURATION / 2)) 
            
            face_cut_idxs_temp = get_shot_changes(
            det_diff_list, half_w_size, STD_MULTIPLIER_FACE) 
            
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
            
        # Iterate through new sub segments
        for sub_frame_list in sub_segment_list:
            
            frame_counter = len(sub_frame_list)
            
            segment_dict = {}
        
            segment_dict[FRAMES_KEY] = sub_frame_list
        
            segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = frame_counter         
        
            # Segment duration in milliseconds
            duration = frame_counter * 1000.0 / self.fps
        
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



    def divideSegmentByFace_old(self, segment_frame_list):
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
                    
                else:
                    
                    diff_list.append(-1)
            
            else:
                
                diff_list.append(-1)
        
        segment_divided = False
                    
        if(len(det_diff_list) > 0):
            
            use_fixed_threshold = True
        
            if(use_fixed_threshold):
            
                mean = np.mean(det_diff_list)
                
                std = np.std(det_diff_list)
                
                print('mean', mean)
                
                print('std', std)
                
                plt.plot(diff_list)
                plt.show() 
                
                # If standard deviation is less than mean, 
                # there is only one shot in video
                
                if(std > mean):
                    
                    segment_divided = True
                    
                    threshold = mean + STD_MULTIPLIER * std
                    
                    # Counter for all frames in original segment
                    counter = 0
                    
                    # Counter for all frames in new segment
                    sub_counter = 0
                    
                    # Counter for frames with detections in new segment
                    det_counter = 0
                    
                    sub_frame_list = []
                    
                    for frame_dict in segment_frame_list:
                        
                        diff = diff_list[counter]
                        
                        if(diff > threshold):
                            
                            sub_segment_list.append(sub_frame_list)
                            
                            sub_frame_list = []
                            
                            sub_counter = 0
                            
                        sub_frame_list.append(frame_dict)
                        
                        sub_counter = sub_counter + 1
                        
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
            
        # Iterate through new sub segments
        for sub_frame_list in sub_segment_list:
            
            frame_counter = len(sub_frame_list)
            
            segment_dict = {}
        
            segment_dict[FRAMES_KEY] = sub_frame_list
        
            segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = frame_counter
        
            # Segment duration in milliseconds
            duration = frame_counter * 1000.0 / self.fps
        
            segment_dict[SEGMENT_DURATION_KEY] = duration
        
            segment_dict[ASSIGNED_TAG_KEY] = 'Undefined'
        
            segment_dict[CONFIDENCE_KEY] = -1
            
            # Segment must be considered only if its number 
            # of frames is greater or equals than a minimum
            if(frame_counter >= min_segment_frames):
                
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
