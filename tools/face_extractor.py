#---------------------------------------------------------
# This module defines the following classes of the ActiveTools API:
#    FaceModels
#    FaceExtractor
#
# The documentation API shall be automatically generated using Sphynx.
# All methods are blocking, unless specified otherwise.
#
# To do:
#  - define and list custom exceptions!
#  - define configuration parameters
#  
#---------------------------------------------------------

import cv2
from face_detection import detect_faces_in_image
from face_recognition import recognize_face
from Utils import load_YAML_file, aggregate_frame_results
from Constants import *
import time


class FaceModels(object):
    '''
    The persistent data structure containing the face models used by the 
    face recognition algorithm and replicated on each worker.
    This class ensures that the face models are replicated and updated on each worker.
    '''
    def __init__(self, workers):
        '''
        Initialize the face models on all workers.

        :type  workers: list of strings
        :param workers: the address (IP and port) of workers.
        '''
        pass
		
    def add_faces(self, filenames_or_images, tag):
        '''
        Add new faces to the face models and associate them with the given tag.
        No check is done on invalid or duplicated faces (it is resposibility of the caller to provide valid faces).
        This method is asynchronous and is propagated to all workers.

        :type  filenames_or_images: an Image object, or a string, or a list of Image objects, or a list of strings
        :param filenames_or_images: faces to be added to the face models data structure

        :type  tag: string
        :param tag: the tag associated to the face to be added to the face models data structure
        '''
        pass

    def remove_tags(self, tags):
        '''
        Remove the given tag or tags (and all associated faces) from the face models data structure.
        If any of the provided tags is not in the face models data structure, the tag is ignored.
        This method is asynchronous and is propagated to all workers.

        :type  tags: string or list of strings
        :param tags: the tags associated to the face to be added to the face models data structure
        '''
        pass
        
    def rename_tag(self, old_tag, new_tag, blocking=True):
        '''
        Rename a tag in the face models data structure.
        Raise an exception if old_tag does not exist in face models data structure.
        Raise an exception if new_tag already exists in face models data structure.
        This method is asynchronous and is propagated to all workers.

        :type  old_tag: string
        :param old_tag: a tag already present in the face models data structure

        :type  new_tag: string
        :param new_tag: a tag not yet present in the face models data structure
        '''
        pass

    def sync(self):
        '''
        Wait until all asynchronous methods previously invoked have been executed by all workers.
        This method shall be called in order to ensure that face models data structure on all workers are aligned.
        '''
        pass
        
    def dump(self):
        '''
        Return a file containig the dump of the face models data structure.
        '''
        pass
        
    def load(self, file_name):
        '''
        Update the face models data structure on all workers from a file.
        
        :type  file_name: string
        :param file_name: the name of the file containing the dump of the face models data structure
        '''
        pass

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

        if(params == None):
            # Load configuration file
            self.params = load_YAML_file(FACE_EXTRACTOR_CONFIGURATION_FILE_PATH);
        else:
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
        detection_params = self.params[FACE_DETECTION_KEY]

        detection_result = detect_faces_in_image(resource_path, detection_params, False)

        face_bboxes = detection_result[FACE_DETECTION_FACES_KEY]
        face_images = detection_result[FACE_DETECTION_FACE_IMAGES_KEY]

        # Face recognition
        recognition_params = self.params[FACE_RECOGNITION_KEY]
        
        faces = []
        count = 0
        #face=cv2.imread(resource_path,cv2.IMREAD_GRAYSCALE);
        #face_images=[face]
        for face in face_images:
            
            face_dict = {}
            
            # Resize face
            resize_face = False
            if(resize_face):
                new_size = (CROPPED_FACE_WIDTH, CROPPED_FACE_HEIGHT)
                face = cv2.resize(face, new_size)
            
            rec_result = recognize_face(face, self.face_models, recognition_params, False)
            tag = rec_result[PERSON_ASSIGNED_TAG_KEY]
            confidence = rec_result[PERSON_CONFIDENCE_KEY]
            face_dict[FACE_EXTRACTION_TAG_KEY] = tag
            face_dict[FACE_EXTRACTION_CONFIDENCE_KEY] = confidence
            face_dict[FACE_EXTRACTION_BBOX_KEY] = face_bboxes[count]
            faces.append(face_dict)
            count = count + 1

        processing_time_in_clocks = cv2.getTickCount() - start_time
        processing_time_in_seconds = processing_time_in_clocks / cv2.getTickFrequency()

        # Populate dictionary with results
        results = {}
        results[FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY] = processing_time_in_seconds
        results[FACE_EXTRACTION_ERROR_KEY] = error
        results[FACE_EXTRACTION_FACES_KEY] = faces

        self.progress = 100
        handle=time.time()
        self.db_result4image[handle]=results

        return handle
    
    def extractFacesFromVideo(self, resource):
        '''
        Launch the face extractor on one video resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        # Save processing time
        start_time = cv2.getTickCount()

        error = None
        frames = None
        segments = None

        capture = cv2.VideoCapture(resource)

        frame_counter = 0

        if capture is None or not capture.isOpened():

            error = 'Error in opening video file'

        else:

            frames = []

            while True:
            
                frame_dict = {}
            
                ret, frame = capture.read()

                if(not(ret)):
                    break;

                elapsed_video_ms = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)

                elapsed_video_s = elapsed_video_ms / 1000 # Frame position in video in seconds

                video_position = capture.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO)

                self.progress = 100 * video_position

                cv2.imwrite(TMP_FRAME_FILE_PATH, frame)

                handle = self.extractFacesFromImage(TMP_FRAME_FILE_PATH)

                frame_results = self.getResults(handle)

                frame_error = frame_results[FACE_EXTRACTION_ERROR_KEY]

                if(frame_error):

                    error = frame_results[FACE_EXTRACTION_ERROR_KEY]

                    break;

                else:

                    frame_dict[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                    frame_dict[FACE_EXTRACTION_FACES_KEY] = frame_results[FACE_EXTRACTION_FACES_KEY]

                    frame_dict[FACE_EXTRACTION_FRAME_COUNTER_KEY] = frame_counter

                    frames.append(frame_dict)

                frame_counter = frame_counter + 1;

            if(USE_TRACKING):

                segments = []

                frame_counter = 0
                
                for frame in frames:

                    faces = frame[FACE_EXTRACTION_FACES_KEY]

                    elapsed_video_s = frame[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY]

                    if(len(faces) != 0):

                        face_counter = 0
                        for face in faces:

                            segment_dict = {}

                            prev_bbox = face[FACE_EXTRACTION_BBOX_KEY]

                            segment_frames_list = []

                            segment_frame_dict = {}

                            segment_frame_dict[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                            segment_frame_dict[FACE_EXTRACTION_FRAME_COUNTER_KEY] = frame_counter

                            segment_frame_dict[FACE_EXTRACTION_TAG_KEY] = face[FACE_EXTRACTION_TAG_KEY]

                            segment_frame_dict[FACE_EXTRACTION_CONFIDENCE_KEY] = face[FACE_EXTRACTION_CONFIDENCE_KEY]

                            segment_frame_dict[FACE_EXTRACTION_BBOX_KEY] = prev_bbox

                            segment_frames_list.append(segment_frame_dict)

                            del frames[frame_counter][FACE_EXTRACTION_FACES_KEY][face_counter]

                            sub_frame_counter = frame_counter + 1

                            prev_frame_counter = frame_counter

                            # Search face in subsequent frames and add good bounding boxes to segment
                            # Bounding boxes included in this segment must not be considered by other segments

                            for subsequent_frame in frames[sub_frame_counter :]:

                                # Consider only successive frames or frames whose maximum distance is MAX_FRAMES_WITH_MISSED_DETECTION + 1
                                if((sub_frame_counter > (prev_frame_counter + MAX_FRAMES_WITH_MISSED_DETECTION + 1))):
                                    print('### WARNING - Frames too distant')
                                    print(sub_frame_counter)
                                    print(prev_frame_counter)

                                    break;

                                sub_faces = subsequent_frame[FACE_EXTRACTION_FACES_KEY]

                                elapsed_video_s = subsequent_frame[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY]

                                if(len(sub_faces) != 0):

                                    sub_face_counter = 0
                                    for sub_face in sub_faces:

                                        # Calculate differences between the two detections
                                
                                        prev_bbox_x = prev_bbox[0]
                                        prev_bbox_y = prev_bbox[1]
                                        prev_bbox_w = prev_bbox[2]

                                        bbox = sub_face[FACE_EXTRACTION_BBOX_KEY]

                                        bbox_x = bbox[0]
                                        bbox_y = bbox[1]
                                        bbox_w = bbox[2]

                                        delta_x = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
                                        delta_y = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
                                        delta_w = abs(bbox_w - prev_bbox_w)/float(prev_bbox_w)

                                        #Check if delta is small enough
                                        if((delta_x < MAX_DELTA_PCT_X) and (delta_y < MAX_DELTA_PCT_Y) and (delta_w < MAX_DELTA_PCT_W)):

                                            prev_bbox = bbox

                                            segment_frame_dict = {}

                                            segment_frame_dict[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY] = elapsed_video_s

                                            segment_frame_dict[FACE_EXTRACTION_FRAME_COUNTER_KEY] = sub_frame_counter

                                            segment_frame_dict[FACE_EXTRACTION_TAG_KEY] = sub_face[FACE_EXTRACTION_TAG_KEY]

                                            segment_frame_dict[FACE_EXTRACTION_CONFIDENCE_KEY] = sub_face[FACE_EXTRACTION_CONFIDENCE_KEY]

                                            segment_frame_dict[FACE_EXTRACTION_BBOX_KEY] = bbox

                                            segment_frames_list.append(segment_frame_dict)

                                            del frames[sub_frame_counter][FACE_EXTRACTION_FACES_KEY][sub_face_counter]

                                            prev_frame_counter = sub_frame_counter

                                            consecutive_frames_with_missed_detection = 0

                                            break; #Do not consider other faces in the same frame
                                        else:
                                            print 'delta_x = ' + delta_x
                                            print 'delta_y = ' + delta_y
                                            print 'delta_w = '

                                    sub_face_counter = sub_face_counter + 1
                                    
                                sub_frame_counter = sub_frame_counter + 1

                            # Aggregate results from all frames in segment
                            [final_tag, final_confidence] = aggregate_frame_results(segment_frames_list, self.face_models)

                            segment_dict[FACE_EXTRACTION_TAG_KEY] = final_tag

                            segment_dict[FACE_EXTRACTION_CONFIDENCE_KEY] = final_confidence

                            segment_dict[FACE_EXTRACTION_FRAMES_KEY] = segment_frames_list

                            segments.append(segment_dict)

                            face_counter = face_counter + 1
                            
                    frame_counter = frame_counter + 1  

        processing_time_in_clocks = cv2.getTickCount() - start_time
        processing_time_in_seconds = processing_time_in_clocks / cv2.getTickFrequency()

        # Populate dictionary with results
        results = {}
        results[FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY] = processing_time_in_seconds
        results[FACE_EXTRACTION_ERROR_KEY] = error
        results[FACE_EXTRACTION_TOT_FRAMES_NR] = frame_counter

        if(USE_TRACKING):
            
            results[FACE_EXTRACTION_SEGMENTS_KEY] = segments

        else:

            results[FACE_EXTRACTION_FRAMES_KEY] = frames
            
        self.progress = 100
        handle=time.time()
        self.db_result4image[handle]=results

        return handle
        
        
    def wait(self, handle):
        '''
        Wait until the task associated with the given handle has completed.
        If the handle is invalid, this method is ignored.
        TODO: alternatively, a callback mechanism could be provided

        :type  handle: integer ?
        :param handle: the task handle
        '''
        pass

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
    
    def getProgress(self, handle):
        '''
        Return an integer between 0 and 100 indicating the execution progress of the face extraction task.
            0: queued
            100: completed
            any value between 0 and 100: running
        Raise an exception if an error was encountered during the face extraction.

        :type  handle: integer
        :param handle: the task handle
        '''
        pass
