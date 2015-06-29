"""
This module contains all _tests necessasy to evaluate
if the JobManager had been implemented correctely.
All defined _test are used to check the internal API.
"""

from django.test import TestCase
from django.conf import settings
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep
from job_manager.job.job_manager import JobManager
from job_manager.job.job import Job
import requests
import json

# delay introduced for debug purposes
delay = 1

def increase(val, delay=delay):
    """
    Function used to increase by one the value of the input parameter.
    
    @param val: Input integer that will be increased by one.
    @type val: int
    @return: The input integer increased by one.
    @rtype: int
    """
    sleep(delay)
    return val + 1

def multiply(val):
    """
    Function used to multiply by two the input integer parameter.
    
    @param val: Input integer value.
    @type val: int
    @return: The input integer increased by one.
    @rtype: int
    """
    sleep(delay)
    return val * 2


def identity(val):
    """
    Function used to return the input integer parameter.
    
    @param val: Input integer value.
    @type val: int
    @return: The input integer value.
    @rtype: int
    """
    sleep(delay)
    return val

def bad_division(val):
    """
    Function used to divide by zero the input integer parameter.
    
    @param val: Input integer value.
    @type val: int
    @return: An exception due to the division by zero.
    @rtype: Exception
    """
    sleep(delay)
    return val/0


class TestJobManager():#TestCase):
    """
    Set of _tests used to check JobManager functionalities.
    """

    def _test_job_manager(self):
        """
        _test used to check if a Job Manager could be 
        instantiated without any error.
        """
        jm = JobManager()
        jm.start()
        jm.stop()
        self.assertTrue(True)

    def _test_queued_job(self):
        """
        _test the method addJob, adding a simple Job which increase the
        input value by one. The JobManager is not started.
        """
        jm = JobManager()
        job = Job(increase, (1,))
        jm.addJob(job)

        self.assertEqual(1, len(jm.getJobs('QUEUED')))
        jm.stop()
    
    def _test_running_job(self):
        """
        _test the method addJob, adding a simple Job which increase the
        input value by one and starting the JobManager.
        The Job object is associated to a long delay.
        """
        jm = JobManager()
        jm.start()

        delay = 5
        job = Job(increase, (1, 10))    
        jm.addJob(job)
        # wait that the job is moved in the running queue
        sleep(2)
        self.assertEqual(1, len(jm.getJobs('RUNNING')))
        
        delay = 1
        jm.stop()
        
    def _test_aborted_job(self):
        """
        _test used to check id a job is correctly stopped
        and moved in the failed queue.
        """
        job = Job(increase, (1, 5))
        job.user_id = 1

        jm = JobManager()
        jm.start()
        job_id = jm.addJob(job)
        jm.abortJob(job_id)

        sleep(0.1)
        self.assertTrue(job.status == 'ABORTED')
        jm.stop()

    def _test_completed_job(self):
        """
        _test used to check if a Job object is executed corretely by the Job Manager
        and moved in the correct queue.
        The considered job is a simple increase function.
        """
        job = Job(increase, (1,))
        jm = JobManager()
        jm.start()
        jm.addJob(job)

        # wait that the job is moved to the completed queue
        sleep(delay + 2)

        # checking if job result is correct
        self.assertEqual(2, job.result)
        jm.stop()
        
    def _test_failed_job(self):
        """
        _test used to check if the job manager detect and handle
        correctly an exception during job execution.
        """
        jm = JobManager()
        jm.start()
        job = Job(bad_division, (2,))
        jm.addJob(job)

        sleep(delay + 2)

        self.assertEqual(1, len(jm.getJobs('FAILED')))
        
        jm.stop()
        
    def _test_job_clean(self):
        """
        _test used to check if the Job objects are correctly removed
        from the failed and completed queues.
        """
        jm = JobManager()
        jm.start()
        
        job1 = Job(increase, (1,))
        job2 = Job(increase, (2,))
        jm.addJob(job1)
        jm.addJob(job2)
        
        sleep(2*delay)
        jm.cleanJobs()

        self.assertEqual([], jm.getJobs('COMPLETED'))
        self.assertEqual([], jm.getJobs('FAILED'))
        self.assertEqual([], jm.getJobs('QUEUED'))
        self.assertEqual([], jm.getJobs('RUNNING'))
        
        jm.stop()
    
    def _test_job_clean2(self):
        """
        _test used to check if only termnated Jobs objects are 
        removed from the failed and completed queues.
        """
        jm = JobManager()
        jm.start()
        # start the first job and wait for completion
        job1 = Job(increase, (1,))
        jm.addJob(job1)
        sleep(2)
        # start the second job with a bigger delay
        delay = 5
        job2 = Job(increase, (2,))
        jm.addJob(job2)
        # clean all terminated jobs
        jm.cleanJobs()
        sleep(6)

        self.assertEqual(1, len(jm.getJobs('COMPLETED')))
        self.assertEqual([], jm.getJobs('FAILED'))
                
        delay = 1
        jm.stop()
        
    def _test_job_clean_by_user(self):
        """
        _test used to check if only termnated Jobs objects are 
        removed from the failed and completed queues.
        """
        jm = JobManager()
        jm.start()
        
        # create, add and execute job for user 1
        for i in range(5):
            job = Job(increase, (1,))
            job.user_id = 1
            jm.addJob(job)
        
        # create, add and execute job for user 2
        for i in range(5):
            job = Job(increase, (1,))
            job.user_id = 2
            jm.addJob(job)
        
        # wait for completion
        sleep(delay*4)
        
        # clean all terminated jobs of user 1
        jm.cleanJobs(user_id=1)
        
        self.assertEqual(5, len(jm.getJobs('COMPLETED', user_id=2)))
        self.assertEqual(5, len(jm.getJobs('COMPLETED')))
        self.assertEqual([], jm.getJobs('FAILED'))
        jm.stop()

    def _test_get_job(self):
        """
        _test used to retrieve a specific Job object providing its id.
        """
        jm = JobManager()
        jm.start()
        
        job = Job(increase, (1,))
        job_id = jm.addJob(job)

        self.assertIsNotNone(jm.getJob(job_id))
        jm.stop()

    def _test_get_job2(self):
        """
        _test used to retrieve a specific job providing its id.
        """
        jm = JobManager()
        jm.start()
        
        # add some job
        job_id = None
        for i in range(4):
            job = Job(increase, (i,))
            job.user_id = i
            job_id = jm.addJob(job)
        
        # retrieve the last job object
        self.assertIsNotNone(jm.getJob(job_id))
        jm.stop()

    def _test_get_jobs_by_user(self):
        """
        _test used to retrieve all Job objects associated to a specific user
        providing his id.
        """
        jm = JobManager()
        jm.start()
        
        # add some job
        for i in range(4):
            job = Job(increase, (i,))
            job.user_id = i
            jm.addJob(job)
        
        # wait for completion
        sleep(2*delay)
        
        # retrieve the last job object
        self.assertEqual(1, len(jm.getJobs('COMPLETED', user_id=1)))
        jm.stop()

    def _test_get_jobs_by_user2(self):
        """
        _test used to retrieve all Job objects associated to a specific user
        providing his id. The Job Manager is not started in this case.
        """
        jm = JobManager()
        
        # add some job
        for i in range(4):
            job = Job(increase, (i,))
            job.user_id = i
            jm.addJob(job)
        
        # wait for completion
        sleep(2*delay)
        
        # retrieve the last job object
        self.assertEqual(1, len(jm.getJobs('QUEUED', user_id=1)))

    def _test_get_all_jobs(self):
        """
        _test used to check if a Job Manager is able 
        to retrieve all available jobs.
        In this _test no Job objects are added to the JobManager.
        """
        jm = JobManager()
        jm.start()
        
        jobs = jm.getAllJobs()
        
        self.assertEqual([], jobs['QUEUED'])
        self.assertEqual([], jobs['RUNNING'])
        self.assertEqual([], jobs['COMPLETED'])
        self.assertEqual([], jobs['FAILED'])
       
        jm.stop()

    def _test_get_all_jobs_by_user(self):
        """
        _test used to check if a Job Manager is able 
        to retrieve all available jobs of a specific user by his id
        All jobs are associated to a unique user
        """
        jm = JobManager()
        jm.start()
        
        for i in range(4):
            job = Job(increase, (i,))
            job.user_id = 1
            jm.addJob(job)
        
        jobs = jm.getAllJobs(user_id=3)
        
        self.assertEqual([], jobs['QUEUED'])
        self.assertEqual([], jobs['RUNNING'])
        self.assertEqual([], jobs['COMPLETED'])
        self.assertEqual([], jobs['FAILED'])
       
        jm.stop()
   
    def _test_skeleton_progress(self):
        """
        _test the distribution of the percentage of completed stages over a skeleton.
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


class Test_REST_API(TestCase):
    """
    This class defines the _tests necessary to check if the provided
    REST API allows to access correctely to Job Manager functionalities.
    """
    
    def _create_job(self, user_id=0, is_admin=True, job_name='job_manager.job.job.PlainJob',
                    func_name='commons.tests.identity', params={}):
        """
        Function used to create a job with standard parameters.
        """
        return requests.post('http://localhost:9000/api/jobs/', 
                              data={'user_id': user_id,
                                    'is_admin': is_admin,
                                    'func_name': func_name,
                                    'job_name': job_name,
                                    'params': json.dumps(params)})

    def _clean_jobs(self, user_id=0, is_admin=True):
        """
        Function used to delete all terminated jobs of a given user.
        All jobs are removed from the queue if it is an admin request.
        """
        sleep(0.5)
        return requests.delete('http://localhost:9000/api/jobs/', 
                              data={'user_id': user_id, 'is_admin': is_admin})
    
    def _get_jobs(self, user_id=0, is_admin=True, status='ALL'):
        """
        Function used to retrieve all Job objects of a given if his
        id is provided. It is possible to obtain all Job objects if
        an admin user request them.
        """
        sleep(1)
        return requests.get('http://localhost:9000/api/jobs/', 
                            data={'user_id': user_id, 'is_admin': is_admin, 'status':status})
        
    def test_create_job(self):
        """
        Check if it is possible to start a Job on the
        Job Manager invoking the existing REST API.
        """
        r = self._create_job(1, True, params={'func': (1,)})
        self.assertEqual(r.status_code, requests.codes.created)
        self._clean_jobs()
    
    def test_create_job2(self):
        """
        Check if it is possible to start a Job on the
        Job Manager invoking the existing REST API.
        """
        r = self._create_job(2, False, params={'func': (3,)})
        self.assertEqual(r.status_code, requests.codes.created)
        self._clean_jobs()
    
    def test_get_jobs(self):
        """
        Function used to _test if it is possible to
        retrieve all Job objects for user 1 through the REST API.
        No Job objects have been created for this user.
        """
        r = self._get_jobs(1, True)
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(0, len(r.json()))
    
    def test_get_jobs2(self):
        """
        Function used to _test if it is possible to retrieve all 
        Job objects of a given user through the REST API.
        A Job object has been created for the user.
        """
        self._create_job(1, False, params={'func' :(1,)})
        r = self._get_jobs(1, False)
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(1, len(r.json()))
        self._clean_jobs()
        
    def test_get_jobs3(self):
        """
        Function used to _test if it is possible to retrieve all 
        Job objects for admin user through the REST API.
        It creates a Job object for another non admin user.
        """
        self._create_job(2, False, params={'func': (1,)})
        r = self._get_jobs(1, True)
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(1, len(r.json()))
        self._clean_jobs()
       
    def test_get_job(self):
        """
        Test used to check if it is possible
        to retrieve a Job executed by the user.
        """
        job_id = self._create_job(2, False, params={'func': (1,)}).json()['id']
        r = requests.get('http://localhost:9000/api/jobs/' + str(job_id),
                          {'user_id': 2, 'is_admin': False})
        self.assertEqual(r.status_code, requests.codes.ok)
        self._clean_jobs()
    
    def test_get_job2(self):
        """
        Test used to check if a generic user is able
        to retrieve a Job executed by another user.
        """
        job_id = self._create_job(1, False, params={'func': (1,)}).json()['id']
        r = requests.get('http://localhost:9000/api/jobs/' + str(job_id),
                          {'user_id': 2, 'is_admin': False})
        self.assertNotEqual(r.status_code, requests.codes.ok)
        self._clean_jobs()
    
    def test_get_job3(self):
        """
        Test used to check if the admin is able to retrieve
        a Job executed by another user.
        """
        job_id = self._create_job(1, False, params={'func': (1,)}).json()['id']
        r = requests.get('http://localhost:9000/api/jobs/' + str(job_id),
                          {'user_id': 2, 'is_admin': True})
        self.assertEqual(r.status_code, requests.codes.ok)
        self._clean_jobs()
    
    def ___test_get_job_result(self):
        """
        Test used to check if it is possible
        to retrieve the result of an executed Job.
        """
        job_id = self._create_job(2, False, params={'func': (1,)}).json()['id']
        r = requests.put('http://localhost:9000/api/jobs/' + str(job_id),
                         data={'user_id': 2, 'is_admin': False})
        self.assertEqual(r.status_code, requests.codes.ok)
        self._clean_jobs()
    
    def test_abort_job(self):
        """
        Function used to check if it is possible to abort
        a running Job thtorugh the REST API.
        """
        job_id = self._create_job(2, False, params={'func': (1,)}).json()['id']
        r = requests.delete('http://localhost:9000/api/jobs/' + str(job_id))#, **{'user_id': 2, 'is_admin': False})
        self.assertEqual(r.status_code, requests.codes.no_content)
        self._clean_jobs()
    
    def test_clean_jobs(self):
        """
        Test used ot check if it is possible to delete all
        terminated jobs for a given user through the REST API.
        Two jobs are created for this _test.
        """
        # start two jobs and wait for completion
        self._create_job(1, False, params={'func': (1,)})
        self._create_job(1, False, params={'func': (2,)})
        
        # clean jobs and check if they exists
        r = self._clean_jobs(1, False)
        self.assertEqual(r.status_code, requests.codes.no_content)
        jobs = self._get_jobs(1, False).json()
        self.assertEqual(0, len(jobs))
        
    def test_clean_jobs2(self):
        """
        Test used ot check if an admin user is able to clean all
        terminated jobs of other users through the REST API.
        Four jobs are created for this _test.
        """
        # start two jobs and wait for completion
        for i in range(4):
            self._create_job(1, False, params={'func': (i,)})
        
        # clean jobs and check if they exists
        r = self._clean_jobs(2, True)
        self.assertEqual(r.status_code, requests.codes.no_content)
        jobs = self._get_jobs(2, True).json()
        self.assertEqual(0, len(jobs))
        self._clean_jobs()
    
    def test_clean_jobs3(self):
        """
        Test used ot check if a standard user is able to clean
        terminated jobs of other users through the REST API.
        Four jobs are created for this _test.
        """
        # start two jobs and wait for completion
        for i in range(4):
            self._create_job(1, False, params={'func': (i,)})
        
        # clean jobs and check if they exists
        r = self._clean_jobs(user_id=2, is_admin=False)
        self.assertEqual(r.status_code, requests.codes.no_content)
        jobs = self._get_jobs(1, False).json()
        self.assertEqual(4, len(jobs))
