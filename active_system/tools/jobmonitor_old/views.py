import json
import jobmanager
from jobmanager import views
from importlib import import_module
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

"""
These views are a copy of the one provided by the job manager.
They are simply used to redirect request to the job manager and return
information using a standard API.
# NB: attualmente si invocano direttamente le viste fornite dal job manager
# ma quando il monitor verra' spostato assieme al core sara' necessario
# invocare le apposite API REST tramite richiete HTTP POST.
"""


#@login_required
def index(request):
	print "home redirect"
	return render(request, 'jobmonitor/index.html')


@csrf_exempt
##@login_required
def start_job(request):
	print("JOBMONITOR: START JOB")
	return jobmanager.views.start_job(request)

#@csrf_exempt
#@login_required
def stop_job(request, job_id):
	return jobmanager.views.stop_job(request, job_id)

@csrf_exempt
#@login_required
def clean_jobs(request):
	return jobmanager.views.clean_jobs(request)

#@csrf_exempt
#@login_required
def get_job(request, job_id):
	return jobmanager.views.get_job(request, job_id)

@csrf_exempt
#@login_required
def get_job_result(request):
	return jobmanager.views.get_job_result(request)

#@csrf_exempt
##@login_required
def list_jobs(request):
	return jobmanager.views.list_jobs(request)
