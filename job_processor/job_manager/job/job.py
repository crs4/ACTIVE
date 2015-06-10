"""
Module used to define the structure of Job objects.
Jobs will be executed by the Job Manager and are used to
embed user functions.

It has been defined different type of jobs, depending on the
type of executions and expected parameters. All Jobs inherits the
main fields and methods from the class Job.
"""

from abc import abstractmethod
from skeleton.visitors import Executor
from skeleton.skeletons import Seq
import uuid
import time
import logging

# variable used for logging purposes
logger = logging.getLogger('job_processor')


class Job:
    """
    This class is used as a wrapper of a generic user function.
    Activities could be simple functions or parallel/distributed computations.
    For each job it is possible to specify the list of related data necessary
    for its executions.
    """

    def __init__(self, func, args):
        """
        Constructor used to initialize all job fields.

        @param func: The function that will be executed (or a callable object).
        @type func: Callable object
        @param args: Function arguments needed to execute the function.
        @type args: List of objects
        @param name: Optional parameter for job description.
        @type name: string
        """
        self.id = str(uuid.uuid4())
        self.args = args
        self.executor = func
        self.name = None
        self.func_name = None
        self.user_token = None # job owner's token
        self.user_id = None    # job owner's id
        self.status = None     # job processing status
        self.result = None     # field containing the result data
        self.progression = self.compute_progress  # function used to compute the job execution progress
        self.start_time = None # timestamp reporting when a job has been started
        self.end_time = None   # timestamp reporting when a job has been finished
        self.error_info = None # container of error information (if any)

    def __call__(self, args=None):
        """
        Function used to execute the provided input function, applying it to
        its parameter. It returns the results and handle the error raising (if any).

        @param args: Input parameter for the callable function (actually not used).
        @type args: List of objects
        @return: The result of the computation or None if an exception is raised.
        @rtype: Object
        """
        try:
            logger.debug('Executing job ' + self.name)
            self.__set_start_end()
            self.result = apply(self.executor, self.args)
        except Exception as ex:
            print ex
            self.error_info = ex
            self.result = None
        finally:
            self.__set_start_end()

        return self.result

    def __repr__(self):
        """
        Return a string representation of the current job.

        @return: String with jobID and name.
        @rtype: String
        """
        return str(self.id) + " - " + self.name

    def duration(self):
        """
        Function used to compute the duration of a computation.
        If the job is finished it returns the amount of milliseconds
        needed to complete the activities.
        Otherwise it returns the total milliseconds elapsed from the
        start of the job to the current time.

        @return: Milliseconds elapsed from the job start and the job stop (if any).
        @rtype: int
        """
        if self.end_time:
            return self.end_time - self.start_time
        return int(round(time.time()*1000)) - self.start_time

    def __set_start_end(self):
        """
        Function used to toggle the job chronometer.
        If it is stopped (no start time initialized) it set the
        a start time to the current timestamp. If it is started it
        set the end time to the current timestamp.
        """
        if self.start_time:
            self.end_time = int(round(time.time()*1000))
        else:
            self.start_time = int(round(time.time()*1000))

    def get_result(self):
        """
        Function used to return the result of job computation
        if it is finished, otherwise it returns None.
        """
        return self.result

    @abstractmethod
    def compute_progress(self):
        pass

    @abstractmethod
    def stop(self, info=None):
        pass


class PlainJob(Job):
    """
    This class is used as a wrapper in order to detect processing progress
    for activities based on simple functions.
    """

    def compute_progress(self):
        """
        Basic function used to detect processing progress.
        """
        if self.status == 'COMPLETED':
            return 100
        return 0

    def stop(self, info=None):
        if info:
            self.error_info = info


class DistributedJob(Job):
    """
    This class is used as a wrapper for the distributed computing of a function over
    one of the available cluster nodes (workers). It uses just one of the available
    skeletons to ensure that the function is distributed over the cluster.
    """

    def __call__(self, args=None):
        try:
            self.__set_start_end()
            # create a sequential skeleton
            skel = Seq(self.executor)
            # evaluate it with an executor
            self.result = Executor().eval(skel, self.args)
        except Exception as ex:
            print ex
            self.error_info =  ex
            self.result = None
        finally:
            self.__set_start_end()
        return self.result

    def compute_progress(self):
        """
        Basic function used to detect processing progress.
        """
        if self.status == 'COMPLETED':
            return 100
        return 0

    def stop(self, info=None):
            if info:
                    self.error_info = info


class SkeletonJob(Job):
    """
    This class is used as a wrapper in order to detect processing progress
    for activities based on structured skeletons.
    """
    def compute_progress(self):
        """
        Function used to detect processing progress based on skeleton
        executors.
        """
        return self.executor.get_progress()

    def stop(self, info=None):
        if info:
            self.error_info = info
        self.executor.abort()
