import json
from importlib import import_module
from django.shortcuts import render
from django.http import HttpResponse
from job_manager import JobManager
from job import SkeletonJob, PlainJob
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from skeleton.skeletons import Farm, Pipe, Map, Seq, If
from skeleton.visitors import Executor

from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager

from pluginmanager.plugin_mount_point import ActionProvider

"""
These views are used to provide a simple REST API
that could be used by an HTTP client to get informations
about the state of each job.
In order to invoke any method user login is required.
So it will be possible to associate a job manager to each user
through his user_id parameter.
"""

# dictionary of job managers, each user has his own one
user_job_managers = {}

# function necessary to get the correct job manager
def get_job_manager(username):
	# if no job manager is available, it creates a new one
        if(not username in user_job_managers):
                jm = JobManager()
                jm.start()
                user_job_managers[username] = jm
        # return the current user job manager 
	return user_job_managers[username]


@csrf_exempt
def start_job(request):
	"""
	This view is used to start a job from a set of parameters and its
	full specified name.
	"""
	# get the current user job manager if available, otherwise create a new one
	
	try:
		data = json.loads(request.body)
		print data['func_name']
		print data['params']
		print data['name']

		user_id = 'root' # request.user.get_username()
		jmd = get_job_manager(user_id)	


		func_name = data['func_name']
		func_input = data['params']
		splits = func_name.split('.')
		func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
		job = func(*func_input)
		
		#plugin = ActionProvider.get_plugin(func_name)
		#print "nome plugin", plugin
		#job = PlainJob(plugin().perform, tuple(func_input))

		job.name = data['name']
		job.func_name = func_name
		job_id = jmd.addJob(job)
		return HttpResponse(json.dumps({'id': job_id}))
	except KeyError as ex:
		print ex
		return HttpResponse(json.dumps({'status': 401, 'msg': 'Unauthorized'}))

#@csrf_exempt
def stop_job(request, job_id):
	"""
	This view is used to abort a previous started job.
	Job and all associated task are stopped.
	"""
	
	# get the current user job manager if available, otherwise create a new one
	user_id = request.user.get_username()
        jmd = get_job_manager(user_id)

	# stop job execution
	res = jmd.abortJob(job_id)	
	print job_id, " ", res
	return HttpResponse(json.dumps({'info': res}, default=str))

@csrf_exempt
def clean_jobs(request):
	"""
	Clean all job that are waiting for execution or already executed.
	WARNING: computed results are lost!
	"""
        # get the current user job manager if available, otherwise create a new one
	user_id = request.user.get_username()
        jmd = get_job_manager(user_id)

	jmd.cleanJobs()
	return HttpResponse(json.dumps({'info' : True}))

def get_job(request, job_id):
	"""
	This view is used to return job information by its ID.
	"""

        # get the current user job manager if available, otherwise create a new one
	user_id = request.user.get_username()
        jmd = get_job_manager(user_id)

	job = jmd.getJob(job_id)
	response = {	"id" : job.id,
			"error_info" : job.error_info,
			"start_timestamp" : job.start_time,
			"end_timestamp" : job.end_time,
			"status" : job.status,
			"name" : job.name,
			"func_name": job.func_name,
			"result": str(job.result)[:500] + '...',
			"progression": job.progression() } if job else {}
	return HttpResponse(json.dumps(response, default=str))

@csrf_exempt
def get_job_result(request):
	"""
	This view is used to compute if the result of a job has been
	computed or if it is still waiting for computation or the
	job is currently runnning.
	"""

        # get the current user job manager if available, otherwise create a new one
	user_id = request.user.get_username()
        jmd = get_job_manager(user_id)

	job_id = request.POST.get("job_id", '')
	job = jmd.getJob(job_id)
	res = job.get_result()
	return HttpResponse(json.dumps(res, default=str))

def list_jobs(request):
	"""
	This view is used to return a list of jobs, divided by their
	computational status.
	It is possible to filter all jobs by status (optional).
	"""
        # get the current user job manager if available, otherwise create a new one	
	user_id = request.user.get_username()
	jmd = get_job_manager(user_id)

	status = request.GET['status']
	
	if(status == 'ALL'):
		jobs = jmd.getAllJobs()
		jobs = jobs["QUEUED"] + jobs["RUNNING"] + jobs["COMPLETED"] + jobs["FAILED"] 
	elif(status == 'ABORTED'):
		jobs = jmd.getJobs('FAILED')
		jobs = [job for job in jobs if job['status'] == 'ABORTED']
	else: 
		jobs = jmd.getJobs(status)
	
	ret = []
	for job in jobs:
		ret.append({"id":job.id, "name":job.name, "status":job.status, "progression": job.progression()})
	return HttpResponse(json.dumps(ret, default=str))
