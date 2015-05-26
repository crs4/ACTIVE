import cv2
import math
import os
import pickle
import time
from constants import *
from face_detection import detect_faces_in_image
from face_recognition import recognize_face
from Utils import aggregate_frame_results, load_YAML_file, save_YAML_file, track_faces_with_LBP


class FaceExtractor(object):
    '''
    Tool for detecting and recognizing faces in images and video.
    '''
    def __init__(self, face_models = None, params=None):
        '''
        Initialize the face extractor.
        The configuration parameters define and customize the face extraction algorithm.
        If any of the configuration parameters is not provided a default value is used.

        :type  face_models: a FaceModels object
        :param face_models: the face models data structure

        :type  params: dictionary 
        :param params: configuration parameters (see table)
        '''

        self.params = params;

        self.face_models = face_models;

        self.progress = 0;
        
        self.db_result4image={}
        

    def extractFacesFromImage(self, resource_path):
        '''
        Launch the face extractor on one image resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        # Save processing time
        start_time = cv2.getTickCount()

        error = None;
        
        # Face detection
        align_path = ALIGNED_FACES_PATH
        if((self.params is not None) and 
        (ALIGNED_FACES_PATH_KEY in self.params)):
            
            align_path = self.params[ALIGNED_FACES_PATH_KEY]

        detection_result = detect_faces_in_image(resource_path, align_path, self.params, False)
        
        detection_error = detection_result[ERROR_KEY]
        
        if(not(detection_error)):
            
            face_images = detection_result[FACES_KEY]
    
            detected_faces = detection_result[FACES_KEY]
    
            # Face recognition
            
            faces = []
            #face=cv2.imread(resource_path,cv2.IMREAD_GRAYSCALE);
            #face_images=[face]
            for det_face_dict in face_images:
                
                face_dict = {}
                
                face = det_face_dict[FACE_KEY]
                bbox = det_face_dict[BBOX_KEY]
                
                # Resize face
                resize_face = USE_RESIZING
                
                if((self.params is not None) and 
                (USE_RESIZING_KEY in self.params)):
                    
                    resize_face = self.params[USE_RESIZING_KEY]
                
                if(resize_face):
                    
                    face_width = CROPPED_FACE_WIDTH
                    face_height = CROPPED_FACE_HEIGHT
                    
                    if((self.params is not None) and 
                    (CROPPED_FACE_WIDTH_KEY in self.params) and
                    (CROPPED_FACE_HEIGHT_KEY in self.params)):
                        
                        face_width = self.params[CROPPED_FACE_WIDTH_KEY]
                        face_height = self.params[CROPPED_FACE_HEIGHT_KEY]
                    
                    new_size = (face_width, face_height)
                    face = cv2.resize(face, new_size)
                
                rec_result = recognize_face(face, self.face_models, self.params, False)
                
                tag = rec_result[ASSIGNED_TAG_KEY]
                confidence = rec_result[CONFIDENCE_KEY]
                face_dict[ASSIGNED_TAG_KEY] = tag
                face_dict[CONFIDENCE_KEY] = confidence
                face_dict[BBOX_KEY] = bbox
                face_dict[FACE_KEY] = face
                faces.append(face_dict)
    
            processing_time_in_clocks = cv2.getTickCount() - start_time
            processing_time_in_seconds = processing_time_in_clocks / cv2.getTickFrequency()
    
            # Populate dictionary with results
            results = {}
            results[ELAPSED_CPU_TIME_KEY] = processing_time_in_seconds
            results[ERROR_KEY] = error
            results[FACES_KEY] = faces
            
        else:
            
            results = {}
            results[ERROR_KEY] = detection_error
    
        self.progress = 100
        handle=time.time()
        self.db_result4image[handle]=results
    
        return handle
        

    def extractFacesFromVideo(self, resource):
        '''
        Launch the face extractor on one video resource.
        This method is asynchronous and returns a task handle.

        :type  resource: string
        :param resource: resource file path
        '''
        # Save processing time
        start_time = cv2.getTickCount()

        error = None
        frames = None
        segments = None

        capture = cv2.VideoCapture(resource)

        # Counter for all frames
        frame_counter = 0
        
        # Counter for analyzed frames
        anal_frame_counter = 0
        
        # Value of frame_counter for last analyzed frame
        last_anal_frame = 0

        if capture is None or not capture.isOpened():

            error = 'Error in opening video file'

        else:

            frames = []
            
            if((USE_TRACKING or SIM_TRACKING or USE_SLIDING_WINDOW)
            and LOAD_IND_FRAMES_RESULTS):
                
                # Load frames by using pickle
                
                print 'Loading frames'
                
                resource_name = os.path.basename(resource)
                
                file_name = resource_name + '.pickle'
                
                file_path = os.path.join(FRAMES_FILES_PATH, file_name)
                
                with open(file_path) as f:
                    
                    frames = pickle.load(f) 
                    
                    anal_frame_counter = len(frames)
                
            else:
            
                video_fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
    
                tot_frames = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    
                while True:
                
                    frame_dict = {}
                
                    ret, frame = capture.read()
    
                    if(not(ret)):
                        break
                        
                    # Next frame to be analyzed
                    next_frame = last_anal_frame + (video_fps/USED_FPS)
                    if(USE_ORIGINAL_FPS or (frame_counter > next_frame)):
    
                        # Frame position in video in seconds
                        elapsed_video_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                        elapsed_video_s = elapsed_video_ms / 1000 
                        
                        print "elapsed video s =", elapsed_video_s
                        
                        #video_position = capture.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO) # This doesn't work!
        
                        self.progress = 100 * (frame_counter / tot_frames)
        
                        #print('progress: ' + str(self.progress) + '%')
        
                        cv2.imwrite(TMP_FRAME_FILE_PATH, frame)
        
                        handle = self.extractFacesFromImage(TMP_FRAME_FILE_PATH)
        
                        frame_results = self.getResults(handle)
        
                        frame_error = frame_results[ERROR_KEY]
        
                        if(frame_error):
        
                            error = frame_results[ERROR_KEY]
        
                            break
        
                        else:
        
                            frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s
        
                            frame_dict[FACES_KEY] = frame_results[FACES_KEY]
        
                            frame_dict[FRAME_COUNTER_KEY] = frame_counter
        
                            frames.append(frame_dict)
                            
                        anal_frame_counter = anal_frame_counter + 1
                        
                        last_anal_frame = frame_counter
        
                    frame_counter = frame_counter + 1
                    
                frames_dict = {}
                
                frames_dict[FRAMES_KEY] = frames
                
                # Save frames by using pickle
                    
                resource_name = os.path.basename(resource)
                
                file_name = resource_name + '.pickle'
                
                file_path = os.path.join(FRAMES_FILES_PATH, file_name)    
                    
                with open(file_path, 'w') as f:
                    
                    pickle.dump(frames, f)
    
            if(USE_TRACKING and (frames is not None)):
                
                segments = track_faces_with_LBP(frames, self.face_models)

            elif(USE_SLIDING_WINDOW and (frames is not None)):

                frame_rate = capture.get(cv2.cv.CV_CAP_PROP_FPS)

                frame_nr_in_window = frame_rate * SLIDING_WINDOW_SIZE

                frame_nr_half_window = int(math.floor(frame_nr_in_window/2))

                print('frame_nr_half_window: ', frame_nr_half_window)

                sl_window_frame_counter = 0

                for frame in frames:

                    # Get faces from frame results
                    faces = frame[FACES_KEY]

                    if(len(faces) != 0):

                        # Select frames to be included in window
                        
                        first_frame_in_window = sl_window_frame_counter - frame_nr_half_window

                        if (first_frame_in_window < 0):

                            first_frame_in_window = 0 # First frame in window is first frame of all video if window exceeds video

                        last_frame_in_window = sl_window_frame_counter + frame_nr_half_window

                        if (last_frame_in_window > (len(frames)-1)):

                            last_frame_in_window = len(frames)-1

                        window_frames = frames[first_frame_in_window : (last_frame_in_window + 1)]

                        window_frames_list = []

                        for window_frame in window_frames:

                            # Get tag from first face
                            faces = window_frame[FACES_KEY]

                            if(len(faces) != 0):

                                first_face = faces[0];

                                assigned_tag = first_face[ASSIGNED_TAG_KEY]

                                confidence = first_face[CONFIDENCE_KEY]

                                window_frame_dict = {}

                                window_frame_dict[ASSIGNED_TAG_KEY] = assigned_tag

                                window_frame_dict[CONFIDENCE_KEY] = confidence

                                window_frames_list.append(window_frame_dict)

                        # Final tag for each frame depends on assigned tags on all frames in window

                        [frame_final_tag, frame_final_confidence] = aggregate_frame_results(window_frames_list, self.face_models)

                        print('frame_final_tag: ', frame_final_tag)

                        frame[FACES_KEY][0][ASSIGNED_TAG_KEY] = frame_final_tag

                        frame[FACES_KEY][0][CONFIDENCE_KEY] = frame_final_confidence

                    sl_window_frame_counter = sl_window_frame_counter + 1

        processing_time_in_clocks = cv2.getTickCount() - start_time
        processing_time_in_seconds = processing_time_in_clocks / cv2.getTickFrequency()

        # Populate dictionary with results
        results = {}
        results[ELAPSED_CPU_TIME_KEY] = processing_time_in_seconds
        results[ERROR_KEY] = error
        results[TOT_FRAMES_NR_KEY] = anal_frame_counter

        if(USE_TRACKING):
            
            results[SEGMENTS_KEY] = segments

        else:

            results[FRAMES_KEY] = frames
            
        self.progress = 100
        handle=time.time()
        self.db_result4image[handle]=results

        return handle
        

    def getResults(self, handle):
        '''
        Return the results of the face extraction process.
        This call invalidates the specified handle.
        If the handle was returned by extractFacesFromImage(), a dictionary 
        is returned with the following entries:
          elapsed_cpu_time:  float  (the elapsed cpu time in sec)
          error: a string specyfying an error condition, or None if no errors occurred
          faces: a list of tags with associated bounding boxes
        Example:
            results = {'elapsed_cpu_time':  0.011,
                       'error': None,
               'faces': ({'tag': 'Barack Obama', 'confidence': 60, 'bbox':(100,210, 50, 50)},
                                 {'tag': 'Betty White', 'confidence': 30, 'bbox':(30, 250, 40, 45)}
                                )
                      }
        For extractFacesFromVideo(), if no tracking is used, a dictionary is returned with the following entries:
            elapsed_cpu_time: float (the elapsed cpu time in sec)
            error: a string specyfying an error condition, or None if no errore occurred
            frames: a list of frames, each containing a list of tags with associated bounding boxes
        Example:
            results = {'elapsed_cpu_time': 11.1,
                       'error':None,
                       'tot_frames_nr':299
                       'frames': ({'elapsed_video_time': 0,
                                   'frameCounter': 0,
                                   'faces': ({'tag': 'Barack Obama', 'confidence':60, 'bbox':(100,210, 50, 50)},
                                             {'tag': 'Betty White', 'confidence':30, 'bbox':(30, 250, 40, 45)}
                                            )
                                  {'elapsed_video_time':0.04},
                                   'frameCounter': 1,
                                   'faces': ({'tag': 'Barack Obama', 'confidence':55, 'bbox':(110,220, 50, 50)},
                                             {'tag': 'Betty White', 'confidence':35, 'bbox':(40, 270, 40, 45)}                                  
                                 )
                      }
        For extractFacesFromVideo(), if tracking is used, a dictionary is returned with the following entries:
            elapsed_cpu_time: float (the elapsed cpu time in sec)
            error: a string specyfying an error condition, or None if no errore occurred
            segments: a list of segments, each associated to a person
        Example:
            results = {'elapsed_cpu_time': 11.1,
                       'error':None,
                       'tot_frames_nr':299
                       'segments': ({'tag': 'Barack Obama'
                                     'confidence': 40 
                                     'frames': ({'elapsed_video_time': 0,
                                                 'frameCounter': 0,
                                                 'tag': 'Barack Obama',
                                                 'confidence': 60
                                                 'bbox':(100,210, 50, 50)},
                                                {'elapsed_video_time':0.04},
                                                 'frameCounter': 1,
                                                 'tag': 'Barack Obama',
                                                 'confidence': 20
                                                 'bbox':(110,220, 50, 50)}                                  
                                                )
                                    )
                      }
                   
        :type  handle: integer
        :param handle: the task handle
        '''
        return self.db_result4image[handle]
