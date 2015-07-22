"""
This module defines all views provided by
the Job Monitor tool. In this case all views simply redirect a 
request to the job processor and return the result.
This is done both for job and cluster node views.
The job monitor is just a proxy tool for the remote job processor system.
"""


import requests
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView


def index(request):
    return render(request, "job_monitor_index.html")


class JobsList(APIView):
    """
    Class used to retrieve all jobs.
    """
    queryset = User.objects.none()

    def get(self, request, format=None):
        """
        Method used to implement the GET function for listing all jobs.
        It retrieves all available jobs handled by the job processor.
	"""
        status = request.GET.get('status', 'ALL')
        url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
        r = requests.get(url, params={"status":status, 'user_id': request.user.pk})
        return HttpResponse(r)


class JobsDelete(APIView):
    """
    Class used to abort the execution of a job. 
    """
    queryset = User.objects.none()

    def get(self, request, format=None):
        """
        Method used to implement the GET function for stopping job execution.
        It tries to stop as soon as possible the executiuon of a giveng job.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.delete(url, params={'user_id': request.user.pk})
	return HttpResponse(r)


class JobGetDetails(APIView):
    """
    Class used to retrieve all job details.
    """
    queryset = User.objects.none()

    def get(self, request, pk, format=None):
        """
        This method implements the GET function in order to retrieve all
        details about a specific job handled by the job processor.
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + str(pk) + "/"
        r = requests.get(url, params={'user_id': request.user.pk})
        return HttpResponse(r)


class JobStopDetails(APIView):
    queryset = User.objects.none()

    def get(self, request, pk, format=None):
        """
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + str(pk) + '/'
	r = requests.delete(url, params={'user_id': request.user.pk})
	return HttpResponse(r)


class JobGetResult(APIView):
    queryset = User.objects.none()

    def get(self, request, pk, format=None):
        """
        """
        url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + str(pk) + '/'
	r = requests.put(url, params={'user_id': request.user.pk})
	return HttpResponse(r)


"""
def list_jobs(request):
	status = request.GET["status"]
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.get(url, params={"status":status, 'user_id': request.user.pk})
	return HttpResponse(r)

def get_job(request, job_id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + job_id + "/"
	r = requests.get(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def clean_jobs(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.delete(url, params={'user_id': request.user.pk})
	return HttpResponse(r)


def stop_job(request, job_id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + job_id + '/'
	r = requests.delete(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def get_job_result(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.put(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

"""

def list_nodes(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.get(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def start_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.post(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def stop_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.delete(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def restart_cluster(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/cluster/"
	r = requests.put(url, params={'user_id': request.user.pk})
	return HttpResponse(r)

def get_node(request, id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/node/" + id + '/'
	r = requests.get(url, params={'user_id': request.user.pk})
	return HttpResponse(r)
