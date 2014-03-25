#---------------------------------------------------------
# ActiveCore API
#
# This is a very first draft of the programmatic API of Active Core.
# The documentation API shall be automatically generated using Sphynx.
# All methods are blocking, unless specified otherwise.
#
# To do:
#  - define and list custom exceptions!
#  - define configuration parameters
#  
#---------------------------------------------------------

class Processor(object):
    '''
    The processor allows to execute tasks in parallel on N workers.
    It also provides a mechanism for updating the status of all workers.
    '''
    def __init__(self, workers=None, application):
        '''
        Initialize the communications with workers.
        An exception is raised if any of the workers is not available.
        If workers=None, it is assumed that all API calls are executed locally in the same thread 
        of the caller (blocking calls).

        :type  workers: list of strings
        :param workers: the address (IP and port) of workers, e.g. "156.148.18.76:8001"
        '''
        pass
		
    def deploy(self, build_path):
        '''
        Trigger a deployment off the build machine to all workers.

        :type  build_path: string
        :param build_path: the full build path, including the host address
        '''
        pass
	    
    def start(self):
        '''
        Start the processor.
        All software versions on all workers shall be the same, otherwise an exception 
        is raised. 
        '''
		
    def shutdown(self):
        '''
        Shutdown the processor, through the following procedure:
         1. the processor no longer accepts new tasks
         2. wait till all pending tasks are completed by the workers
         3. stop the processor and all workers.		
        '''

class FaceRecognitionTrainingSet(object):
    '''
    Training set for the face recognition.
    TODO: Felice please suggest a better name for this class!
    This is a shared resource which is replicated on each worker.
    '''
    def __init__(self, processor, db_name):
        '''
        Initialize the training set on all workers.
        The caller is responsible for creating the connection with the database.
        The caller is also responsible for managing database backups.

        :type  workers: list of strings
        :param workers: the address (IP and port) of workers.

        :type  db_name: string
        :param db_name: the database name
        '''
        pass
		
    def add_faces(self, filenames_or_images, tag):
        '''
        Add new faces to the training set and associate them with the given tag.
        No check is done on invalid or duplicated faces (it is resposibility of the caller to provide valid faces).
        This method is asynchronous and is propagated to all workers.

        :type  filenames_or_images: an Image object, or a string, or a list of Image objects, or a list of strings
        :param filenames_or_images: faces to be added to the training set

        :type  tag: string
        :param tag: the tag associated to the face to be added to the training set
        '''

    def remove_tags(self, tags):
        '''
        Remove the given tag or tags (and all associated faces) from the training set.
        If any of the provided tags is not in the training set, the tag is ignored.
        This method is asynchronous and is propagated to all workers.

        :type  tags: string or list of strings
        :param tags: the tags associated to the face to be added to the training set
        '''

    def rename_tag(self, old_tag, new_tag, blocking=True):
        '''
        Rename a tag in the training set.
        Raise an exception if old_tag does not exist in training set.
        Raise an exception if new_tag already exists in training set.
        This method is asynchronous and is propagated to all workers.

        :type  old_tag: string
        :param old_tag: a tag already present in the training set

        :type  new_tag: string
        :param new_tag: a tag not yet present in the training set
        '''

    def sync(self):
        '''
        Wait until all asynchronous methods previously invoked have been executed by all workers.
        This method shall be called in order to ensure that training sets on all workers are aligned.
        '''

    def has_tag(self, tag):
        '''
        Return true if the tag is already in the training set.
        This call can be processed by any of the available workers (the caller is responsible for 
        ensuring that the training sets are aligned on all workers).

        :type  tag: string
        :param tag: the tag associated to a set of faces in the training set
        '''
        pass

    def get_tags(self):
        '''
        Return all tags of the training set as a list of strings.
        This call can be processed by any of the available workers, the caller is responsible for 
        ensuring that the training sets are aligned on all workers.
        '''
		
    def get_faces(self, tag):
        '''
        Return a list of serialized Image objects associated to the given tag in the training set, 
        or an empty list if the tag is not in the training set.
        TODO: provide detail about how to pickle/unpickle the Image object

        :type  tag: string
        :param tag: the tag associated to a set of faces in the training set
        '''

class FaceExtractor(object):
    '''
    Tool for detecting and recognizing faces in images and video.
    '''
    def __init__(self, training_set, params=None):
        '''
        Initialize the face extractor.
        The configuration parameters define and customize the face extraction algorithm.
        If any of the configuration parameters is not provided a default value is used.

        :type  training_set: a FaceRecognitionTrainingSet object
        :param training_set: the training set for the face recognition

        :type  params: dictionary 
        :param params: configuration parameters (see table)
        '''
        pass

    def extractFacesFromImage(self, resource_path):
        '''
        Launch the face extractor on one image resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        pass

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
        pass
    
    def getProgress(self, handle):
        '''
        Return an integer between 0 and 100 indicating the the execution progress of the face extraction task.
            0: queued
            100: completed
            any value between 0 and 100: running
        Raise an exception if an error was encountered during the face extraction.

        :type  handle: integer ?
        :param handle: the task handle
        '''
