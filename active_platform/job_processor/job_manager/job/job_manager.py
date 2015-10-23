import time
from collections import OrderedDict
from multiprocessing.dummy import Pool

"""
This class is used to define a Job Manager, in order to
handle the execution of generic activities (Job objects).
A Job Manager executes a limited number of jobs at time and
then save their information in different queues (dictionaries)
based on the computation status.
So it is possibile to obtain job objects queued, in a running status,
completed or failed due to some computation error.
"""
class JobManager:
	def __init__(self, max_jobs=12):
		"""
		A Job Managar is able to manage a limited number
		of job at the same time. This degree of parallelism
		is customizable with a parameter.
		Jobs are stored in different dictionaries based on their
		execution status. Dictionaries has been used in order to
		simplify all searches based on job ids.
		:param max_jobs: Max number of jobs executed concurrently.
		"""
		self.__queuedJobs    = OrderedDict()	# set of jobs waiting for execution
		self.__runningJobs   = OrderedDict()	# set of jobs that are running 
		self.__failedJobs    = {}		# set of jobs that failed due to some error
		self.__completedJobs = {}		# set of jobs completed with no errors
		self.__max_jobs = max_jobs		# max num of jobs that could be handled
		self.__flag = False			# flag used to start and stop jobs management
		self.__pool = Pool(self.__max_jobs + 1) # thread pool used to execute jobs asynchronously
		self.__async_job_ref = {}		# dictionary used to maintain a reference to asynch results

	def addJob(self, job):
		"""
		Method used to add a job for execution.
		Job is always queued and it will be executed
		only if job manager is started and there are
		available computational resources.

		@param job: Job that will be queued an then executed.
		@type job: Job object
		@return: The id of the new added Job object.
		@rtype: String
		"""
		job.status = "QUEUED"
		self.__queuedJobs[job.id] = job
		return job.id

	def getAllJobs(self, user_id):
		"""
		This method is used to return a dictionary containing all jobs stored
		and handled by the job manager during its execution.
		For each computational status it has been defined the list of job in
		that state.

		@param user_id: Id of the user that requires all stored jobs.
		@type user_id: int
		@return: The dictionary of job lists indexed by their computational status.
		@rtype: Dict of list of Job objects
		"""
		temp = {"FAILED"   : [job for job in self.__failedJobs.values()    if str(job.user) == str(user_id)],
			"COMPLETED": [job for job in self.__completedJobs.values() if str(job.user) == str(user_id)],
			"RUNNING"  : [job for job in self.__runningJobs.values()   if str(job.user) == str(user_id)],
			"QUEUED"   : [job for job in self.__queuedJobs.values()    if str(job.user) == str(user_id)]}

		return temp

	def getJobs(self, status, user_id):
		"""
		This method returns a list of Job objects based on the computational state
		specified as parameter.
		Valid values for status paramters are: "FAILED", "COMPLETED", "RUNNING", "QUEUED" 
		It will return None if a not valid status is provided  

		@param status: The status of the jobs that will be returned in a list.
		@type status: String
		@param user_id: Id of the user that requested all stored jobs.
		@type user_id: int
		@return: A list of jobs with the requested computational status, None if the parameter is not valid.
		@rtype: List of Job objects
		"""
		return self.getAllJobs(user_id)[status]

	def getJob(self, job_id, user_id):
		"""
		Method used to return the Job object with the specified id (if any).
		If there is no Job with the parameter id it will return None.
		This method search first on all jobs queued, then on all jobs running
		and finally on completed or failed jobs.

		@param job_id: Id of the requested Job object.
		@type job_id: int
		@param user_id: Id of the user that requested a specific Job objects.
		@type user_id: int
		@return: The requested Job object, None if it doesn't exists.
		@rtype: Job object
		"""
		job_id = str(job_id)	# cast inaspettato: dovrebbe essere una stringa!
		job = None
		if job_id in self.__queuedJobs:
			job = self.__queuedJobs[job_id]
		elif job_id in self.__runningJobs:
			job = self.__runningJobs[job_id]
		elif job_id in self.__completedJobs:
			job = self.__completedJobs[job_id]
		elif job_id in self.__failedJobs:
			job = self.__failedJobs[job_id]
		# check user ownership
		if job is not None and str(job.user) == str(user_id):
			return job
		return None

	def abortJob(self, job_id, user_id):
		"""
		Method used to stop the execution of a Job
		using its id as parameter.
		If a job is still queued it is removed from the queue.
		Otherwise if it is remove it will be stopped and then
		removed from the execution queue.

		@param job_id: Id of the job that will be stopped.
		@type job_id: int
		@param user_id: Id of the user that request the job cancelling.
		@type user_id: int
		@return: The result of object cancellation.
		@rtype: bool
		"""
		# move the job to the failed queue
		if job_id in self.__queuedJobs:	# looking for queued jobs
			job = self.__queuedJobs[job_id]
			if str(job.user) == str(user_id):
				del self.__queuedJobs[job_id]
				job.status = "ABORTED"
				self.__failedJobs[job_id] = job
				return True

		if job_id in self.__runningJobs:	# looking for running jobs
			job = self.__runningJobs[job_id]
			if str(job.user) == str(user_id):
				job.status = "ABORTED"
				job.stop("JOB ABORTED")
				del self.__runningJobs[job_id]
				del self.__async_job_ref[job_id]
				self.__failedJobs[job_id] = job
				return True	
		
		return False


	def cleanJobs(self, user_id):
		"""
		Method used to remove all objects containing information
		about completed or failed jobs.
		Dictionaries containing jobs are cleared.

		@param user_id: Id of the user that request the job cleaning.
		@type user_id: int
		"""
		for job in self.__failedJobs.values():
			if str(job.user) == str(user_id):
				del self.__failedJobs[job.id]

		for job in self.__completedJobs.values():
			if str(job.user) == str(user_id):
				del self.__completedJobs[job.id]

	def start(self):
		"""
		This method allow to start the job manager in order to
		execute all queued jobs, based on available resources.
		Job handling is started as an asynchronous job and it
		will be executed automatically.
		"""
		self.__flag = True
		self.__pool.apply_async(self.__manage)


	def stop(self):
		"""
		This method stops the job manager thread execution,
		if it has been previously started.
		It doesn't stop the execution of job in the running state, these
		jobs will continue to compute asynchronously.
		"""
		self.__flag = False

	def __manage(self):
		"""
		This method implement the core function of the Job Manager.
		It is responsible for the correct handling of job execution, labelling each
		job with the correct computational status.
		An internal flag is used to interrupt the job handling if needed.
		At each iteration this method look if there is any available resource for job execution;
		if any, it moves some jobs from the waiting queue to the running queue, set the start time
		and execute the job asynchronously.
		Then it looks for the first job in the execution queue and it detect if it is finished or
		it is still running. In the former case set the end time and moves the job in the correct
		computational status queue (COMPLETED or FAILED) otherwise insert the job at the end of the queue.
		Then it starts again to execute the previous steps, if there is any job to execute.
		"""
		while True:
			# check if jobs handling has to be ended
			if(not self.__flag):
				break

			# if there are enough resources execute some queued jobs (if any)
			while len(self.__runningJobs) < self.__max_jobs and len(self.__queuedJobs) > 0:
				# get the job object from the returned couple
				job = self.__queuedJobs.popitem(last=False)[1]
				# run a job asynchronously
				self.__runningJobs[job.id] = job
				self.__async_job_ref[job.id] = self.__pool.apply_async(job)
				job.status = "RUNNING"
			
			# check the status of the first running job
			if len(self.__runningJobs) > 0:
				# get the job object from the returned couple
				job = self.__runningJobs.popitem(last=False)[1]
				# if result not ready move the job to the end
				if(not self.__async_job_ref[job.id].ready()):
					self.__runningJobs[job.id] = job
				# if job is finished move it in the right list
				else:
					del self.__async_job_ref[job.id]
					if(job.error_info):
						job.status = "FAILED"
						self.__failedJobs[job.id] = job
					else:
						job.status = "COMPLETED"
						self.__completedJobs[job.id] = job
			

			# used to don't overload the CPU
			time.sleep(0.01)
