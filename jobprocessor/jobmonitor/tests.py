from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep
from jobmonitor.job_manager import JobManager
from jobmonitor.job import Job

"""
In this module it has been reported all test necessasy to evaluate
if job monitor functionalities had been implemented correctely.
"""

# some sample function used to build jobs
def increase(val):
	sleep(1)
	return val + 1

def multiply(val):
	sleep(1)
	return val * 2

def identity(val):
	sleep(1)
	return val


def prova():
	js   = JobManager()
	for i in range(8):
		print "Job numero ", i
		seq = Seq(increase)
		ext = Executor(seq, 2)
		job = Job(ext, {}, "prova")
		js.addJob(job)
	js.start()
	return js	


class TestJobManager(TestCase):
	"""
	Set of tests used to check JobManager functionalities
	"""

	def test1(self):
		"""
		Test used to check if a Job Manager could be instantiated without any error.
		"""
		jm = JobManager()
		jm.start()
		jm.stop()
		self.assertTrue(True)

	def test2(self):
                """
                Test used to check if a Job Manager is able to execute a job.
                """
		# creating a sample job and a job manager
		# function parameters are passed as a tuple 
                job = Job(increase, (1,))
		jm = JobManager()
		# starting the job manager and adding a job
                jm.start()
		jm.addJob(job)

		sleep(1) # wait that the job is moved to the running queue

		# checking if job result is correct
		self.assertEqual(2, job.result.get())
		# stopping job manager
                jm.stop()


	def test3(self):
                """
                Test used to check if a Job Manager is able to execute multiple jobs.
                """
                # creating and starting a job manager
                jm = JobManager()
                jm.start()
                # creating and adding many jobs to the manager
		num_jobs = 90
		for i in range(num_jobs):
			job = Job(increase, (2,))
			jm.addJob(job)

		sleep(num_jobs + 1)

                # checking if all jobs has been completed
		if(len(jm.getAllJobs()["COMPLETED"]) != num_jobs):
			self.assertTrue(False)

		# checking if jobs results are correct
		for job_id in jm.getAllJobs()["COMPLETED"]:
			job = jm.getJob(job_id)
			if(job.result.get() != 3):
				self.assertTrue(False)

                # stopping job manager
                jm.stop()

	

	# TODO: creare i test per i diversi metodi esposti dalla classe JobManager
 	"""
	def test_1(self):
		seq1 = Seq(increase)
		ext1 = Executor(seq1, 1)
		
		seq2 = Seq(multiply)
                ext2 = Executor(seq2, 2)

		seq3 = Seq(identity)
                ext3 = Executor(seq3, 8)

		js   = JobManager()
		js.addJob(ext1)
		js.addJob(ext2)
		js.addJob(ext3)
		js.start()

	def test_2(self):
		js   = JobManager()
		for i in range(80):
			seq = Seq(increase)
			ext = Executor(seq, 2)
			job = Job(ext, "prova")
			
			js.addJob(job)
		
		js.start()
	"""
