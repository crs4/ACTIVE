# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep
from job_manager.job.job_manager import JobManager
from job_manager.job.job import Job

"""
This module defines all tests necessary to evaluate the correctness
of the job monitor functionalities.
"""

delay = 1

# some sample function used to build jobs
def increase(val):
	sleep(delay)
	return val + 1

def incr(val):
	print "Calcolo eseguito su", val
	return val + 1

def multiply(val):
	sleep(delay)
	return val * 2

def identity(val):
	sleep(delay)
	return val

def bad_division(val):
        sleep(delay)
        return val/0

def prova():
	js   = JobManager()
	for i in range(8):
		print "Job numero ", i
		seq = Seq(increase)
		ext = Executor()
		job = Job(ext, (seq, 2), "prova")
		js.addJob(job)
	js.start()
	return js	


class TestJobManager(TestCase):
	"""
	Set of tests used to check JobManager functionalities
	"""
	def test_job_manager(self):
		"""
		Test used to check if a Job Manager could be instantiated without any error.
		"""
		try:
			jm = JobManager()
			jm.start()
			jm.stop()
			self.assertTrue(True)
		except Exception as e:
			self.assertTrue(False)

	def test_add_job(self):
		"""
		Test the method addJob, adding a simple Job which increase the
		input value by one.
		The job is not executed but only added to the execution queue.
		"""
		jm = JobManager()
		job = Job(increase, (1,))
		job.user = 1
		jm.addJob(job)
		self.assertEqual(1, len(jm.getJobs('QUEUED', 1)))
	
	def test_add_job2(self):
		"""
		Test the method addJob, adding a simple Job which increase the
		input value by one.
		The job is not executed but only added to the execution queue.
		"""
		jm = JobManager()
		job = Job(increase, (1,))
		job.user = 1
		job_id = jm.addJob(job)
		self.assertEqual(job_id, job.id)

	def test_job_execution(self):
                """
                Test used to check if a Job Manager is able to execute a job.
		The considered job is a simple increase function.
                """
                job = Job(increase, (1,))
		jm = JobManager()
                jm.start()
		jm.addJob(job)
		# wait that the job is moved to the running queue
		sleep(delay + 2)

		# checking if job result is correct
		self.assertEqual(2, job.result)
                jm.stop()

	def test_job_execution2(self):
                """
                Test used to check if a Job Manager is able to execute multiple jobs.
                """
                # creating and starting a job manager
                jm = JobManager()
                jm.start()
                # creating and adding many jobs to the manager
		num_jobs = 5
		for i in range(num_jobs):
			job = Job(increase, (2,))
			job.user = 1
			jm.addJob(job)

		sleep(num_jobs + 1)

                # checking if all jobs has been completed
		if(len(jm.getAllJobs(1)["COMPLETED"]) != num_jobs):
			self.assertTrue(False)
		else:
			# checking if all jobs results are correct
			for job_id in jm.getAllJobs(1)["COMPLETED"]:
				job = jm.getJob(job_id, 1)
				self.assertTrue(3, job.result)
                jm.stop()

	def test_job_execution3(self):
		"""
		Test used to check if the job manager detect and handle
		correctely an exception during job execution.
		"""
		jm = JobManager()
		jm.start()
		job = Job(bad_division, (2,))
		job.user = 1
		jm.addJob(job)

		sleep(2)
		self.assertEqual(1, len(jm.getJobs('FAILED', 1)))
		jm.stop()

	def test_job_get(self):
		"""
		Test used to check if the Job Manager is ablke to retrieve the
		correct Job object by its id.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		jm.addJob(job)
		
		sleep(2)
		self.assertIsNotNone(jm.getJob(job.id, job.user))
		jm.stop()

	def test_job_get2(self):
		"""
		Test used to check if the Job Manager is ablke to retrieve the
		correct Job object by its id.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		job_id = jm.addJob(job)
		
		sleep(2)
		self.assertEqual(job_id, jm.getJob(job_id, job.user).id)
		jm.stop()

	def test_job_abort(self):
		"""
		Test used to cancel the execution of a job by its id.
		A sample job is runned and then stopped.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		jm.addJob(job)
		
		self.assertTrue(jm.abortJob(job.id, job.user))
		jm.stop()

	def test_job_abort2(self):
		"""
		Test used to cancel the execution of a job by its id.
		A sample job is runned and then stopped.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		jm.addJob(job)
		
		jm.abortJob(job.id, job.user)
		job = jm.getJob(job.id, job.user)
		self.assertEqual('ABORTED', job.status)
		jm.stop()

	def test_job_clean(self):
		"""
		Test used to remove completed or aborted jobs from the
		Job Manager queues.
		A sample job is runned, waited and the cleaned.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		jm.addJob(job)
		
		sleep(2)
		jm.cleanJobs(job.user)
		self.assertIsNone(jm.getJob(job.id, job.user))
		jm.stop()

	def test_job_clean2(self):
		"""
		Test used to cancel the execution of a job by its id.
		A sample job is runned and then stopped.
		"""
		jm = JobManager()
                jm.start()
                job = Job(increase, (2,))
                job.user = 1
                jm.addJob(job)

                jm.cleanJobs(job.user)
		sleep(2)
                self.assertEqual('COMPLETED', jm.getJob(job.id, job.user).status)
                jm.stop()

	def test_job_get_all(self):
		"""
		Test used to check if the Job Manager is ablke to retrieve the
		correct Job object by its id.
		"""
		jm = JobManager()
		jm.start()
		for i in range(5):
			job = Job(increase, (2,))
			job.user = 1
			jm.addJob(job)
		
		sleep(5)
		self.assertEqual(5, len(jm.getJobs('COMPLETED', 1)))
		jm.stop()

	def test_job_get_all2(self):
		"""
		Test used to check if the Job Manager is ablke to retrieve the
		correct Job object by its id.
		"""
		jm = JobManager()
		jm.start()
		for i in range(5):
			job = Job(increase, (2,))
			job.user = 1
			jm.addJob(job)
		
		sleep(0.2)
		self.assertEqual(5, len(jm.getAllJobs(1)['RUNNING']))
		sleep(5)
		jm.stop()
	 

class TestSkeletonJobs(TestCase):
	"""
	Test suite used to check if it is possible to execute some jobs
	using the Job Manager with different users.
	"""

	def test(self):
		"""
		Test the distribution of the percentage of completed stages over a skeleton.
		"""
		js   = JobManager()
		pipe = Pipe(Seq(increase), Seq(increase))
		ext = Executor()
		job = Job(ext, (pipe, 100))
		js.addJob(job)
		js.start()

		#Read the progress variable to check the percentage of completed stages.
		percentage = []	
		while(True):
			val = ext.get_progress()
			if(val not in percentage):
				percentage.append(val)
			if(val == 100):
				break
			sleep(1)

		self.assertEqual(percentage, [0, 50, 100])
		js.stop()	

class TestUserJobs(TestCase):
	"""
	Class used to test the Job Manager functionalities when there are different
	users creating and executing differnt jobs.
	"""
	def test_user(self):
		"""
		Test used to retrieve all jobs of a given user.
		"""
		jm = JobManager()
		jm.start()
		job1 = Job(increase, (2,))
		job1.user = 1
		jm.addJob(job1)

		sleep(2)
		self.assertEqual(1, len(jm.getJobs('COMPLETED', 1)))
		jm.stop()

	def test_user2(self):
		"""
		Test used to retrieve all jobs of a user on many.
		"""
		jm = JobManager()
		jm.start()
		for i in range(3):
			job = Job(increase, (2+i,))
			job.user = i
			jm.addJob(job)

		sleep(2)
		self.assertEqual(1, len(jm.getJobs('COMPLETED', 1)))
		jm.stop()

	def test_user3(self):
		"""
		Test used to retrieve one job on many user's jobs.
		"""
		jm = JobManager()
		jm.start()
		for i in range(30):
			job = Job(increase, (2+i,))
			job.user = 1
			jm.addJob(job)
		
		job = Job(increase, (2,))
		job.user = 2
		jm.addJob(job)

		sleep(10)
		self.assertEqual(1, len(jm.getJobs('COMPLETED', 2)))
		jm.stop()

	def test_user_get(self):
		"""
		Test used to retrieve one job on many user's jobs.
		"""
		jm = JobManager()
		jm.start()
		job = None
		for i in range(10):
			job = Job(increase, (2+i,))
			job.user = 1
			jm.addJob(job)
		
		sleep(2)
		self.assertTrue(jm.getJob(job.id, 1))
		jm.stop()

	def test_user_abort(self):
		"""
		Test used to stop the execution of a job by its owner.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (6,))
		job.user = 1
		jm.addJob(job)
		
		self.assertTrue(jm.abortJob(job.id, 1))
		jm.stop()
	
	def test_user_abort2(self):
		"""
		Test used to stop the execution of a given job by another user.
		"""
		jm = JobManager()
		jm.start()
		job = Job(increase, (2,))
		job.user = 1
		jm.addJob(job)
		
		self.assertFalse(jm.abortJob(job.id, 2))
		jm.stop()

	def test_user_clean(self):
		"""
		Test used to clean all completed jobs of a specific user.
		"""
		jm = JobManager()
		jm.start()
		for i in range(3):
			job = Job(increase, (2+i,))
			job.user = 1
			jm.addJob(job)
		
		sleep(6)
		jm.cleanJobs(1)
		self.assertEqual(0, len(jm.getJobs('COMPLETED', 1)))
		jm.stop()












class TestJobManager2(TestCase):
	"""
	Set of tests used to check JobManager functionalities
	"""
	def test_job_manager(self):
		"""
		Test used to check if a Job Manager could be instantiated without any error.
		"""
		jm = JobManager()
		jm.start()
		jm.stop()
		self.assertTrue(True)

	def test_add_job(self):
		"""
		Test the method addJob, adding a simple Job which increase the
		input value by one.
		"""
		jm = JobManager()
		job = Job(increase, (1,))
		job.user = 1
		jm.addJob(job)
		self.assertEqual(1, len(jm.getJobs('QUEUED', 1)))

	def test_job_execution(self):
                """
                Test used to check if a Job Manager is able to execute a job.
		The considered job is a simple increase function.
                """
                job = Job(increase, (1,))
		jm = JobManager()
                jm.start()
		jm.addJob(job)

		sleep(delay + 2) # wait that the job is moved to the running queue

		# checking if job result is correct
		self.assertEqual(2, job.result)
		# stopping job manager
                jm.stop()

	def test_jobs_execution(self):
                """
                Test used to check if a Job Manager is able to execute multiple jobs.
                """
                # creating and starting a job manager
                jm = JobManager()
                jm.start()
                # creating and adding many jobs to the manager
		num_jobs = 9
		for i in range(num_jobs):
			job = Job(increase, (2,))
			job.user = 1
			jm.addJob(job)

		sleep(num_jobs + 1)

                # checking if all jobs has been completed
		if(len(jm.getAllJobs(1)["COMPLETED"]) != num_jobs):
			self.assertTrue(False)

		# checking if jobs results are correct
		for job_id in jm.getAllJobs(1)["COMPLETED"]:
			job = jm.getJob(job_id, 1)
			if(job.result != 3):
				self.assertTrue(False)

                # stopping job manager
                jm.stop()

	def ttest33333(self):
                """
                Test used to check if a Job Manager is able to execute multiple jobs.
                """
                # creating and starting a job manager
                jm = JobManager()
                jm.start()
                # creating and adding many jobs to the manager
		num_jobs = 10
		for i in range(num_jobs):
			job = Job(increase, (2,))
			job.user = 1
			jm.addJob(job)

		for job in jm.getAllJobs(1)["QUEUED"]:
			job_id = job.id
			job2 = jm.getJob(job_id, 1)
			if(not job2):
				self.assertTrue(False)

                # stopping job manager
                jm.stop()

	def test_failed_job(self):
		"""
		Test used to check if the job manager detect and handle
		correctely an exeception during job execution.
		"""
		jm = JobManager()
		job1 = Job(increase, (2,))
		job1.user = 1
		job2 = Job(bad_division, (2,))
		job2.user = 1
		jm.addJob(job1)
		jm.addJob(job2)
		
		jm.start()
		sleep(2)
		jm.stop()

		
		if(len(jm.getJobs('FAILED', 1)) != 1 or len(jm.getJobs('COMPLETED', 1)) != 1):
			self.assertTrue(False)


