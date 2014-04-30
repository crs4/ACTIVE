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
from enum import Enum
from face_detection import detect_faces_in_image
from face_recognition import recognize_face
from Utils import load_YAML_file
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
        
        self.db_resutl4image={}

    def extract_faces_from_image(self, resource_path):
        '''
        Launch the face extractor on one image resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''

        # Call synchronous method

    def extract_faces_from_image_sync(self, resource_path):
        '''
        Launch the face extractor on one image resource.
        This method is synchronous and returns a dictionary with the results.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        # Save processing time
        start_time = cv2.getTickCount();
        
        # Face detection
        detection_params = self.params[FACE_DETECTION_KEY];

        detection_result = detect_faces_in_image(resource_path, detection_params, False)

        face_bboxes = detection_result[FACE_DETECTION_FACES_KEY];
        face_images = detection_result[FACE_DETECTION_FACE_IMAGES_KEY];

        # Face recognition
        recognition_params = self.params[FACE_RECOGNITION_KEY];
        
        faces = [];
        count = 0;
        #face=cv2.imread(resource_path,cv2.IMREAD_GRAYSCALE);
        #face_images=[face]
        for face in face_images:
            face_dict = {};
            
            # Resize face
            resize_face = False;
            if(resize_face):
                new_size = (FACES_WIDTH, FACES_HEIGHT);
                face = cv2.resize(face, new_size);
            
            rec_result = recognize_face(face, self.face_models, recognition_params, False);
            tag = rec_result[PERSON_ASSIGNED_TAG_KEY];
            face_dict[FACE_EXTRACTION_TAG_KEY] = tag;
            face_dict[FACE_EXTRACTION_BBOX_KEY] = face_bboxes[count];
            faces.append(face_dict);
            count = count + 1;

        processing_time_in_clocks = cv2.getTickCount() - start_time;
        processing_time_in_seconds = processing_time_in_clocks / cv2.getTickFrequency();

        # Populate dictionary with results
        results = {};
        results[FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY] = processing_time_in_seconds;
        results[FACE_EXTRACTION_ERROR_KEY] = '';
        results[FACE_EXTRACTION_FACES_KEY] = faces;

        self.progress = 100;
        handle=time.time()
        self.db_resutl4image[handle]=results

        return handle
    
    def extractFacesFromVideo(self, resource):
        '''
        Launch the face extractor on one video resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        pass
        
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
          error: a string specyfing an error condition, or None if no errors occurred
          faces: a list of tags with associated associated bounding boxes
        Example:
            results = {'elapsed_cpu_time':  0.011,
                       'error': None,
		               'faces': ({'tag': 'Barack Obama', 'bbox':(100,210, 50, 50)},
                                 {'tag': 'Betty White',  'bbox':(30, 250, 40, 45)}
                                )
                      }
        For extractFacesFromVideo() a dictionary is returned with the following entries:
            TBD  
                   
        :type  handle: integer ?
        :param handle: the task handle
        '''
        return self.db_resutl4image[handle]
    
    def getProgress(self, handle):
        '''
        Return an integer between 0 and 100 indicating the execution progress of the face extraction task.
            0: queued
            100: completed
            any value between 0 and 100: running
        Raise an exception if an error was encountered during the face extraction.

        :type  handle: integer ?
        :param handle: the task handle
        '''
        pass
