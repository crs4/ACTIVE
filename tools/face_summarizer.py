import cv2

import os

from Constants import *

from face_detection import detect_faces_in_image

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
        
        frame_list = [] # List of frame paths
        
        detected_faces = []
        
    def detectFacesInVideo(self, resource):
        '''
        Launch the face summarizer on one video resource.
        This method is asynchronous and returns a task handle
        
        :type resource: string
        :param resource: file path of resource
        '''
        
        print '### Face detection ###'
        
        # Save processing time
        start_time = cv2.getTickCount()
        
        error = None
        
        getFrameList()
        
        detection_params = None
        
        if self.params is not None:
			
			detection_params = self.params[FACE_DETECTION_KEY]
		
		frame_counter = 0
		detected_faces = []
		for frame_path in self.frame_list:	
			
			detection_result = detect_faces_in_image
			(frame_path, detection_params, False)
			
			detection_error = detection_result[ERROR_KEY]
			
			detection_dict = {}
			
			detection_dict[FRAME_COUNTER_KEY] = frame_counter
			
			if(not(detection_error)):
				
				face_bboxes = detection_result[FACES_KEY]
				face_images = detection_result[FACE_IMAGES_KEY]
				
				face_count = 0
				faces = []
				for face in face_images:
					face_dict = {}
					
					face_dict[BBOX_KEY] = face_bboxes[face_count]
					face_dict[FACE_KEY] = face
					
					faces.append(face_dict)
					
				detection_dict[FACES_KEY] = faces
				
				detection_dict[ERROR_KEY] = None
			
			else:
				
				detection_dict[ERROR_KEY] = detection_error				
        
    def getFrameList(self, resource):
        
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
                    elapsed_video_s = ms / 1000 
                    
                    print 'elapsed video s =', elapsed_video_s              
        
                    self.progress = 100 * (frame_counter / tot_frames)
    
                    #print('progress: ' + str(self.progress) + '%')
                            
                    fr_name = str(frame_counter) + '.bmp'
                    
                    frame_path = os.path.join(FRAME_DIR_PATH, fr_name)
                    
                    cv2.imwrite(frame_path, frame)
                    
                    self.frame_list.append(frame_path) 
                    
                    last_anal_frame = frame_counter
                    
                frame_counter = frame_counter + 1               
