import cv2

import cv2.cv as cv

import face_detection as fd

import numpy as np

import os

import pickle as pk

from Constants import *

from Utils import aggregate_frame_results, is_rect_similar, save_YAML_file

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
        
        self.params = params
        
        self.resource_name = None # Name of resource being analyzed
        
        self.frame_list = [] # List of frame paths
        
        self.detected_faces = [] # List of detected faces
        
        # Minimum number of frames from detection 
        # before tracking interruption
        self.min_tracking_frames = 0
        
        self.tracked_faces = [] # List of tracked faces
        
        self.recognized_faces = [] # List of recognized faces
        
    def detectFacesInVideo(self):
        '''
        Detect faces on analyzed video.
        It works by using list of extracted frames
        '''
        
        print '### Face detection ###'
        
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
            
            frame_path = frame_dict[FRAME_PATH_KEY] 
            
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
        
        res_name = self.resource_name
        
        # Create directory for this video     
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        det_path = os.path.join(video_path, FACE_DETECTION_DIR) 
        
        if(not(os.path.exists(det_path))):
			
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
        
        print '### Frame extraction ###'
        
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
            
            # Calculate minimum number of frames for tracking
            self.min_tracking_frames = video_fps * MIN_TRACKING_TIME
            
            while True:
                
                # Read frame
                ret, frame = capture.read()
                
                # If not frame is read, abort
                if(not(ret)):
                    
                    break
                    
                # Next frame to be analyzed
                next_frame = last_anal_frame + (video_fps/USED_FPS)
                
                if(USE_ORIGINAL_FPS or (frame_counter > next_frame)):
                
                    # Frame position in video in seconds
                    ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                    elapsed_s = ms / 1000 
                    
                    #print 'elapsed video s =', elapsed_video_s              
        
                    self.progress = 100 * (frame_counter / tot_frames)
    
                    #print('progress: ' + str(self.progress) + '%')
                            
                    fr_name = str(frame_counter) + '.bmp'
                    
                    frame_path = os.path.join(frames_path, fr_name)
                    
                    cv2.imwrite(frame_path, frame)
                    
                    frame_dict = {}
                    
                    frame_dict[FRAME_PATH_KEY] = frame_path
                    
                    frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
                    
                    self.frame_list.append(frame_dict) 
                    
                    last_anal_frame = frame_counter
                    
                frame_counter = frame_counter + 1               

        # Save processing time
        time_in_clocks = cv2.getTickCount() - start_time
        time_in_seconds = time_in_clocks / cv2.getTickFrequency()
        
        print 'Time for frame extraction:', str(time_in_seconds), 's\n'


    def trackFacesInVideo(self):
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
        
        # Make copy of detected faces
        detection_list = list(self.detected_faces)
        
        # Iterate through frames in detected_faces
        for detection_dict in detection_list:
            
            #det_frame_counter = detection_dict[FRAME_COUNTER_KEY]
            
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
                segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
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
                
                ## Show image
                #cv2.rectangle(
                #image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                    
                #cv2.imshow('image', image)
            
                #cv2.waitKey(0)  
                
                # Set up the Region Of Interest for tracking
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                hist = cv2.calcHist(
                [hsv_roi], [0], mask_roi, [16], [0, 180])
                
                prev_hist = hist
                diff_list = [] # List with histogram differences
                
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                hist = hist.reshape(-1)
                
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
                        
                        break
                    
                    # Show track window (red) and detection bbox ( blue)
                    cv2.rectangle(sub_image, (track_x0, track_y0), 
                    (track_x1, track_y1), (0, 0, 255), 3, 8, 0) 
                    
                    sub_faces = sub_det_dict[FACES_KEY]
            
                    sub_face_counter = 0
                    
                    sim = False
                    
                    sub_face = None
                    
                    for sub_face_dict in sub_faces:

                        det_bbox = sub_face_dict[BBOX_KEY]
                    
                        # If track window corresponds to 
                        # a detected face, 
                        # update track window with detection 
                        # bounding box and delete detection from list
                        
                        sim = is_rect_similar(track_window, det_bbox)
                        
                        if(sim):
                            
                            det_face_counter = det_face_counter + 1
                            
                            #track_window = det_bbox
                            
                            #sub_face = sub_face_dict[FACE_KEY]
                            
                            #print('det_bbox', det_bbox)
                    
                            #det_x0 = det_bbox[0]
                            #det_y0 = det_bbox[1]
                            #det_w = det_bbox[2]
                            #det_h = det_bbox[3]
                            #det_x1 = det_x0 + det_w
                            #det_y1 = det_y0 + det_h 
                            
                            #cv2.rectangle(image, (det_x0, det_y0), 
                            #(det_x1, det_y1), (255, 0, 0), 3, 8, 0) 
                            
                            break
                            
                        sub_face_counter = sub_face_counter + 1 
                        
                    # Percentage of detected faces must be greater
                    # than MIN_DETECTION_PCT
                        
                    det_pct = float(det_face_counter / segment_face_counter)
                
                    if(det_pct < MIN_DETECTION_PCT):
                
                        break
                        
                    x0 = track_window[0]
                    y0 = track_window[1]
                    w = track_window[2]
                    h = track_window[3]
                    x1 = x0 + w
                    y1 = y0 + h    
                        
                    # Set up the Region Of Interest for tracking
                    hsv_roi = sub_hsv[y0:y1, x0:x1]
                    mask_roi = sub_mask[y0:y1, x0:x1]
                    new_hist = cv2.calcHist(
                    [hsv_roi], [0], mask_roi, [16], [0, 180])
                    
                    # Calculate difference between histograms of 
                    # faces in two consecutive frames
                    diff = abs(cv2.compareHist(
                    prev_hist, new_hist,cv.CV_COMP_CHISQR))
                    
                    prev_hist = new_hist
                        
                    if((segment_face_counter > self.min_tracking_frames)
                        and (len(diff_list) > 0)):
                        
                        mean = np.mean(diff_list)
                        std = np.std(diff_list)
                        
                        threshold = mean + 2 * std
                        
                        if(diff > threshold):
                            
                            print 'threshold = ', threshold

                            break
 
                    # Do not consider first frames in tracking for
                    # threshold calculation    
                    if(segment_face_counter > FRAMES_TO_DISCARD):
                            
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
                    
                        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                        hist = hist.reshape(-1)
                        
                        del (detection_list[sub_frame_counter]
                        [FACES_KEY][sub_face_counter])                             
                        
                    else:
                        
                        segment_frame_dict[DETECTED_KEY] = False    
                      
                    elapsed_s = sub_det_dict[ELAPSED_VIDEO_TIME_KEY]  
                        
                    # Update list of frames for segment
                    segment_frame_dict[FRAME_COUNTER_KEY] = sub_frame_counter
                    segment_frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
                    segment_frame_dict[BBOX_KEY] = track_window
                    #segment_frame_dict[FACE_KEY] = sub_face
                    segment_frame_dict[FRAME_PATH_KEY] = sub_frame_path
                    segment_frame_list.append(segment_frame_dict)

                    #cv2.imshow('image', sub_image)
            
                    #cv2.waitKey(0) 
                    
                    sub_frame_counter = sub_frame_counter + 1   
                    
                    segment_face_counter = segment_face_counter + 1                 
                
                segment_dict[FRAMES_KEY] = segment_frame_list
                
                segment_dict[SEGMENT_TOT_FRAMES_NR_KEY] = segment_face_counter
                
                segment_dict[ASSIGNED_TAG_KEY] = 'Undefined'
                
                segment_dict[CONFIDENCE_KEY] = -1
                
                print 'segment_face_counter:', segment_face_counter
                
                det_pct = float(det_face_counter / segment_face_counter)
                
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
        
        print '### Face Recognition ###'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        self.recognized_faces = []
        
        # List of segments already analyzed and annotated
        ann_segments = []
        
        # Iterate through tracked faces

        segment_counter = 0
        tag = 0
        for tracking_segment_dict in self.tracked_faces:
            
            if(segment_counter not in ann_segments):
                    
                # Save all segments relative 
                # to one person in person_dict
                person_dict = {}
                
                person_dict[ASSIGNED_TAG_KEY] = tag
                
                segment_list = []
                
                segment_dict = {}
                
                segment_dict[FRAMES_KEY] = tracking_segment_dict
                
                segment_dict[ASSIGNED_TAG_KEY] = tag
                
                segment_dict[CONFIDENCE_KEY] = 0
                
                segment_list.append(segment_dict)
                
                ann_segments.append(segment_counter)
                
                model = self.createFaceModel(tracking_segment_dict)
                
                # Use model of this segment 
                # to recognize faces of remaining segments
                sub_segment_counter = 0
                for sub_segment_dict in self.tracked_faces:
                    
                    #print('ann_segments', ann_segments)
                    
                    if(sub_segment_counter not in ann_segments):
                    
                        segment_frame_list = sub_segment_dict[FRAMES_KEY]
                        
                        frames = []
                        
                        for segment_frame_dict in segment_frame_list:
                            
                            face = self.getFaceFromSegmentFrame(
                            segment_frame_dict)

                            if(face is not None):
                                
                                #cv2.imshow('face', face)
                                #cv2.waitKey(0)
                                
                                conf = model.predict(
                                np.asarray(face, dtype=np.uint8))
                                
                                print ('conf', conf)
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
                            
                            segment_dict[FRAMES_KEY] = sub_segment_dict
                            
                            segment_dict[ASSIGNED_TAG_KEY] = tag
                            
                            segment_dict[CONFIDENCE_KEY] = final_conf
                            
                            segment_list.append[segment_dict] 
                             
                    print('sub_segment_counter', sub_segment_counter)                            
                    sub_segment_counter = sub_segment_counter + 1
                
                # Add segments to person dictionary
                
                person_dict[SEGMENTS_KEY] = segment_list
                
                self.recognized_faces.append(person_dict)
                
                tag = tag + 1
                
            segment_counter = segment_counter + 1
        
        # Save recognition result in YAML file
        file_name = self.resource_name + '.YAML'
            
        file_path = os.path.join(FACE_TRACKING_PATH, file_name)
        
        save_YAML_file(file_path, self.tracked_faces) 
        
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
        
        bbox = segment_frame_dict[BBOX_KEY]
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
            bbox = segment_frame_dict[BBOX_KEY]
            
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
                
                if(face):
                    
                    result = face
                    
        return result
        
        
    def saveTrackingSegments(self):
        '''
        Save frames from tracking segments on disk.
        A folder contains the frames from one segment
        '''         
        
        # Create directory for this video  
        res_name = self.resource_name
            
        video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)
        
        track_path = os.path.join(video_path, FACE_TRACKING_DIR) 
        
        segments_path = os.path.join(
        track_path, FACE_TRACKING_SEGMENTS_DIR)
        
        if(not(os.path.exists(segments_path))):
			
			os.makedirs(segments_path)   
        
        segment_counter = 0
        
        for segment_dict in self.tracked_faces:
            
            segment_frame_list = segment_dict[FRAMES_KEY]
            
            segment_path = os.path.join(
            segments_path, str(segment_counter))
            
            if(not(os.path.exists(segment_path))):
				
				os.makedirs(segment_path)
            
            image_counter = 0
            
            for segment_frame_dict in segment_frame_list:
                
                frame_path = segment_frame_dict[FRAME_PATH_KEY]
                
                bbox = segment_frame_dict[BBOX_KEY]
                
                x0 = bbox[0]
                x1 = x0 + bbox[2]
                y0 = bbox[1]
                y1 = y0 + bbox[3]
                
                # Show image
                image = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                              
                cv2.rectangle(
                image, (x0, y0), (x1, y1), (0, 0, 255), 3, 8, 0)
                
                file_name = str(image_counter) + '.bmp'
                
                face_path = os.path.join(segment_path, file_name)
                
                cv2.imwrite(face_path, image)
                
                image_counter = image_counter + 1
                
            segment_counter = segment_counter + 1   
        
