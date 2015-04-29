import copy

import cv2

import cv2.cv as cv

import face_detection as fd

import yaml

import math

import numpy as np

import operator

import os

import pickle as pk

import shutil

import sys

from caption_recognition import get_tag_from_image

from Constants import *

from Utils import aggregate_frame_results, compare_clothes, get_dominant_color, get_hist_difference, get_mean_intra_distance, get_shot_changes, is_rect_similar, load_YAML_file, merge_consecutive_segments, save_YAML_file

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
        
        self.anal_results = {} # Dictionary with analysis results
        
        self.anal_times = {} # Dictionary with times for analysis
        
        self.cloth_threshold = 0 # Threshold for clothing recognition
        
        self.cut_idxs = [] # List of frame indexes where new shots begin
        
        self.detected_faces = [] # List of detected faces 
        
        # List of tracked faces not considered
        self.disc_tracked_faces = [] 
        
        self.faces_nr = {} # Number of faces for each frame
        
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
        
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
        
        # Check if a file with parameters of this video exists   
        video_path = os.path.join(video_indexing_path, res_name)
        
        file_name = res_name + '_parameters.YAML'
        
        file_path = os.path.join(video_path, file_name)
        
        if(self.params is not None):
            
            if(VIDEO_PARAMS_FILE_PATH_KEY in self.params):
                
                file_path = self.params[VIDEO_PARAMS_FILE_PATH_KEY]
        
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
        
        sim_user_ann = SIMULATE_USER_ANNOTATIONS
        
        if(self.params is not None):
            
            sim_user_ann = self.params[SIMULATE_USER_ANNOTATIONS_KEY]
            
        if(not(sim_user_ann)):
            
            self.getFrameList(resource)
            
            self.detectFacesInVideo()       
            
            self.trackFacesInVideo()
        
        #self.saveTrackingSegments() # TEST ONLY
        
        #self.saveDiscTrackingSegments() # TEST ONLY
        
        use_people_clustering = USE_PEOPLE_CLUSTERING
        
        if(self.params is not None):
            
            use_people_clustering = self.params[USE_PEOPLE_CLUSTERING_KEY]
        
        if(use_people_clustering):    
            
            self.clusterFacesInVideo()
    
            #self.saveRecPeople(True) # TEST ONLY
            
            ### TO BE DELETED ###
            #use_clothing_rec = USE_CLOTHING_RECOGNITION
            
            #if(self.params is not None):
            
                #use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
            
            #if(use_clothing_rec):
            
                #self.recognizeClothesInVideo()
                
                #self.saveRecPeople(False) # TEST ONLY
                
            #####################
            
            self.saveTempPeopleFiles()
            
            self.showRecPeople()
            
            #self.recognizeFacesInVideo()
            
            if(sim_user_ann):
            
                self.simulateUserAnnotations()
            
            else:
                
                self.readUserAnnotations()
            
            self.savePeopleFiles()
            
        else:
            
            self.showTrackedPeople()
            
            self.readTrackUserAnnotations()
            
        self.saveAnalysisResults()
        
        
    def detectFacesInVideo(self):
        '''
        Detect faces on analyzed video.
        It works by using list of extracted frames
        '''
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        use_eyes_position = USE_EYES_POSITION
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            use_eyes_position = self.params[USE_EYES_POSITION_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
                frame_path, align_path, self.params, False)
    
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
                        
                        if(use_eyes_position):
                        
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
                        
                    used_fps = USED_FPS    
                    use_or_fps = USE_ORIGINAL_FPS
                    use_or_res = USE_ORIGINAL_RES
                    used_res_scale_factor = USED_RES_SCALE_FACTOR
                    
                    if(self.params is not None):
                        
                        used_fps = self.params[USED_FPS_KEY]
                        use_or_fps = self.params[USE_ORIGINAL_FPS_KEY]
                        use_or_res = self.params[USE_ORIGINAL_RES_KEY]
                        used_res_scale_factor = self.params[USED_RES_SCALE_FACTOR_KEY]
                    
                    # Next frame to be analyzed
                    next_frame = last_anal_frame + (video_fps/(used_fps+1))
                    
                    if(use_or_fps or (frame_counter > next_frame)):
                    
                        # Frame position in video in milliseconds
                        elapsed_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                        
                        #print 'elapsed video s =', elapsed_video_s             
                        
                        fr_name = '%07d.png' % frame_counter
                        
                        frame_path = os.path.join(frames_path, fr_name)
                        
                        # Resize frame
                        if(not(use_or_res)):
                            
                            fx = used_res_scale_factor
                            
                            fy = used_res_scale_factor
                            
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
    
            del(capture)
            
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


    def getFacesNr(self):
        '''
        Get number of faces in each frame
        It works by using list of tracked faces
        '''
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        if(len(self.tracked_faces) == 0):
            
            # Try to load YAML file
            track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
            
            file_name = res_name + '.YAML'
                
            file_path = os.path.join(track_path, file_name)
            
            if(os.path.exists(file_path)):
                
                print 'Loading YAML file with tracking results'
                
                with open(file_path) as f:
    
                    self.tracked_faces = yaml.load(f) 
                    
                print 'YAML file with tracking results loaded'
                    
            else:
                
                print 'Warning! No tracking results found!'
                
                return  
                
        self.faces_nr = {}
        
        for segment_dict in self.tracked_faces:
            
            frame_list = segment_dict[FRAMES_KEY]
            
            for frame_dict in frame_list:
            
                frame_path = frame_dict[FRAME_PATH_KEY]
            
                if(frame_path in self.faces_nr):
                
                    self.faces_nr[frame_path] = self.faces_nr[frame_path] + 1
                
                else:
                
                    self.faces_nr[frame_path] = 1 
                    
        # Save YAML file
        faces_nr_path = os.path.join(video_path, FACES_NR_IN_FRAMES_FILE)
        
        save_YAML_file(faces_nr_path, self.faces_nr)
    
    
    def trackFacesInVideo(self):
        '''
        Track faces on analyzed video.
        It works by using list of detected faces
        '''
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
            
            # If a reduced bitrate is used, frames are less
            use_or_fps = USE_ORIGINAL_FPS
            used_fps = USED_FPS
            min_segment_duration = MIN_SEGMENT_DURATION
            tracking_min_int_area = TRACKING_MIN_INT_AREA
            min_size_width = FACE_DETECTION_MIN_SIZE_WIDTH
            min_size_height = FACE_DETECTION_MIN_SIZE_HEIGHT
            max_fr_with_miss_det = MAX_FR_WITH_MISSED_DET
            
            if(self.params is not None):
                
                use_or_fps = self.params[USE_ORIGINAL_FPS_KEY]
                used_fps = self.params[USED_FPS_KEY]
                min_segment_duration = self.params[MIN_SEGMENT_DURATION_KEY]
                tracking_min_int_area = self.params[TRACKING_MIN_INT_AREA_KEY]
                min_size_width = self.params[MIN_SIZE_WIDTH_KEY]
                min_size_height = self.params[MIN_SIZE_HEIGHT_KEY]
                max_fr_with_miss_det = self.params[MAX_FR_WITH_MISSED_DET_KEY]
            
            # Minimum duration of a segment in frames
            min_segment_frames = int(
            math.ceil(self.fps * min_segment_duration))
            
            if(not(use_or_fps)):
                
                min_segment_frames = int(
                math.ceil((used_fps+1) * min_segment_duration))
            
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
                
                if(image is None):
                    
                    print('Warning! Image is None (1)')
                    
                    frame_counter = frame_counter + 1
                    
                    continue
                
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
                            
                            #print('new shot begins', sub_frame_counter)
                                
                            break
                
                        sub_frame_path = sub_det_dict[FRAME_PATH_KEY]
                    
                        # Read image from given path
                        sub_image = cv2.imread(
                        sub_frame_path, cv2.IMREAD_COLOR)

                        if(sub_image is None):
                            
                            print('Warning! Image is None (2)')
                            
                            continue
                        
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
                        
                        # TEST ONLY
                        #cv2.rectangle(
                        #sub_image, (track_x0, track_y0), (track_x1, track_y1), (0, 0, 255), 3, 8, 0)
                        
                        #cv2.imshow('tracking', sub_image)
                        #cv2.waitKey(0)
                        
                        # Check size of track window
                        if((track_w <= min_size_width) 
                        or (track_h <= min_size_height)):   
                            
                            #print('Track window too small', sub_frame_counter)                 

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
                            track_window, det_bbox, tracking_min_int_area)
                            
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
                            
                            if(missed_det_counter > max_fr_with_miss_det):
                                
                                # Remove last frames and 
                                # interrupt tracking
                                for i in range(0, max_fr_with_miss_det):
                                
                                    segment_frame_list.pop()
                                    
                                segment_face_counter = (
                                segment_face_counter - max_fr_with_miss_det)
                                
                                #print('Too many missed detections', sub_frame_counter)
                                
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
                        
                        del(sub_image)
                        
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
                    
                del(image)
                
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
            
    
    
    def createClothModel(self, segment_dict):
        '''
        Create cloth model of one tracked face.
        
        :type segment_dict: dictionary
        :param segment_dict: video segment relative to tracked face
        '''
    
        # List of color histograms
        model = []
        
        # Extract list of frames from dictionary
        frame_list = segment_dict[FRAMES_KEY]
        
        cl_pct_height = CLOTHES_BBOX_HEIGHT
        cl_pct_width = CLOTHES_BBOX_WIDTH
        neck_pct_height = NECK_HEIGHT
        use_dom_color = CLOTHING_REC_USE_DOMINANT_COLOR
        use_mean_x = CLOTHING_REC_USE_MEAN_X_OF_FACES
        use_3_bboxes = CLOTHING_REC_USE_3_BBOXES
        kernel_size = HIST_SMOOTHING_KERNEL_SIZE
        
        if(self.params is not None):
            
            cl_pct_height = self.params[CLOTHES_BBOX_HEIGHT_KEY]
            cl_pct_width = self.params[CLOTHES_BBOX_WIDTH_KEY]
            neck_pct_height = self.params[NECK_HEIGHT_KEY]
            use_dom_color = self.params[CLOTHING_REC_USE_DOMINANT_COLOR_KEY]
            use_mean_x = self.params[CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]
            use_3_bboxes = self.params[CLOTHING_REC_USE_3_BBOXES_KEY]
            kernel_size = self.params[HIST_SMOOTHING_KERNEL_SIZE_KEY]
        
        min_x = sys.maxint
        max_x = 0
        mean_x = 0
        if(use_mean_x):
            
            # Calculate mean position of face in x axis
            for frame_dict in frame_list:
                
                detected = frame_dict[DETECTED_KEY]
                
                if(detected):
                    
                    face_bbox = frame_dict[DETECTION_BBOX_KEY]
                    face_x = face_bbox[0]
                    
                    if(face_x < min_x):
                        
                        min_x = face_x
                        
                    if(face_x > max_x):
                        
                        max_x = face_x
                        
            mean_x = int((max_x + min_x)/2.0)
        
        for frame_dict in frame_list:
            
            detected = frame_dict[DETECTED_KEY]
            
            # Consider only detected faces
            if(detected):

                frame_path = frame_dict[FRAME_PATH_KEY]
                
                face_bbox = frame_dict[DETECTION_BBOX_KEY]
                            
                face_x = face_bbox[0]
                face_y = face_bbox[1]
                face_width = face_bbox[2]
                face_height = face_bbox[3]
                
                #x0 = face_bbox[0]
                #x1 = x0 + face_bbox[2]
                #y0 = face_bbox[1] + face_bbox[3]
                #y1 = y0 + face_bbox[3]
                
                if(use_3_bboxes):
                    
                    frame_hists = []
                    
                    im = cv2.imread(frame_path)
                    
                    for i in range(0,3):
                        
                        # Get region of interest for clothes
                        clothes_width = int(
                        (face_width * cl_pct_width) / 3.0)
                        clothes_height = int(face_height * cl_pct_height)
                        
                        # Leftmost bounding box for clothes
                        clothes_x0 = int(face_x + face_width/2.0 - 1.5*clothes_width)
                        
                        # OLD IMPLEMENTATION
                        # (final distance between two frames is the distance 
                        # between the two nearest bounding boxes)
                        #if(i == 0):
                            ## Leftmost bounding box for clothes
                            #clothes_x0 = int(face_x - clothes_width/2.0)
                            
                        #elif(i == 1):
                            ## Central bounding box for clothes
                            #clothes_x0 = int(face_x + face_width/2.0 - clothes_width/2.0)
                            
                        #elif(i == 2):
                            ## Rightmost bounding box for clothes
                            #clothes_x0 = int(face_x + face_width - clothes_width/2.0)
                            
                        if(i == 1):
                            # Central bounding box for clothes
                            clothes_x0 = clothes_x0 +  clothes_width
                            
                        elif(i == 2):
                            # Rightmost bounding box for clothes
                            clothes_x0 = clothes_x0 + 2 * clothes_width                          
                            
                        clothes_y0 = int(
                        face_y + face_height + (face_height * neck_pct_height))
                        clothes_x1 = clothes_x0 + clothes_width
                        clothes_y1 = clothes_y0 + clothes_height
                        
                        # Bounding box cannot start out of image
                        if(clothes_x0 < 0):
                            clothes_x0 = 0
                        
                        roi = im[clothes_y0:clothes_y1, clothes_x0:clothes_x1]
                        
                        #cv2.rectangle(im, (clothes_x0, clothes_y0), (clothes_x0+clothes_width, clothes_y0+clothes_height), (255,255,255))
                        
                        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
                        hists = []
                        
                        if(use_dom_color):
                            
                            mask = get_dominant_color(roi_hsv, kernel_size)
                            
                        else:
                            
                            mask = cv2.inRange(roi_hsv, 
                            np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                    
                        for ch in range(0, 3):
                    
                            hist = cv2.calcHist(
                            [roi_hsv], [ch], mask, [256], [0, 255])
                    
                            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                            
                            #hist.reshape(-1)
                            
                            hists.append(hist)
                                
                        frame_hists.append(hists)
                        
                    #cv2.imshow('Image', im)
                        #cv2.imshow('Clothes', roi)
                    #cv2.waitKey(0)
                    
                    model.append(frame_hists)
                    
                    del(im)
                    
                else:
                
                    # Get region of interest for clothes
                    clothes_width = int(face_width * cl_pct_width)
                    clothes_height = int(face_height * cl_pct_height)
                    clothes_x0 = int(face_x + face_width/2.0 - clothes_width/2.0)
                    
                    if(use_mean_x):
                        
                        # Bounding box for clothes 
                        # has fixed position in x axis
                        clothes_x0 = int(mean_x + face_width/2.0 - clothes_width/2.0)
                        
                    clothes_y0 = int(
                    face_y + face_height + (face_height * neck_pct_height))
                    clothes_x1 = clothes_x0 + clothes_width
                    clothes_y1 = clothes_y0 + clothes_height
                    
                    # Bounding box cannot start out of image
                    if(clothes_x0 < 0):
                        clothes_x0 = 0
                    
                    im = cv2.imread(frame_path)
                    
                    roi = im[clothes_y0:clothes_y1, clothes_x0:clothes_x1]
                    #cv2.imshow('Clothes', roi)
                    #cv2.waitKey(0)
                    
                    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
                    hists = []
                    
                    if(use_dom_color):
                        
                        mask = get_dominant_color(roi_hsv, kernel_size)
                        
                    else:
                        
                        mask = cv2.inRange(roi_hsv, 
                        np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                
                    for ch in range(0, 3):
                
                        #hist = cv2.calcHist(
                        #[roi_hsv], [ch], mask, [16], [0, 255])
                        
                        hist = cv2.calcHist(
                        [roi_hsv], [ch], mask, [256], [0, 255])
                
                        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                        
                        #hist.reshape(-1)
                        
                        hists.append(hist)
                            
                    model.append(hists)
                    
                    del(im)
                
        return model
        
        
    
    def createClothModel_old(self, person_dict):
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
        frame_list = segment_dict[FRAMES_KEY]
        
        c = 0
        X, y = [], [] 

        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        use_nose_pos_in_rec = USE_NOSE_POS_IN_RECOGNITION
        
        max_faces_in_model = MAX_FACES_IN_MODEL
        
        algorithm = FACE_MODEL_ALGORITHM
        
        lbp_radius = LBP_RADIUS      
        lbp_neighbors = LBP_NEIGHBORS     
        lbp_grid_x = LBP_GRID_X
        lbp_grid_y = LBP_GRID_Y
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            
            use_nose_pos_in_rec = self.params[USE_NOSE_POS_IN_RECOGNITION_KEY]
            max_faces_in_model = self.params [MAX_FACES_IN_MODEL_KEY]
           
            algorithm = self.params[FACE_MODEL_ALGORITHM_KEY]
           
            lbp_radius = self.params[LBP_RADIUS_KEY]
            lbp_neighbors = self.params[LBP_NEIGHBORS_KEY]
            lbp_grid_x = self.params[LBP_GRID_X_KEY]
            lbp_grid_y = self.params[LBP_GRID_Y_KEY]        
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        # Directory for recognition results
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 
        
        align_path = os.path.join(rec_path, ALIGNED_FACES_DIR)   
 
        if(not(os.path.exists(align_path))):
                
            # Create directory with aligned faces 
            
            os.makedirs(align_path) 
        
        # Iterate through list of frames
        face_counter = 0
        segment_nose_pos_dict = {}
        for frame_dict in frame_list:
            
            face = self.getFaceFromSegmentFrame(frame_dict, align_path)
            
            if(face is not None):
                
                #cv2.imshow('face', face)
                #cv2.waitKey(0)
                X.append(np.asarray(face, dtype = np.uint8))
                y.append(c)
                
                if(use_nose_pos_in_rec):  
                    
                    # Save nose position in segment dictionary
                    nose_pos = frame_dict[NOSE_POSITION_KEY]
                    segment_nose_pos_dict[c] = nose_pos
                    
                face_counter = face_counter + 1
                c = c + 1
            
            # If maximum number of faces is reached, stop adding them
            if(face_counter >= max_faces_in_model):
                
                print 'Warning! Maximum number of faces in model reached'
                break               
             
        model = None
        
        if(algorithm == 'Eigenfaces'):
            
            model = cv2.createEigenFaceRecognizer()
        
        elif(algorithm == 'Fisherfaces'):
            
            model = cv2.createFisherFaceRecognizer()
            
        elif(algorithm == 'LBP'):
            
            model = cv2.createLBPHFaceRecognizer(
            lbp_radius, lbp_neighbors, lbp_grid_x, lbp_grid_y)
        
        model.train(np.asarray(X), np.asarray(y))
        
        if(use_nose_pos_in_rec):
        
            # Save nose positions for this segment in dictionary
            self.nose_pos_list.append(segment_nose_pos_dict)
        
        return model
        
        
    
    def saveClothModels(self, segments):
        '''
        Save cloth models for each tracked face
        
        :type segments: list
        :param segments: list of segments
        '''
        
        print '\n\n### Creating cloth models ###\n'
        
        # Save processing time
        start_time = cv2.getTickCount() 

        res_name = self.resource_name
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        # Directory for cloth models
        models_path = os.path.join(video_path, CLOTH_MODELS_DIR)
        
        if(not(os.path.exists(models_path))):
                
            os.makedirs(models_path) 
        
        counter = 0
        
        for segment_dict in segments:
            
            model = self.createClothModel(segment_dict)
            
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



    def saveClothModels_old(self, people):
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
            
        # Save nose positions
        nose_pos_file_path = os.path.join(video_path, 'noses')
        with open(nose_pos_file_path, 'w') as f:
                
            pk.dump(self.nose_pos_list, f)                
            
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
        print 'Time for calculating face models:', str(time_in_seconds), 's\n'    
            
        self.anal_times[FACE_MODELS_CREATION_TIME_KEY] = time_in_seconds
        
        anal_file_name = res_name + '_anal_times.YAML'
        
        anal_file_path = os.path.join(video_path, anal_file_name)
        
        save_YAML_file(anal_file_path, self.anal_times)
                
            
    def searchClothes_old(self, ann_people, segment_list, train_model, idx):
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
        Search tracked faces that are similar to face in model.
        Segments to be checked are treated indipendently:
        a new segment is merged with reference segment 
        if final confidence is below a fixed threshold.
        
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if((self.params is not None) and 
        (VIDEO_INDEXING_PATH_KEY in self.params)):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        use_aggregation = USE_AGGREGATION
        use_nose_pos_in_rec = USE_NOSE_POS_IN_RECOGNITION
        max_nose_diff = MAX_NOSE_DIFF
        conf_threshold = CONF_THRESHOLD
        
        use_clothing_rec = USE_CLOTHING_RECOGNITION
        
        use_3_bboxes = CLOTHING_REC_USE_3_BBOXES

        # Threshold for using clothing recognition
        clothes_conf_th = CLOTHES_CONF_THRESH
        
        # Directory for face models
        face_models_path = os.path.join(video_path, FACE_MODELS_DIR)
        
        # Directory for cloth models
        cloth_models_path = os.path.join(video_path, CLOTH_MODELS_DIR)
        
        if(self.params is not None):
        
            if(USE_AGGREGATION_KEY in self.params):
                use_aggregation = self.params[USE_AGGREGATION_KEY]
            
            if(USE_NOSE_POS_IN_RECOGNITION_KEY in self.params):
                use_nose_pos_in_rec = (
                self.params[USE_NOSE_POS_IN_RECOGNITION_KEY])
            
            if(MAX_NOSE_DIFF_KEY in self.params):
                max_nose_diff = self.params[MAX_NOSE_DIFF_KEY]
            
            if(CONF_THRESHOLD_KEY in self.params):
                conf_threshold = self.params[CONF_THRESHOLD_KEY]
            
            if(USE_CLOTHING_RECOGNITION_KEY in self.params):
                use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
                
            if(CLOTHING_REC_USE_3_BBOXES_KEY in self.params):   
                use_3_bboxes = self.params[CLOTHING_REC_USE_3_BBOXES_KEY]
            
            if(FACE_MODELS_DIR_PATH_KEY in self.params):
                
                face_models_path = self.params[FACE_MODELS_DIR_PATH_KEY]
            
            if(CLOTH_MODELS_DIR_PATH_KEY in self.params):
                
                cloth_models_path = self.params[CLOTH_MODELS_DIR_PATH_KEY]
                
            if(CLOTHES_CONF_THRESH_KEY in self.params):
                
                clothes_conf_th = self.params[CLOTHES_CONF_THRESH_KEY]

        # Get histograms from model
        
        train_hists = train_model.getMatVector("histograms")
        
        # Get labels from model
        
        train_labels = train_model.getMat("labels")
        
        intra_dist1 = None
        
        if(use_clothing_rec):
            
            # Get models for clothing recognition
            db_path_1= os.path.join(cloth_models_path, str(idx))
            
            if(os.path.isfile(db_path_1)):
        
                model1 = None
                model2 = None
        
                with open(db_path_1, 'r') as f1:
        
                    model1 = pk.load(f1) 
        
                    if(model1): 
                        
                        intra_dist1 = get_mean_intra_distance(
                        model1, use_3_bboxes)           

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
                
                db_path= os.path.join(face_models_path, str(sub_counter))
                        
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
                        
                        if(use_aggregation):
                            
                            frames =  []
                            
                            for i in range(0,len(model_hists)):
                    
                                hist = model_hists[i][0]
                                
                                label = model_labels[i][0]
                                
                                nose_pos = None
                                
                                if(use_nose_pos_in_rec):
                                    
                                    nose_pos = (
                                    self.nose_pos_list[sub_counter][label])
                                
                                # Confidence value
                                conf = sys.maxint
                        
                                # Iterate through LBP histograms 
                                # in training model
                                for t in range(0, len(train_hists)):
                                    
                                    train_hist = train_hists[t][0]
                                    
                                    train_label = train_labels[t][0]
                                    
                                    if(use_nose_pos_in_rec):
                                        
                                        # Compare only faces with
                                        # similar nose position
                                        
                                        train_nose_pos = (
                                        self.nose_pos_list[idx][train_label])                                        
                                        
                                        if((nose_pos is None) or
                                        (train_nose_pos is None)):
                                            
                                            continue
                                            
                                        nose_diff_x = (
                                        abs(nose_pos[0] - train_nose_pos[0]))
                                        
                                        nose_diff_y = (
                                        abs(nose_pos[1] - train_nose_pos[1]))
                                        
                                        if((nose_diff_x > max_nose_diff)
                                        or (nose_diff_y > max_nose_diff)):
                                            
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
                                
                                if(conf < conf_threshold):
                                    
                                    ass_tag = TRACKED_PERSON_TAG
                                    
                                frame_dict[ASSIGNED_TAG_KEY] = ass_tag
                                
                                frames.append(frame_dict)
                        
                            tgs = (TRACKED_PERSON_TAG, UNDEFINED_TAG)
                            
                            [final_tag, final_conf, pct] = (
                            aggregate_frame_results(
                            frames, tags = tgs, params = self.params))
                            
                            #print('train index', idx)
                            #print('query index', sub_counter)
                            #print('final_tag', final_tag)
                            #print('confidence', final_conf)
                            #print('number of frames', len(frames))
                            #print('Percentage', pct)
                            #print('\n')
                            #raw_input('Aspetta poco poco ...') 
                            
                        else:
                            
                            for i in range(0,len(model_hists)):
                    
                                hist = model_hists[i][0]
                                
                                label = model_labels[i][0]
                                
                                nose_pos = None
                                
                                if(use_nose_pos_in_rec):
                                    
                                    nose_pos = (
                                    self.nose_pos_list[sub_counter][label])                                
                        
                                # Iterate through LBP histograms in training model
                                for t in range(0, len(train_hists)):
                                    
                                    train_hist = train_hists[t][0]
                                    
                                    train_label = train_labels[t][0]
                                    
                                    if(use_nose_pos_in_rec):
                                        
                                        # Compare only faces with
                                        # similar nose position
                                        
                                        train_nose_pos = (
                                        self.nose_pos_list[idx][train_label])                                        
                                        
                                        if((nose_pos is None) or
                                        (train_nose_pos is None)):
                                            
                                            continue
                                            
                                        nose_diff_x = (
                                        abs(nose_pos[0] - train_nose_pos[0]))
                                        
                                        nose_diff_y = (
                                        abs(nose_pos[1] - train_nose_pos[1]))
                                        
                                        if((nose_diff_x > max_nose_diff)
                                        or (nose_diff_y > max_nose_diff)):
                                            
                                            continue
                                                                           
                                    diff = cv2.compareHist(
                                    hist, train_hist, cv.CV_COMP_CHISQR)
                                    
                                    if(diff < final_conf):
                                        
                                        final_conf = diff                        
                        
                            if(final_conf < conf_threshold):
                                
                                if(use_clothing_rec):
                                
                                    # If final confidence is very low
                                    # do not use clothing recognition
                                    if(final_conf < clothes_conf_th):
                                        
                                        final_tag = TRACKED_PERSON_TAG
                                        
                                    else:
                                    
                                        # Check clothing similarity
    
                                        #print('idx', idx)
                                        #print('sub_counter', sub_counter)
                                        #print('final_conf', final_conf)
                                        #print('clothes_conf_th', clothes_conf_th)
                                        #print('conf_threshold', conf_threshold)
                                        #raw_input('Aspetta poco poco ...')   
                                        
                                        db_path_2 = os.path.join(
                                        cloth_models_path, str(sub_counter))
    
                                        similar = compare_clothes(db_path_1, 
                                        db_path_2, final_conf,
                                        intra_dist1, self.params)
                        
                                        if(similar):
                                
                                            final_tag = TRACKED_PERSON_TAG
                                    
                                else:
                                    
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


    def searchFaceWithUpdating(
    self, ann_segments, segment_list, train_hists, train_labels, idx):
        '''        
        Search tracked faces that are similar to face in model.
        Reference segment is merged with more similar segment.
        After each merging, reference segment is updated
        
        :type ann_segments: list
        :param ann_segments: list of already checked segments
        
        :type segment_list: list
        :param segment_list: list of segments related to the same person
        
        :type train_hists: list
        :param train_hists: list of LBP histograms of searched face
        
        :type train_labels: list
        :param train_labels: list of model labels of searched face     
        
        :type idx: int
        :param idx: index of segment used for creating model
        '''

        res_name = self.resource_name

        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        # Directory for face models
        models_path = os.path.join(video_path, FACE_MODELS_DIR)

        if(self.params is not None):
            
            if(FACE_MODELS_DIR_PATH_KEY in self.params):
                
                models_path = self.params[FACE_MODELS_DIR_PATH_KEY] 

        # Save a list of confidence values for each hist in train model
        conf_list_list = []
        
        for t in range(0, len(train_hists)):
            
            # Create a list for each hist in train model
            # and initialize it with sys.maxint
            conf_list = []
            
            for s in range(0, len(self.tracked_faces)):
                
                conf_list.append(sys.maxint)
                
            conf_list_list.append(conf_list)
            
        use_nose_pos_in_rec = USE_NOSE_POS_IN_RECOGNITION
        max_nose_diff = MAX_NOSE_DIFF
        conf_threshold = CONF_THRESHOLD
        
        if(self.params is not None):
            
            use_nose_pos_in_rec = (
            self.params[USE_NOSE_POS_IN_RECOGNITION_KEY])
            max_nose_diff = self.params[MAX_NOSE_DIFF_KEY]
            conf_threshold = self.params[CONF_THRESHOLD_KEY]              

        there_are_good_segments = False

        tgs = [] # List of tags
        sub_counter = 0
        print('len tracked', len(self.tracked_faces))
        for sub_segment_dict in self.tracked_faces:
            
            tgs.append(sub_counter)
            
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
                        
                if(overlap_seg):
                    
                    sub_counter = sub_counter + 1
                    
                    continue
                
                db_path= os.path.join(models_path, str(sub_counter))
                        
                if(os.path.isfile(db_path)):
                    
                    model = cv2.createLBPHFaceRecognizer()
                    
                    model.load(db_path)
                
                    if(model):
                        
                        there_are_good_segments = True
                        
                        # Get histograms from model      
                        model_hists = model.getMatVector("histograms")
                        
                        # Get labels from model
                        model_labels = model.getMat("labels")
                        
                        # Iterate through models related to this segment                      
                        final_tag = UNDEFINED_TAG
                        
                        final_conf = sys.maxint    
                        
                        # Iterate through LBP histograms in training model
                        for t in range(0, len(train_hists)):
                            
                            train_hist = train_hists[t][0]
                            
                            train_label = train_labels[t][0]
                            
                            conf = sys.maxint
                            
                            train_nose_pos = None
                            
                            if(use_nose_pos_in_rec):
                                
                                # Compare only faces with
                                # similar nose position
                                                     
                                train_nose_pos = (
                                self.nose_pos_list[idx][train_label])
                                
                            for i in range(0,len(model_hists)):
                    
                                hist = model_hists[i][0]
                                
                                label = model_labels[i][0]
                                
                                nose_pos = None
                                
                                if(use_nose_pos_in_rec):
                                        
                                    nose_pos = (
                                    self.nose_pos_list[sub_counter][label])                                         
                                                                    
                                
                                    if((nose_pos is None) or
                                    (train_nose_pos is None)):
                                        
                                        continue
                                        
                                    nose_diff_x = (
                                    abs(nose_pos[0] - train_nose_pos[0]))
                                    
                                    nose_diff_y = (
                                    abs(nose_pos[1] - train_nose_pos[1]))
                                    
                                    if((nose_diff_x > max_nose_diff)
                                    or (nose_diff_y > max_nose_diff)):
                                        
                                        continue
                                                                   
                                diff = cv2.compareHist(
                                hist, train_hist, cv.CV_COMP_CHISQR)
                                
                                if(diff < conf):
                                    
                                    conf = diff
                            
                            conf_list_list[t][sub_counter] = conf
            
            sub_counter = sub_counter + 1
        
        # Assign final tags to frames              
        
        if(there_are_good_segments):
            #At least one segment has been checked
            frames = []
            
            #print('conf_list_list', conf_list_list)
            
            for t in range(0, len(train_hists)): 
                
                frame_dict = {}
                
                conf_list = conf_list_list[t]
                
                [assigned_tag, conf] = min(enumerate(conf_list), 
                key=operator.itemgetter(1))
                
                frame_dict[ASSIGNED_TAG_KEY] = assigned_tag
                frame_dict[CONFIDENCE_KEY] = conf
                
                frames.append(frame_dict)
                
            # Aggregate frame results             
            [final_tag, final_conf, pct] = (
            aggregate_frame_results(
            frames, tags = tgs, params = self.params))
            
            #print('idx', idx)
            
            #print('conf_list_list', conf_list_list)
            
            #print('frames', frames)
            
            #print('final_tag', final_tag)
            
            #print('final_conf', final_conf)
                
            new_segment_merged =  False   
                
            # There is a sufficiently similar segment
            if(final_conf < conf_threshold):
                
                new_segment_merged = True
                
                segment_dict = {}
                
                sub_segment_dict = self.tracked_faces[final_tag]
                
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
                ann_segments.append(final_tag)      
                         
                #print('sub_counter', sub_counter)                            
                sub_counter = sub_counter + 1
        
            #print('len(segment_list)', len(segment_list))
            
            #print('ann_segments', ann_segments)
            
            #raw_input("Press Enter to continue...")
            
            if(new_segment_merged):
                
                # Update reference segment
                db_path= os.path.join(models_path, str(final_tag))
                    
                model = cv2.createLBPHFaceRecognizer()
                
                model.load(db_path)
                
                if(model):  
                    
                    # Get histograms from model      
                    model_hists = model.getMatVector("histograms")
                    
                    # Get labels from model
                    model_labels = model.getMat("labels")
                    
                    # Update list of labels
                    train_hist_nr = len(train_hists)
                    for lbl in model_labels:
                        
                        new_lbl = lbl + train_hist_nr
                        
                        np.append(train_labels, new_lbl)
                        
                    # Update list of histograms
                    np.append(train_hists, model_hists)     
                    
                    # Update nose positions
                    if(use_nose_pos_in_rec):

                        new_segment_nose_pos = self.nose_pos_list[final_tag]
                        new_segment_keys = new_segment_nose_pos.keys()
                        
                        for new_segment_key in new_segment_keys:
                            
                            nose_pos = new_segment_nose_pos[new_segment_key]
                            new_key = new_segment_key + train_hist_nr
                            self.nose_pos_list[idx][new_key] = nose_pos
                    
                    ann_segments = self.searchFaceWithUpdating(ann_segments, 
                    segment_list, train_hists, train_labels, idx)             
    
        return ann_segments


    def recognizeClothesInVideo_old(self):
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
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
            
            self.anal_times[CLOTHING_RECOGNITION_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
    
    
    def clusterFacesInVideo(self):       
        '''
        Cluster faces on analyzed video,
        assigning a generic tag to each face.
        It works by using a list of tracked faces
        '''   
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        # Directory for clustering results
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR)  
        
        # Directory for face models
        face_models_path = os.path.join(video_path, FACE_MODELS_DIR)
        
        if(self.params is not None):
            
            if(FACE_MODELS_DIR_PATH_KEY in self.params):
                
                face_models_path = self.params[FACE_MODELS_DIR_PATH_KEY]     
        
        rec_file_path = os.path.join(rec_path, file_name)
        
        rec_loaded = False
        
        # Try to load YAML file with recognition results
        if(os.path.exists(rec_file_path)):
            
            print 'Loading YAML file with clustering results'
            
            rec_faces = load_YAML_file(rec_file_path)
            
            if(rec_faces):
                
                self.recognized_faces = rec_faces
                
                print 'YAML file with clustering results loaded'
                
                rec_loaded = True
                
        if(not(rec_loaded)):
        
            # Check existence of tracking results
            track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
            
            file_name = res_name + '.YAML'
                
            file_path = os.path.join(track_path, file_name)
            
            if(self.params is not None):
                
                if(FACE_TRACKING_FILE_PATH_KEY in self.params):
                    
                    file_path = self.params[FACE_TRACKING_FILE_PATH_KEY]
            
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
            
            if((self.params is not None)
            and (NOSE_POS_FILE_PATH_KEY in self.params)):
                    
                nose_pos_file_path = self.params[NOSE_POS_FILE_PATH_KEY]
                
                with open(nose_pos_file_path) as f:
                    
                    self.nose_pos_list = pk.load(f)
                    
            else:
                    
                # Save face models
                self.saveFaceModels(tracking_list)
                
            use_clothing_rec = USE_CLOTHING_RECOGNITION
            
            if(self.params is not None):
            
                use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]    
                
            if(use_clothing_rec and 
            ((self.params is None) or 
            (CLOTH_MODELS_DIR_PATH_KEY not in self.params))):
                
                # Save cloth models
                self.saveClothModels(tracking_list)
            
            print '\n\n### People clustering ###\n'
            
            # Save processing time
            start_time = cv2.getTickCount()
            
            self.recognized_faces = []
            
            update_after_merging = UPDATE_FACE_MODEL_AFTER_MERGING
            
            if(self.params is not None):
            
                update_after_merging = (
                self.params[UPDATE_FACE_MODEL_AFTER_MERGING_KEY])
            
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
                    
                    # Add annotation for segment
                    if(ANN_TAG_KEY in tracking_segment_dict):
                    
                        segment_ann = tracking_segment_dict[ANN_TAG_KEY]
                    
                        segment_dict[ANN_TAG_KEY] = segment_ann
                    
                    segment_list.append(segment_dict)
                    
                    ann_segments.append(segment_counter)
                    
                    db_path= os.path.join(
                    face_models_path, str(segment_counter))
                    
                    if(os.path.isfile(db_path)):
                        
                        model = cv2.createLBPHFaceRecognizer()
                        
                        model.load(db_path)
                    
                        if(model):

                            # Use model of this segment 
                            # to recognize faces of remaining segments
                            
                            if(update_after_merging):
                                
                                # Get histograms from model
                                train_hists = (
                                model.getMatVector("histograms"))
        
                                # Get labels from model
                                train_labels = model.getMat("labels")
                                
                                ann_segments = self.searchFaceWithUpdating(
                                ann_segments, segment_list, train_hists,
                                train_labels, segment_counter)
                                
                            else:
                                
                                ann_segments = self.searchFace(ann_segments, 
                                segment_list, model, segment_counter)

                            # Add segments to person dictionary
                            
                            person_dict[SEGMENTS_KEY] = segment_list
                            
                            # Save total duration of video in milliseconds
                            
                            tot_duration = (
                            self.video_frames * 1000.0 / self.fps)
                            
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
            
            print 'Time for people clustering:', time_in_seconds, 's\n'
            
            # Delete directory with aligned faces
            align_path = os.path.join(rec_path, ALIGNED_FACES_DIR) 
            
            if(os.path.exists(align_path)):
            
                shutil.rmtree(align_path)
            
            self.anal_times[PEOPLE_CLUSTERING_TIME_KEY] = time_in_seconds
            
            anal_file_name = res_name + '_anal_times.YAML'
            
            anal_file_path = os.path.join(video_path, anal_file_name)
            
            save_YAML_file(anal_file_path, self.anal_times)
    
        
    def recognizeFacesInVideo(self):
        '''
        Recognize faces on analyzed video,
        assigning a tag to each face.
        It works by using a list of people clusters
        '''  
        
        res_name = self.resource_name
        
        # YAML file with results
        file_name = res_name + '.YAML'
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        # Directory for recognition results
        rec_path = os.path.join(video_path, FACE_RECOGNITION_DIR) 
        
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
            
            # Check existence of clustering results
            
            cluster_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR)
            
            file_name = res_name + '.YAML'
            
            file_path = os.path.join(cluster_path, file_name)
            
            if(len(self.recognized_faces) == 0):
            
                # Try to load YAML file
                if(os.path.exists(file_path)):
                    
                    print 'Loading YAML file with clustering results'
                    
                    with open(file_path) as f:
        
                        self.recognized_faces = yaml.load(f) 
                        
                    print 'YAML file with clustering results loaded'
                        
                else:
                    
                    print 'Warning! No clustering results found!'
                    
                    return 
                    
            print '\n\n### People recognition ###\n'
                
            # Save processing time
            start_time = cv2.getTickCount()            
                        
            # Try to load YAML file with number of faces in frames
            faces_nr_file_path = os.path.join(
            video_path, FACES_NR_IN_FRAMES_FILE)
            
            if(os.path.exists(faces_nr_file_path)):
                
                print 'Loading YAML file with number of faces in frames'
                
                with open(faces_nr_file_path) as f:
                    
                    self.faces_nr = yaml.load(f)
                    
                print ' YAML file with number of faces in frames loaded'
            
            else:
                # Get number of faces in each frame
                self.getFacesNr()
            
            print(self.faces_nr)
            
            p_counter = 0
            
            clusters_nr = float(len(self.recognized_faces))
            
            # Iterate through people clusters
            for person_dict in self.recognized_faces:
                
                self.progress = 100 * (p_counter / clusters_nr)
            
                print('progress: ' + str(self.progress) + ' %          \r'),
                
                segment_list = person_dict[SEGMENTS_KEY]
                
                # Iterate through segments related to this person
                for segment_dict in segment_list:
                    
                    frame_list = segment_dict[FRAMES_KEY]
                    
                    for frame_dict in frame_list:
                        
                        frame_path = frame_dict[FRAME_PATH_KEY]
                        
                        # Check if this is the only face in this frame
                        if((frame_path in self.faces_nr) 
                        and (self.faces_nr[frame_path] == 1)):
                            
                            # Execute caption recognition
                            gray_im = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE) 
                            
                            get_tag_from_image(gray_im, self.params)      
    
    
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
        
        offset_pct_x = OFFSET_PCT_X
        offset_pct_y = OFFSET_PCT_Y
        
        cropped_face_width = CROPPED_FACE_WIDTH
        cropped_face_height = CROPPED_FACE_HEIGHT
        
        if(self.params is not None):
            
            if(OFFSET_PCT_X_KEY in self.params):
                offset_pct_x = self.params[OFFSET_PCT_X_KEY]
                
            if(OFFSET_PCT_Y_KEY in self.params):
                offset_pct_y = self.params[OFFSET_PCT_Y_KEY]
            
            if(CROPPED_FACE_WIDTH_KEY in self.params):
                cropped_face_width = self.params[CROPPED_FACE_WIDTH_KEY]
                
            if(CROPPED_FACE_HEIGHT_KEY in self.params):
                cropped_face_height = self.params[CROPPED_FACE_HEIGHT_KEY]           
        
        offset_pct = (offset_pct_x, offset_pct_y)
        dest_sz = (cropped_face_width, cropped_face_height)
        
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
            
            use_nose_pos_in_rec = USE_NOSE_POS_IN_RECOGNITION
            
            if(self.params is not None):
            
                use_nose_pos_in_rec = self.params[USE_NOSE_POS_IN_RECOGNITION_KEY]
            
            if(not(use_nose_pos_in_rec)):
                
                bbox = segment_frame_dict[TRACKING_BBOX_KEY]
                
                x0 = bbox[0]
                x1 = x0 + bbox[2]
                y0 = bbox[1]
                y1 = y0 + bbox[3]
                
                tracked_face = image[y0:y1, x0:x1]
                
                cv2.imwrite(TMP_TRACKED_FACE_FILE_PATH, tracked_face)
    
                crop_result = fd.get_cropped_face(
                TMP_TRACKED_FACE_FILE_PATH, align_path, self.params, False)
                
                if(crop_result):
                    
                    face = crop_result[FACE_KEY]
                    
                    if(face is not None):
                        
                        result = face
                    
        del(image)
        
        return result


    def saveDiscTrackingSegments(self):
        '''
        Save frames from discarded tracking segments on disk.
        A folder contains the frames from one segment
        '''         
        
        print '\n\n### Saving discarded tracking segments ###\n'
        
        # Create directory for this video  
        res_name = self.resource_name
            
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
                
                del(image)
                
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
            
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
                #cv2.rectangle(
                #image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                
                file_name = '%07d.bmp' % image_counter
                
                face_path = os.path.join(segment_path, file_name)
                
                cv2.imwrite(face_path, image)
                
                del(image)
                
                image_counter = image_counter + 1
                
                face_counter = face_counter + 1
                
            segment_counter = segment_counter + 1  
 
 
    def saveRecPeople(self, use_face_rec_dir):
        '''
        Save frames for recognized people on disk.
        A folder contains the segments from one person
        
        :type use_face_rec_dir: boolean
        :param use_face_rec_dir: if true, use PEOPLE_CLUSTERING_DIR, 
        otherwise use CLOTHIN_RECOGNITION_DIR
        '''  
        
        print '\n\n### Saving recognized people ###\n'
               
        # Create directory for this video  
        res_name = self.resource_name
            
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)       
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR)
        
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
                    
                    del(image)
                    
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
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        #use_clothing_rec = USE_CLOTHING_RECOGNITION
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            
            #use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 
        
        ### TO BE DELETED ###
        
        #if(use_clothing_rec):
            
        #    rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR) 
            
        #####################
        
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
                        
                        # Ask user if shown person is known
                        while((ans != ANSWER_YES) and (ans != ANSWER_NO)):
                            
                            ans = raw_input(IS_KNOWN_PERSON_ASK)
                            
                        if(ans == ANSWER_YES):
                            name = raw_input(PERSON_NAME + ': ')
                            surname = raw_input(PERSON_SURNAME + ': ')
                            final_tag = surname + '_' + name
                            
                        print '\n'
                        
                        person_dict[ANN_TAG_KEY] = final_tag
                    
                    del(image)
                    
                    p_counter = p_counter + 1
                    
        #print(self.recognized_faces)

    def readUserAnnotations(self):
        '''
        Read annotations by user from disk
        '''

        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        use_clothing_rec = USE_CLOTHING_RECOGNITION
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            
            use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 

        if(use_clothing_rec):
            
            rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR)
        
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
            
            auto_p_dict[ANN_TAG_KEY] = UNDEFINED_TAG
            
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
                        
                        found = True
                        
                        break
                        
                if(found):
                    
                    break
                        
            user_rec_faces.append(auto_p_dict)            
                        
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
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        half_window_size = HALF_WINDOW_SIZE
        
        std_mult_frame = STD_MULTIPLIER_FRAME
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            
            half_window_size = self.params[HALF_WINDOW_SIZE_KEY]
            
            std_mult_frame = self.params[STD_MULTIPLIER_FRAME_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
            
            del(image)
            
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
            self.hist_diffs, half_window_size, std_mult_frame)      
            
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
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        #use_clothing_rec = USE_CLOTHING_RECOGNITION
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
            #use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 
        
        ### TO BE DELETED ###
        
        #if(use_clothing_rec):
            
        #    rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR) 
            
        #####################
        
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
            
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)      
        
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
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        use_clothing_rec = USE_CLOTHING_RECOGNITION
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
            
            use_clothing_rec = self.params[USE_CLOTHING_RECOGNITION_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 
        
        if(use_clothing_rec):
            
            rec_path = os.path.join(video_path, CLOTHING_RECOGNITION_DIR)
        
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
            
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)       
        
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
            
        # Get minimum segment duration
        min_duration = MIN_SEGMENT_DURATION
        
        if((self.params is not None) and
        (MIN_SEGMENT_DURATION_KEY in self.params)):
            
            min_duration = self.params[MIN_SEGMENT_DURATION_KEY]
        
        # Save unique tags
        tags = []
        
        for person_dict in self.recognized_faces:
            
            ann_tag = person_dict[ANN_TAG_KEY]
            
            if((ann_tag != UNDEFINED_TAG) and (ann_tag not in tags)):
                
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
            
            tot_dur = 0
            
             # Iterate through all recognized people in video
            for temp_person_dict in self.recognized_faces:
                
                ann_tag = temp_person_dict[ANN_TAG_KEY]
                
                if(ann_tag == tag):
                    
                    temp_segment_list = temp_person_dict[SEGMENTS_KEY]
                        
                    for segment_dict in temp_segment_list:
                    
                        segment_list.append(segment_dict)
                
                        simple_seg_dict = {}
                        
                        start = segment_dict[SEGMENT_START_KEY]
                        
                        simple_seg_dict[SEGMENT_START_KEY] = start
                        
                        dur = segment_dict[SEGMENT_DURATION_KEY]
                        
                        tot_dur = tot_dur + dur
                        
                        simple_seg_dict[SEGMENT_DURATION_KEY] = dur
                        
                        simple_segment_list.append(simple_seg_dict)
                    
            person_dict[SEGMENTS_KEY] = segment_list
                    
            MERGE_CONSECUTIVE_SEGMENTS = False # TODO SET TRUE (AFTER EXPERIMENTS)
            if(MERGE_CONSECUTIVE_SEGMENTS):
                    
                (simple_segment_list, tot_dur) = merge_consecutive_segments(
                simple_segment_list, min_duration)
            
            simple_dict[SEGMENTS_KEY] = simple_segment_list
            
            person_dict[TOT_SEGMENT_DURATION_KEY] = tot_dur
            
            simple_dict[TOT_SEGMENT_DURATION_KEY] = tot_dur
            
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
                    
                del(image)
            
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
            
            
            half_window_size = HALF_WINDOW_SIZE
        
            std_mult_face = STD_MULTIPLIER_FACE
        
            if(self.params is not None):
                
                half_window_size = self.params[HALF_WINDOW_SIZE_KEY]
                
                std_mult_face = self.params[STD_MULTIPLIER_FACE_KEY]
            
            face_cut_idxs_temp = get_shot_changes(
            det_diff_list, half_window_size, std_mult_face) 
            
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
            
        use_or_fps = USE_ORIGINAL_FPS
        used_fps = USED_FPS
        min_detection_pct = MIN_DETECTION_PCT
        min_segment_duration = MIN_SEGMENT_DURATION
        
        if(self.params is not None):
            
            use_or_fps = self.params[USE_ORIGINAL_FPS_KEY]
            used_fps = self.params[USED_FPS_KEY]
            min_detection_pct = self.params[MIN_DETECTION_PCT_KEY]
            min_segment_duration = self.params[MIN_SEGMENT_DURATION_KEY]    
            
        # Minimum duration of a segment in frames
        min_segment_frames = int(
        math.ceil(self.fps * min_segment_duration))   
        
        # If a reduced bitrate is used, frames are less
        if(not(use_or_fps)):
            
            min_segment_frames = int(
            math.ceil((used_fps+1) * min_segment_duration)) 
            
        # Iterate through new sub segments
        for sub_frame_list in sub_segment_list:
            
            frame_counter = len(sub_frame_list)
            
            segment_dict = {}
        
            segment_dict[FRAMES_KEY] = sub_frame_list
        
            segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = frame_counter         
        
            # Segment duration in milliseconds
            
            duration = frame_counter * 1000.0 / self.fps
            
            # If a reduced bitrate is used, frames are less
            
            if(not(use_or_fps)):
            
                duration = frame_counter * 1000.0 / (used_fps+1)
        
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
                
                #print('det_pct', det_pct)
                    
                if(det_pct >= min_detection_pct):   
            
                    new_segments.append(segment_dict)
                    
                else:
                    
                    self.disc_tracked_faces.append(segment_dict)
            else:
                
                self.disc_tracked_faces.append(segment_dict)
            
        return new_segments
        
    
    def getClothThreshold_old(self):
        '''
        Calculate threshold for cloth recognition.
        '''
        
        res_name = self.resource_name

        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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
        
        
        
        
    def showTrackedPeople(self):
        '''
        Show and save one image for each tracked people in video
        ''' 
        
        # Check existence of tracking results
        
        res_name = self.resource_name
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        key_frames_path = os.path.join(
        track_path, FACE_RECOGNITION_KEY_FRAMES_DIR)
        
        if(not(os.path.exists(key_frames_path))):
            
            os.makedirs(key_frames_path)

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
        
        p_counter = 0
        
        for segment_dict in self.tracked_faces:
                
            frame_list = segment_dict[FRAMES_KEY]      
    
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
                
                del(image)
                
                p_counter = p_counter + 1
                    

    def readTrackUserAnnotations(self):
        '''
        Read annotations by user from disk
        '''

        # Check existence of tracking results
        
        res_name = self.resource_name
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
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

        user_ann_path = os.path.join(
        track_path, FACE_RECOGNITION_USER_ANNOTATIONS)
        
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
        
        # Iterate through tracked faces
        for auto_p_dict in self.tracked_faces:
            
            auto_p_dict[ANN_TAG_KEY] = UNDEFINED_TAG
            
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
                        
                        found = True
                        
                        break
                        
                if(found):
                    
                    break
                        
            user_rec_faces.append(auto_p_dict)            
                        
            auto_p_counter = auto_p_counter + 1          
                    
        self.tracked_faces = user_rec_faces
        
        # Save recognition result in YAML file
        save_YAML_file(file_path, self.tracked_faces) 
        
        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for user annotation:', time_in_seconds, 's\n'

        self.anal_times[USER_ANNOTATION_TIME_KEY] = time_in_seconds
        
        anal_file_name = res_name + '_anal_times.YAML'
        
        anal_file_path = os.path.join(video_path, anal_file_name)
        
        save_YAML_file(anal_file_path, self.anal_times)


    def simulateUserAnnotations(self):
        '''
        Simulate user annotations by tacking tags from first segments
        '''     
        
        # Check existence of recognition results
        
        res_name = self.resource_name
        
        # Directory for this video     
        video_indexing_path = VIDEO_INDEXING_PATH
        
        if(self.params is not None):
            
            video_indexing_path = self.params[VIDEO_INDEXING_PATH_KEY]
           
        video_path = os.path.join(video_indexing_path, res_name)
        
        rec_path = os.path.join(video_path, PEOPLE_CLUSTERING_DIR) 

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
         
        auto_p_counter = 0
        
        user_rec_faces = []
        
        # Iterate through automatic recognized faces
        for auto_p_dict in self.recognized_faces:
            
            segment_list = auto_p_dict[SEGMENTS_KEY]
            
            # Get first segment
            if(len(segment_list) >= 1):
                
                first_segment = segment_list[0]
                
                segment_ann_tag = first_segment[ANN_TAG_KEY]            
                        
                auto_p_dict[ANN_TAG_KEY] = segment_ann_tag
                        
                user_rec_faces.append(auto_p_dict)
                        
            auto_p_counter = auto_p_counter + 1          
                    
        self.recognized_faces = user_rec_faces
        
        # Save recognition result in YAML file
        save_YAML_file(file_path, self.recognized_faces)                
                
                                 
    def saveAnalysisResults(self):
        '''
        Save results of anlysis in dictionary
        '''  
        segments_nr = len(self.tracked_faces)
        self.anal_results[SEGMENTS_NR_KEY] = segments_nr
        
        people_clusters_nr = len(self.recognized_faces)
        self.anal_results[PEOPLE_CLUSTERS_NR_KEY] = people_clusters_nr
        
        # Count relevant tags
        relevant_people_nr = 0
        for person_dict in self.recognized_faces:
            
            tag = person_dict[ANN_TAG_KEY]
            
            if(tag!= UNDEFINED_TAG):
                
                relevant_people_nr = relevant_people_nr + 1
                
        self.anal_results[RELEVANT_PEOPLE_NR_KEY] = relevant_people_nr
