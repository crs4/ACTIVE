import uuid
import time
from abc import abstractmethod

class Job:
	"""
	This class is used as a wrapper in order to incapsulate a generic activity
	related to item management. Activities could be simple functions or composed
	skeletons for parallel and distributed computations.
	For each job it is possible to detect also a list of other informations
	related to its execution and result.
	"""

	def __init__(self, func, args):
		"""
		:param func: The function that will be executed (or a callable object).
		:param args: Function arguments needed to execute the function.
		:param name: Optional parameter for job description.
		"""
		self.id = str(uuid.uuid4())
		self.args = args 
		self.executor = func
		self.name = None
		self.func_name = None
		self.status = None     # job processing status
		self.result = None     # field containing the result data
		self.progression = self.compute_progress  # function used to compute the job execution progress
		self.start_time = None # timestamp reporting when a job has been started
		self.end_time = None   # timestamp reporting when a job has been finished
		self.error_info = None # container of error information (if any)
	
	def __call__(self, args=None):
		"""
		Function used to execute the provided input function to the job, applying it to
		its parameter. It returns the results and handle the error raising (if any).
		:param args: Input parameter for the callable function (actually not used).
		:returns: The result of the computation or None if an exception is raised.
		"""
		try:
			self.set_start_end()
			self.result = apply(self.executor, self.args)
		except Exception as ex:
			self.error_info =  ex
			self.result = None
		finally:
			self.set_start_end()

		return self.result

	def __repr__(self):
		"""
		Function that allows to obtain a string representation.
		"""
		return str(self.id)

	def duration(self):
		"""
		Function used to compute the duration of a computation.
		If the job is finished it returns the amount of milliseconds 
		needed to complete the activities.
		Otherwise it returns the total milliseconds elapsed from the
		start of the job to the current time.
		:returns: The total milliseconds elapsed from the job start and the job stop (if any).
		"""
		if(self.end_time):
			return self.end_time - self.start_time
		return int(round(time.time()*1000)) - self.start_time

	def set_start_end(self):
		"""
		Function used to toggle the job chronometer.
		If it is stopped (no start time initialized) it set the
		a start time to the current timestamp. If it is started it
		set the end time to the current timestamp.
		"""
		if(self.start_time):
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
	for activities based on simple fuctions.
	"""
	def compute_progress(self):
		"""
		Basic function used to detect processing progress.
		"""
		if(self.result):
			return 100
		return 0

	def stop(self, info=None):
		if(info):
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
		if(info):
                        self.error_info = info
		self.executor.abort()
