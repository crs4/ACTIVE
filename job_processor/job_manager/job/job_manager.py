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
		:param job: Job that will be queued an then executed. 
		"""
		job.status = "QUEUED"
		self.__queuedJobs[job.id] = job
		return job.id

	def abortJob(self, job_id):
		"""
		Method used to stop the execution of a Job
		using its id as parameter.
		If a job is still queued it is removed from the queue.
		Otherwise if it is remove it will be stopped and then
		removed from the execution queue.
		:param job_id: Id of the job that will be aborted.
		"""
		# move the job to the failed queue
		if(job_id in self.__queuedJobs):	# looking for queued jobs
			job = self.__queuedJobs[job_id]
			del self.__queuedJobs[job_id]
			job.status = "ABORTED"
			self.__failedJobs[job_id] = job

		elif(job_id in self.__runningJobs):	# looking for running jobs
			job = self.__runningJobs[job_id]
			job.status = "ABORTED"
			job.stop("JOB ABORTED")
			del self.__runningJobs[job_id]
			del self.__async_job_ref[job_id]
			self.__failedJobs[job_id] = job
			
		return True

	def cleanJobs(self):
		"""
		Method used to remove all objects containing information
		about completed or failed jobs.
		Dictionaries containing jobs are cleared.
		"""
		self.__failedJobs.clear()
		self.__completedJobs.clear()

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

	def getAllJobs(self):
		"""
		This method is used to return a dictionary containing all jobs stored
		and handled by the job manager during its execution.
		For each computational status it has been defined the list of job in
		that state.
		:returns: The dictionary of job lists indexed by their computational status.
		"""
		return {"FAILED"   : self.__failedJobs.values(),
			"COMPLETED": self.__completedJobs.values(),
			"RUNNING"  : self.__runningJobs.values(),
			"QUEUED"   : self.__queuedJobs.values()}

	def getJobs(self, status):
		"""
		This method returns a list of Job objects based on the computational state
		specified as parameter.
		Valid values for status paramters are: "FAILED", "COMPLETED", "RUNNING", "QUEUED" 
		It will return None if a not valid status is provided  
		:params status: The status of the jobs that will be returned in a list.
		:returns: A list of jobs with the requested computational status, None if the parameter is not valid.
		"""
		return self.getAllJobs()[status]

	def getJob(self, job_id):
		"""
		Method used to return the Job object with the specified id (if any).
		If there is no Job with the parameter id it will return None.
		This method search first on all jobs queued, then on all jobs running
		and finally on completed or failed jobs.

		:param job_id: Identifier of the Job object to return.
		:returns: Job with the specified id, None if it doesn't exists.
		"""
		job_id = str(job_id)	# cast inaspettato: dovrebbe essere una stringa!
		if(job_id in self.__queuedJobs):
			return self.__queuedJobs[job_id]
		elif(job_id in self.__runningJobs):
			return self.__runningJobs[job_id]
		elif(job_id in self.__completedJobs):
			return self.__completedJobs[job_id]
		elif(job_id in self.__failedJobs):
			return self.__failedJobs[job_id]
		else:
			return None

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
			while(len(self.__runningJobs) < self.__max_jobs and len(self.__queuedJobs) > 0):
				# get the job object from the returned couple
				job = self.__queuedJobs.popitem(last=False)[1]
				# run a job asynchronously
				self.__runningJobs[job.id] = job
				self.__async_job_ref[job.id] = self.__pool.apply_async(job)
				job.status = "RUNNING"			
			
			# check the status of the first running job
			if(len(self.__runningJobs) > 0):
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
