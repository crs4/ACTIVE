from django.conf import settings
from django.http import HttpResponse, Http404

from rest_framework.views import APIView

from job_manager.job.job_manager import JobManager

from importlib import import_module
import json
import logging

# variable used for logging purposes
logger = logging.getLogger('job_processor')


jmd = JobManager()
jmd.start()

# variable used to handle one Job Manager for each user.
# A Job Manager is associated to a user through his authentication token.
#jmd = {'0' : JobManager()}
#jmd['0'].start()

class JobList(APIView):
    """
    Class used to retrieve the list of all stored Job objects, create a new
    Job object and start its execution. delete all result of already executed jobs.
    Job objects could be selected by status or retrieved entirely.
    Objects data are retrieved and provided in a serialized format.
    """

    def get(self, request):
        """
        This view is used to return a list of jobs, divided by their
        computational status.
        It is possible to filter all jobs by status (optional).

        @param request: HttpRequest used to retrieve all Job objects.
        @type request: HttpRequest
        @return: HttpResponse containing all serialized Job data.
        @rtype: HttpResponse
        """
        status = request.GET.get('status', 'ALL')

        logger.debug('Requested Job objects with status ' + status)

        if status == 'ALL':
            jobs = jmd.getAllJobs()
            jobs = jobs['QUEUED'] + jobs['RUNNING'] + jobs['COMPLETED'] + jobs['FAILED']
        elif status == 'ABORTED':
            jobs = jmd.getJobs('FAILED')
            jobs = [job for job in jobs if job['status'] == 'ABORTED']
        else:
            jobs = jmd.getJobs(status)

        ret = []
        for job in jobs:
            ret.append({'id' : job.id,
                        'name' : job.name,
                        'status' : job.status,
                        'progression' : job.progression()})
        return HttpResponse(json.dumps(ret, default=str))

    def post(self, request, format=None):
        """
        This view is used to start a Job object from a set of parameters and its
        full specified name.

        @param request: HttpRequest containing all data necessary to create a new Job object.
        @type request: HttpRequest
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing all serialized Job data.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new Job object')

        func_name = request.POST.get('func_name', '')
        job_name = request.POST.get('job_name', '')
        func_in1 = json.loads(request.POST.get('event_in_params', {}))
        func_in2 = json.loads(request.POST.get('event_out_params', {}))
        name = request.POST.get('name', 'JOB')

        # associate the user authentication token
        if 'token' not in func_in1:
            func_in1['token'] = 0
        token = func_in1['token']
        print func_in1

        try:
            # get the plugin script function
            complete_path = settings.PLUGIN_SCRIPT_MODULE + '.' + func_name
            splits = complete_path.split('.')
            func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # get the job wrapper function
            splits = job_name.split('.')
            job_class = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # construct a job instance
            job = job_class(func, (func_in1, func_in2,))
            job.name = name
            job.func_name = func_name

            #job.user_token = token


            # check if user Job Manager is instantiated
            #if token not in jmd:
            #    jmd[token] = JobManager()
            #    jmd[token].start()

            # add the job to the execution queue
            job_id = jmd.addJob(job)
            return HttpResponse(json.dumps({'id': job_id}))

        except Exception as ex:
            print ex
            logger.error('Error on starting job execution ' + job_name)
            return HttpResponse(json.dumps({'error': str(ex)}))

    def delete(self, request):
        """
        Clean all job that are waiting for execution or already executed.
        WARNING: all previously computed results are lost!

        @param request: HttpRequest used to delete the data of available Job.
        @type request: HttpRequest
        @return: HttpResponse containing the result of Job data cleaning.
        @rtype: HttpResponse
        """
        jmd.cleanJobs(request)
        return HttpResponse(json.dumps({'info' : True}))


class JobDetail(APIView):
    """
    Class used to retrieve data of a specific Job object,
    update Job data and delete data Job.
    """

    def get(self, request, pk, format=None):
        """
        This view is used to return Job object information by its id.
        All data is returned in a serialized form.

        @param request: HttpRequest used to retrieve data of a specific Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing all serialized Job data.
        @rtype: HttpResponse
        """
        job = jmd.getJob(pk)
        response = {}
        if job:
            response = {'id' : job.id,
                        'error_info' : job.error_info,
                        'start_timestamp' : job.start_time,
                        'end_timestamp' : job.end_time,
                        'status' : job.status,
                        'name' : job.name,
                        'func_name' : job.func_name,
                        'result' : str(job.result),
                        'progression': job.progression() }
        return HttpResponse(json.dumps(response, default=str))

    def post(self, request, pk, format=None):
        """
        This method is used to compute if the result of a job has been
        computed or if it is still waiting for computation or the
        job is currently running.

        @param request: HttpRequest containing all data of a new Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing the id of the new object, error otherwise.
        @rtype: HttpResponse
        """
        job = jmd.getJob(pk)
        if job:
            res = job.get_result()
            return HttpResponse(json.dumps(res, default=str))

        logger.error('Error on retrieving Job object ' + str(pk) + ' result')
        return HttpResponse(json.dumps({'error': 'No job found'}))

    def put(self, request, pk, format=None):
        """
        This method is used to return the result of a job, if any.
        If the jobs still running or waiting for execution the returned
        value will be None.

        @param request: HttpRequest containing all fresh data for a specific Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object to update.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing all updated Job data.
        @rtype: HttpResponse
        """
        job = jmd.getJob(pk)
        res = job.get_result()
        return HttpResponse(json.dumps(res, default=str))

    def delete(self, request, pk, format=None):
        """
        This view is used to abort a previous started job.
        Job and all associated task are stopped.

        @param request: HttpRequest used to delete a specific Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing the result of the Job deletion.
        @rtype: HttpResponse
        """
        res = jmd.abortJob(pk)
        return HttpResponse(json.dumps({'info': res}, default=str))