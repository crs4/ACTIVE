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

def bad_division(val):
	sleep(1)
	return val/0

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

	def test_add_job(self):
		"""
		Test the method addJob.
		"""
		jm = JobManager()
		job = Job(increase, (1,))
		jm.addJob(job)
		self.assertEqual(1, len(jm.getJobs('QUEUED')))

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

		sleep(2) # wait that the job is moved to the running queue

		# checking if job result is correct
		self.assertEqual(2, job.result)
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
		num_jobs = 9
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
			jm.addJob(job)

		for job in jm.getAllJobs()["QUEUED"]:
			job_id = job.id
			job2 = jm.getJob(job_id)
			if(not job2):
				self.assertTrue(False)

                # stopping job manager
                jm.stop()

	def ttest4(self):
		"""
		Test the distribution of the percentage of completed stages over a skeleton.
		"""
		js   = JobManager()
		pipe = Pipe(Seq(increase), Seq(increase))
		ext = Executor()
		job = Job(ext.eval, (pipe, 100))
		js.addJob(job)
		js.start()

		#Read the progress variable to check the percentage of completed stages.
		percentage = []	
		while(True):
			if(ext.progress not in percentage):
				percentage.append(ext.progress)
			if(ext.progress == 100):
				break
			sleep(1)
		self.assertEqual(percentage, [0, 50, 100])
		js.stop()	

	def test5(self):
		jm = JobManager()
		job = Job(increase, (2,))
		jm.addJob(job)
		#Raise InfiniteDivisionException
		job = Job(bad_division, (2,))
		jm.addJob(job)
		jm.start()
		sleep(2)
		jm.stop()
		#
		if(len(jm.getJobs('FAILED')) != 1 or len(jm.getJobs('COMPLETED')) != 1):
			assertTrue(False)
		
	

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
