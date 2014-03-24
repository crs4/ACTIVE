

#---------------------------------------------------------
# ActiveCore API
#---------------------------------------------------------
# TODO:
#  - define and list custom exceptions!!
#  - configure sphynx to generate documentation
#
# ALL METHODS ARE BLOCKING, UNLESS SPECIFIED OTHERWISE
#
# Configuration parameters:
#   Key          Value
#   ...          ...
#---------------------------------------------------------

class Processor(object):
	'''
	The processor allows to execute tasks in parallel on N workers.
	It also provides a mechanism for updating the status of all workers.
	'''
	def __init__(self, workers=None, application):
		'''
		Initialize the communications with all workers.
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
	This is a shared resource which is replicated on each worker.
	'''
	def __init__(self, processor, db_path=None):
		'''
		Initialize the training set on all workers.
		
		:type  workers: list of strings
		:param workers: the address (IP and port) of workers.
		
		:type  db_path: string
		:param db_path: a file containg the dump of the training set database
		'''
		pass
		
	def add_faces(self, files_or_images, tag):
		'''
		Add new faces to the training set and associate them with the given tag.
		It is resposibility of the caller to provide valid faces.
		No check is done on invalid or duplicated faces.
		If the ActiveCore configuration is based on a set of workers, the method is propagated to each worker.
		
		:type  files_or_images: an Image object, or a string, or a list of Image objects, or a list of strings
		:param files_or_images: faces to be added to the training set
		
		:type  tag: string
		:param tag: the tag associated to the face to be added to the training set
		'''

	def remove_tags(self, tag=None):
		'''
		Remove the given tags (and all associated faces) from the training set.
		If tags=None, all tags are removed from the training set (i.e. the training set is cleared).
		If any of the provided tags is not in the training set, the tag is ignored.
		
		:type  tag: string or list of strings
		:param tag: the tags associated to the face to be added to the training set
		'''

	def rename_tag(self, old_tag, new_tag, blocking=True):
		'''
		Rename a tag in the training set.
		Raise an exception if old_tag does not exist in training set.
		Raise an exception if new_tag already exists in training set.
		
		:type  old_tag: string
		:param old_tag: a tag already present in the training set
		
		:type  new_tag: string
		:param new_tag: a tag not yet present in the training set
		'''

    def sync(self):
		'''
		Wait until all write operations to the training set have been propagated to all workers.
		'''

	def has_tag(self, tag):
		'''
		Return true if the tag is already in the training set.
		This call can be processed by any of the available workers, the caller is responsible for 
		ensuring that the training sets are aligned on all workers.
		
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
		'''

class FaceExtractor(object):
	'''
	Tool for detecting and recognizing faces in images and video.
	'''
    def __init__(self, training_set, params=None):
		'''
		Initialize the face extractor.
		The provided configuration parameters override default values.
		
		:type  training_set: a FaceRecognitionTrainingSet object
		:param training_set: the training set for the face recognition
		
		:type  params: dictionary 
		:param params: configuration parameters (see table)
		'''
        pass
	
	def extractFacesFromImage(self, id_s, resource, params=None):
		'''
		Launch the face extractor on one or more image resources.
		The provided configuration parameters override default values.
		This is a non-blocking call.
		Return a task handle.
		
		:type  resources: string
		:param resources: resource file path
				
		:type  params: dictionary 
		:param params: configuration parameters (see table)
		'''
		pass
		
	def extractFacesFromVideo(self, resource, params=None):
		'''
		Launch the face extractor on one or more video resources (asynchronous task).
		The provided configuration parameters override default values.
		This is non-blocking call.
		Return a task handle.
		
		:type  resources: string
		:param resources: resource file path
		
		:type  params: dictionary 
		:param params: configuration parameters (see table)
		'''
		pass
        
	def sync(self, handle):
		'''
		Wait until the task associated with the given handle has completed.
		
		:type  handle: integer ?
		:param handle: the task handle
		'''
		pass
		
    def getResults(self, handle):
		'''
		Return the results of the face extraction process.
		This call invalidates the specified handle.
		For extractFacesFromImage() a dictionary is returned with the following entries:
		  elapsed_cpu_time:  float  (the elapsed cpu time in sec)
		  error: a string specyfing an error condition, or None if the execution completed without errors
		  faces: a list of tags with associated associated bounding boxes
		example:
		
		    results = {'elapsed_cpu_time':  0.011,
		               'error': None,
		               'faces': ({'tag': 'Barack Obama', 'bbox':(100,210, 50, 50)},
		                         {'tag': 'Betty White',  'bbox':(30, 250, 40, 45)}
		                        )
		              }
		For extractFacesFromVideo() a dictionary is returned with the following entries:
          TBD                     
		'''
		pass
    
    def getProgress(self, handle):
		'''
		Return an integer between 0 and 100 indicating the the execution progress of the face extraction task.
		  0: queued
		  100: completed
		  any value between 0 and 100: running
        Raise an exception if an error was encountered during the face extraction.
		'''
