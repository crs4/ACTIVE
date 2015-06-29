"""
This module contains all classes and functions necessary to
define a REST API for JobManager functionalities.
"""

from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from job_manager.job.job_manager import JobManager
from importlib import import_module
import json
import logging


# variable used for logging purposes
logger = logging.getLogger('job_processor')

# global variable used to handle all users Job
jm = JobManager()
jm.start()


class JobList(APIView):
    """
    Class used to retrieve the list of all stored Job objects, create a new
    Job object and start its execution. delete results of already executed jobs.
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
        state    = request.data.get('status', 'ALL')
        user_id  = int(request.data.get('user_id', '0'))
        is_admin = request.data.get('is_admin', 'False') == 'True'

        logger.debug('Requested Job objects with status ' + str(state) + ' by user ' + str(user_id))
        
        if state == 'ALL':
            jobs = jm.getAllJobs(None if is_admin else user_id)
            jobs = jobs['QUEUED'] + jobs['RUNNING'] + jobs['COMPLETED'] + jobs['FAILED']
        elif state == 'ABORTED':
            jobs = jm.getJobs('FAILED', None if is_admin else user_id)
            jobs = [job for job in jobs if job['status'] == 'ABORTED']
        else:
            jobs = jm.getJobs(state, None if is_admin else user_id)
        
        # generate the representation for each retrieved job
        ret = []
        for job in jobs:
            ret.append({'id'         : job.id,
                        'name'       : job.name,
                        'status'     : job.status,
                        'progression': job.progression(),
                        'user_id'    : job.user_id})
        
        return Response(ret, status=status.HTTP_200_OK)

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
        try:
            user_id  = int(request.data.get('user_id', '0'))
            is_admin = request.data.get('is_admin', 'False') == 'True'
            func_name = request.data.get('func_name', '')
            job_name = request.data.get('job_name', '')
            params = json.loads(request.data.get('params', '{}'))
            name = request.data.get('name', 'JOB')

            # get the plugin script function
            complete_path = settings.PLUGIN_SCRIPT_MODULE + '.' + func_name
            splits = complete_path.split('.')
            func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # get the job wrapper function
            splits = job_name.split('.')
            job_class = getattr(import_module('.'.join(splits[:-1])), splits[-1])
            # construct a job instance
            job = job_class(func, params.get('func', ()), params.get('kwdict', {}))
            job.name = name
            job.func_name = func_name
            job.user_id   = int(user_id)

            # add the job to the execution queue
            job_id = jm.addJob(job)
            return Response({'id': job_id}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            print ex
            logger.error('Error on starting job execution ' + job_name)
            return Response({'error': str(ex)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """
        Clean all job that are waiting for execution or already executed.
        WARNING: all previously computed results are lost!

        @param request: HttpRequest used to delete the data of available Job.
        @type request: HttpRequest
        @return: HttpResponse containing the result of Job data cleaning.
        @rtype: HttpResponse
        """
        user_id  = int(request.data.get('user_id', '0'))
        is_admin = request.data.get('is_admin', 'False') == 'True'
        jm.cleanJobs(None if is_admin else user_id)
        return Response({'info': True}, status=status.HTTP_204_NO_CONTENT)


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
        user_id  = int(request.query_params.get('user_id', 0))
        is_admin = request.query_params.get('is_admin', 'False') == 'True'
        job = jm.getJob(pk)

        # check if the job has been retrieved
        if not job:
            logger.error('Error on retrieving Job object ' + str(pk))
            return Response('No job found for id ' + str(pk), status=status.HTTP_404_NOT_FOUND)
        
         # check the user ownership of the retrieved job
        if not is_admin and job.user_id != user_id:
            logger.error('User ' + str(user_id) + ' not owner of Job object ' + str(pk))
            return Response('User not authorized', status=status.HTTP_403_FORBIDDEN)

        # return the retrieved object
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
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
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
        print request.DATA

        user_id  = int(request.data.get('user_id', 0))
        is_admin = request.data.get('is_admin', 'False') == 'True'
        job = jm.getJob(pk)

        print user_id, is_admin
        
        # check if the job has been retrieved
        if not job:
            logger.error('Error on retrieving Job object ' + str(pk))
            return Response('No job found for id ' + str(pk), status=status.HTTP_404_NOT_FOUND)
        
         # check the user ownership of the retrieved job
        if not is_admin and job.user_id != user_id:
            logger.error('User ' + str(user_id) + ' not owner of Job object ' + str(pk))
            return Response('User not authorized', status=status.HTTP_403_FORBIDDEN)
        
        # retrieve and return the job result
        res = job.get_result()
        return Response(res, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        """
        This view is used to abort a previous started job.
        Job and all associated tasks are stopped.

        @param request: HttpRequest used to delete a specific Job object.
        @type request: HttpRequest
        @param pk: Primary key of the Job object.
        @type pk: int
        @param format: Format used to serialize object data.
        @type format: string
        @return: HttpResponse containing the result of the Job deletion.
        @rtype: HttpResponse
        """
        print request.data
        print request.query_params
        user_id  = int(request.query_params.get('user_id', 0))
        is_admin = request.query_params.get('is_admin', 'False') == 'True'
        job = jm.getJob(pk)

        # check if the job has been retrieved
        if not job:
            logger.error('Error on retrieving Job object ' + str(pk))
            return Response('No job found for id ' + str(pk), status=status.HTTP_404_NOT_FOUND)
        
        # check the user ownership of the retrieved job
        #if not is_admin and job.user_id != user_id:
        #    logger.error('User ' + str(user_id) + ' not owner of Job object ' + str(pk))
        #    return Response('User not authorized', status=status.HTTP_403_FORBIDDEN)
        
        # abort the retrieved job
        if jm.abortJob(pk):
            return Response('Job aborted correctely', status=status.HTTP_204_NO_CONTENT)
        return Response('Job NOT aborted!', status=status.HTTP_404_NOT_FOUND)
