from django.conf import settings
from django.http import HttpResponse, Http404

from rest_framework.views import APIView

from job_manager.job.job_manager import JobManager

from importlib import import_module
import json
import logging


# variable used for logging purposes
logger = logging.getLogger('job_processor')

# global variable used to handle all users Job
jm = JobManager()
jm.start()


def _extract_user_id(request, GET_method=False):
    """
    Function used to extract the user parameter and detect if
    the user is a root. The HttpRequest parameter must contain
    all data necessary for user authentication.

    @param request: HttpRequest containing user parameters.
    @param GET_method: Flag for HTTP GET method request
    @return: The user id, None if the user is root.
    """

    auth_params = {}
    if GET_method:
        auth_params = request.query_params.get('auth_params', {})
    else:
        auth_params = request.data.get('auth_params', {})
    user_id = auth_params.get('user_id', '0')
    is_root = auth_params.get('is_root', False)

    if is_root:
        return None
    return user_id


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
        It is possible to filter all jobs by status and user id (optional)

        @param request: HttpRequest used to retrieve all Job objects.
        @type request: HttpRequest
        @return: HttpResponse containing all serialized Job data.
        @rtype: HttpResponse
        """
        status = request.query_params.get('status', 'ALL')
        user_id =_extract_user_id(request, True)

        logger.debug('Requested Job objects with status ' + status + ' by user ' + str(user_id))

        if status == 'ALL':
            jobs = jm.getAllJobs(user_id)
            jobs = jobs['QUEUED'] + jobs['RUNNING'] + jobs['COMPLETED'] + jobs['FAILED']
        elif status == 'ABORTED':
            jobs = jm.getJobs('FAILED', user_id)
            jobs = [job for job in jobs if job['status'] == 'ABORTED']
        else:
            jobs = jm.getJobs(status, user_id)

        ret = []
        for job in jobs:
            ret.append({'id'         : job.id,
                        'name'       : job.name,
                        'status'     : job.status,
                        'progression': job.progression(),
                        'user_id'    : job.user_id})
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

        func_name = request.data.get('func_name', '')
        job_name = request.data.get('job_name', '')
        auth_params = json.loads(request.data.get('auth_params', {}))
        func_params = json.loads(request.data.get('func_params', {}))
        name = request.data.get('name', 'JOB')

        try:
            # get the plugin script function
            complete_path = settings.PLUGIN_SCRIPT_MODULE + '.' + func_name
            splits = complete_path.split('.')
            func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # get the job wrapper function
            splits = job_name.split('.')
            job_class = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # construct a job instance
            job = job_class(func, (auth_params, func_params,))
            job.name = name
            job.func_name = func_name
            job.user_id   = auth_params['user_id']

            # add the job to the execution queue
            job_id = jm.addJob(job)
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
        user_id = _extract_user_id(request)
        jm.cleanJobs(user_id)
        return HttpResponse(json.dumps({'info': True}))


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
        user_id = _extract_user_id(request, True)
        job = jm.getJob(pk, user_id)

        response = {}
        if job:
            response = {'id'              : job.id,
                        'error_info'      : job.error_info,
                        'start_timestamp' : job.start_time,
                        'end_timestamp'   : job.end_time,
                        'status'          : job.status,
                        'name'            : job.name,
                        'func_name'       : job.func_name,
                        'result'          : str(job.result),
                        'progression'     : job.progression(),
                        'user_id'         : job.user_id}
        return HttpResponse(json.dumps(response, default=str))

    def post(self, request, pk, format=None):
        """
        This method is used to detect if the result of a job has been
        computed or if it is still waiting for its completion.

        @param request: HttpRequest containing all data of a new Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing the id of the new object, error otherwise.
        @rtype: HttpResponse
        """
        user_id = _extract_user_id(request)
        job = jm.getJob(pk, user_id)

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
        user_id = _extract_user_id(request)
        job = jm.getJob(pk, user_id)
        return HttpResponse(json.dumps(job.get_result(), default=str))

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
        user_id = _extract_user_id(request)
        res = jm.abortJob(pk, user_id)
        return HttpResponse(json.dumps({'info': res}, default=str))
