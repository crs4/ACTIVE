from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import Group

from core.views import EventView

from rest_framework.response import Response
from rest_framework import status as http_status

import requests


def _detect_user_params(request):
    """
    Function used to extract the user parameter from a incoming
    HttpRequest. It returns the user id and the if the user is root.

    :param request: HttpRequest that will be analyzed
    :return: User id and Admin flag
    """
    if not request.user or not request.user.is_authenticated():
        return None, False

    user_id = request.user.id
    user_role = request.user.is_superuser
    user_role = user_role or Group.objects.filter(name='Admin') in request.user.groups.all()
    print user_id, user_role #######
    return user_id, user_role


def index(request):
    """
    View function used to return the Job Monitor homepage.

    :param request: HttpRequest used to retrieve the index.
    :return: HttpResponse redirecting to the index page.
    """
    return render(request, "jobmonitor/index.html")


class JobList(EventView):
    """
    Class used to define the REST API for Job objects.
    This class implements all methods necessary to interact with the
    Job Processor REST API, listing all Jobs, starting new ones and deleting
    all Jobs already completed or aborted.
    """
    model = Group # permissions associated to this view

    def get(self, request, format=None):
        """
        Method is used to retrieve all Jobs managed by the Job Processor,
        for the current user. If the user is a Admin user it retrieves every job
        existing in the Job Processor.
        """
        user_id, is_root = _detect_user_params(request)
        status = request.query_params.get('status', 'ALL')


        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
        r = requests.get(url, data={'status' : status, 'user_id': user_id, 'is_root': is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        """
        Method is used to start a new Job on the Job Processor and
        associate it to the current user.
        """
        user_id, is_root = _detect_user_params(request)

        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
        r = requests.post(url,	{'name'       : request.query_params.get('name', 'Job'),
                                 'func_name'  : request.query_params.get('func_name', ''),
                                 'job_name'   : request.query_params.get('job_name', ''),
                                 'auth_params': request.query_params.get('auth_param'),
                                 'func_params': request.query_params.get('func_params'),
                                 'user_id'    : user_id,
                                 'is_root'    : is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        """
        Method is used to delete all terminated Jobs in the Job Processor,
        for the current user. If the user is a Admin user it delete every
        terminated job existing in the Job Processor.
        """
        user_id, is_root = _detect_user_params(request)

        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
        r = requests.delete(url, data={'user_id': user_id, 'is_root': is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)


class JobDetail(EventView):
    """
    Class used to define the REST API for Job objects.
    This class implements all methods necessary to interact with the
    Job Processor REST API, retrieving a job, deleting it or stopping
     its execution on the Job Processor.
    """
    model = Group # permissions associated to this view

    def get(self, request, pk, format=None):
        """
        Method used to retrieve the serialized data of a specific job,
        providing its id and current user data.
        """
        user_id, is_root = _detect_user_params(request)

        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/' + str(pk)
        r = requests.get(url, data={'user_id': user_id, 'is_root': is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        """
        Method used to retrieve the serialized result generated from the
        computation of a specific job, providing its id and current user data.
        """
        user_id, is_root = _detect_user_params(request)

        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/' + str(pk)
        r = requests.put(url, data={'user_id': user_id, 'is_root': is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        """
        Method used to delete the serialized result generated from the
        computation of a specific job, providing its id and current user data.
        """
        user_id, is_root = _detect_user_params(request)

        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/' + str(pk)
        r = requests.put(url, data={'user_id': user_id, 'is_root': is_root})

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)


class ClusterList(EventView):
    """
    Class used to retrieve data about the cluster of nodes, starting all nodes,
    stopping all them
    """
    model = Group # permissions associated to this view

    def get(self, request, format=None):
        """
        Method used to retrieve all cluster nodes.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/cluster/'
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        """
        Method used to start all cluster nodes.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/cluster/'
        r = requests.post(url)

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None):
        """
        Method used to restart all cluster nodes.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/cluster/'
        r = requests.put(url)

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        """
        Method used to stop all cluster nodes.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/cluster/'
        r = requests.delete(url)

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)


class NodeDetail(EventView):
    """
    Class used to retrieve cluster node details, providing the node id.
    """
    model = Group # permissions associated to this view

    def get(self, request, pk, format=None):
        """
        Method used to retrieve the details about a specific
        cluster node, providing its id.
        Node data are returned in a serialized format.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + 'api/node/' + str(pk)
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            return Response(r.json(), status=http_status.HTTP_200_OK)
        return Response(status=http_status.HTTP_404_NOT_FOUND)

"""
def list_jobs(request):
    status = request.GET["status"]
    user_id = request.user.id
    user_role = Group.objects.filter(name = 'Admin') in request.user.groups.all() or request.user.is_superuser


    url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
    r = requests.get(url, params={'status' : status,
                                  'user_id': user_id,
                                  'is_root': user_role})
    return HttpResponse(r)

def get_job(request, job_id):
    url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/' + job_id + "/"
    r = requests.get(url)
    return HttpResponse(r)

def clean_jobs(request):

    url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
    r = requests.delete(url)
    return HttpResponse(r)

def stop_job(request, job_id):
	url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/' + job_id + '/'
	r = requests.delete(url)
	return HttpResponse(r)

def get_job_result(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + 'api/jobs/'
	r = requests.put(url)
	return HttpResponse(r)


def list_nodes(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.get(url)
	return HttpResponse(r)

def start_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.post(url)
	return HttpResponse(r)

def stop_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.delete(url)
	return HttpResponse(r)

def restart_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.put(url)
	return HttpResponse(r)

def get_node(request, id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/node/" + id + '/'
	r = requests.get(url)
	return HttpResponse(r)
"""