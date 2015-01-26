#---------------------------------------------------------
# This module defines the following classes of the ActiveTools API:
#   Processor
#
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
    def __init__(self, application, workers=None):
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
        pass
		
    def shutdown(self):
        '''
        Shutdown the processor, through the following procedure:
         1. the processor no longer accepts new tasks
         2. wait till all pending tasks are completed by the workers
         3. stop the processor and all workers.		
        '''
        pass

