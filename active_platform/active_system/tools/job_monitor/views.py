"""
This module defines all views provided by
the Job Monitor tool. In this case all views simply redirect a 
request to the job processor and return the result.
This is done both for job and cluster node views.
The job monitor is just a proxy tool for the remote job processor system.
"""


import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	return render(request, "jobmonitor/index.html")

def list_jobs(request):
	status = request.GET["status"]
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.get(url, params={"status":status})
	return HttpResponse(r)

def get_job(request, job_id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + job_id + "/"
	r = requests.get(url)
	return HttpResponse(r)

def clean_jobs(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
	r = requests.delete(url)
	return HttpResponse(r)

def stop_job(request, job_id):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/" + job_id + '/'
	r = requests.delete(url)
	return HttpResponse(r)

def get_job_result(request):
	url = settings.JOB_PROCESSOR_ENDPOINT + "api/jobs/"
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
