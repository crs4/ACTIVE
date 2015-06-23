"""
In this module it has been reported all test necessasy to evaluate
if job monitor functionalities had been implemented correctely.
"""

from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep
from job_manager.job.job_manager import JobManager
from job_manager.job.job import Job

delay = 1


# some sample function used to build jobs
def increase(val):
    sleep(delay)
    return val + 1

def incr(val):
    print 'Computation executed on value ' + str(val)
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


def test_1():
    js   = JobManager()
    for i in range(8):
        print 'Executing Job ' + i
        seq = Seq(increase)
        ext = Executor()
        job = Job(ext, (seq, 2), "prova")
        js.addJob(job)
    js.start()
    return js


class TestJobManager(TestCase):
    """
    Set of tests used to check JobManager methods.
    """

    def test_job_manager(self):
        """
        Test used to check if a Job Manager could be instantiated without any error.
        """
        jm = JobManager()
        jm.start()
        jm.stop()
        self.assertTrue(True)

    def test_queued_job(self):
        """
        Test the method addJob, adding a simple Job which increase the
        input value by one.
        """
        jm = JobManager()
        job = Job(increase, (1,))
        jm.addJob(job)

        self.assertEqual(1, len(jm.getJobs('QUEUED')))
        jm.stop()

    def test_get_job(self):
        """
        Test used to retrieve a specific job as root user.
        """
        jm = JobManager()
        job = Job(increase, (1,))
        job.user_id = 1
        job_id = jm.addJob(job)

        job2 = jm.getJob(job_id)

        self.assertIsNotNone(job2)
        jm.stop()

    def test_get_job2(self):
        """
        Test used to retrieve a specific job as root user.
        """
        jm = JobManager()
        job = Job(increase, (1,))
        job.user_id = 1
        job_id = jm.addJob(job)

        job2 = jm.getJob(job_id, 1)

        self.assertIsNotNone(job2)
        jm.stop()

    def test_get_job3(self):
        """
        Test used to retrieve a specific job as root user.
        """
        jm = JobManager()
        job = Job(increase, (1,))
        job.user_id = 1
        job_id = jm.addJob(job)

        job2 = jm.getJob(job_id, 2)

        self.assertIsNone(job2)
        jm.stop()

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
            job.user_id = 1
            jm.addJob(job)

        sleep(2*num_jobs + 1)

        # checking if all jobs has been completed
        if len(jm.getJobs('COMPLETED')) != num_jobs:
            self.assertTrue(False)

        # checking if jobs results are correct
        for job in jm.getJobs('COMPLETED'):
            if job.result != 3:
                self.assertTrue(False)
        jm.stop()

    def test_multiple(self):
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
            job.user_id = 1
            jm.addJob(job)

        for job in jm.getAllJobs()["QUEUED"]:
            job_id = job.id
            job2 = jm.getJob(job_id)
            if not job2:
                self.assertTrue(False)
        jm.stop()

    def test_job_abort(self):
        """
        Test used to check id a job is correctly stopped
        and moved in the failed queue.
        """
        job1 = Job(increase, (1,))
        job1.user_id = 1
        job2 = Job(increase, (2,))
        job2.user_id = 2

        jm = JobManager()
        jm.start()
        job1_id = jm.addJob(job1)
        jm.addJob(job2)
        jm.abortJob(job1_id)

        sleep(0.1)
        self.assertTrue(job1.status == 'ABORTED')
        self.assertTrue(job2.status == 'RUNNING')
        jm.stop()

    def test_job_abort2(self):
        """
        Test used to check id a job is stopped
        only if requested by its owner.
        """
        job1 = Job(increase, (1,))
        job1.user_id = 1

        jm = JobManager()
        jm.start()
        job1_id = jm.addJob(job1)

        self.assertFalse(jm.abortJob(job1_id, 2))
        jm.stop()

    def test_job_clean(self):
        """
        Test used to check if the Job objects are correctly removed
        from the failed and completed queues of a specific user.
        """
        job1 = Job(increase, (1,))
        job1.user_id = 1
        job2 = Job(increase, (2,))
        job2.user_id = 2

        jm = JobManager()
        jm.start()
        jm.addJob(job1)
        jm.addJob(job2)
        sleep(2*delay)
        jm.cleanJobs(1)

        self.assertTrue(len(jm.getJobs('COMPLETED', 1)) == 0)
        jm.stop()

    def test_job_clean2(self):
        """
        Test used to check if the Job objects are correctly removed
        from the failed and completed queues of all users.
        """
        job1 = Job(increase, (1,))
        job1.user_id = 1
        job2 = Job(increase, (2,))
        job2.user_id = 2

        jm = JobManager()
        jm.start()
        jm.addJob(job1)
        jm.addJob(job2)
        sleep(2*delay)
        jm.cleanJobs()

        self.assertTrue(len(jm.getJobs('COMPLETED')) == 0)
        jm.stop()

    def test4(self):
        """
        Test the distribution of the percentage of completed stages over a skeleton.
        """
        js   = JobManager()
        pipe = Pipe(Seq(increase), Seq(increase))
        ext = Executor()
        job = Job(ext, (pipe, 100))
        js.addJob(job)
        js.start()

        # read the progress variable to check the percentage of completed stages.
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

    def test_failed_job(self):
        """
        Test used to check if the job manager detect and handle
        correctly an exception during job execution.
        """
        jm = JobManager()
        job1 = Job(increase, (2,))
        job2 = Job(bad_division, (2,))
        jm.addJob(job1)
        jm.addJob(job2)

        jm.start()
        sleep(2)
        jm.stop()


        if(len(jm.getJobs('FAILED')) != 1 or len(jm.getJobs('COMPLETED')) != 1):
            self.assertTrue(False)
