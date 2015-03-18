from django.shortcuts import render
from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from job_manager.job.job_manager import JobManager
from job_manager.job.job import SkeletonJob, PlainJob

from importlib import import_module
import json


jmd = JobManager()

class JobList(APIView):

	def get(self, request):
		"""
	        This view is used to return a list of jobs, divided by their
	        computational status.
	        It is possible to filter all jobs by status (optional).
	        """
		status = request.GET.get('status', 'ALL')

		if(status == 'ALL'):
			jobs = jmd.getAllJobs()
			jobs = jobs['QUEUED'] + jobs['RUNNING'] + jobs['COMPLETED'] + jobs['FAILED']
		elif(status == 'ABORTED'):
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
		This view is used to start a job from a set of parameters and its
		full specified name.
		"""
		
                func_name = request.POST.get('func_name', '')
		job_name = request.POST.get('job_name', '')
		func_in1 = json.loads(request.POST.get('event_in_params', {}))
		func_in2 = json.loads(request.POST.get('event_out_params', {}))
		name = request.POST.get('name', 'JOB')

                print "Parametri ", func_name, job_name, name
		print func_in1, func_in2

		try:
			splits = ('plugins_script.' + func_name).split('.')
                        func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
			func(func_in1, func_in2)
			return HttpResponse(json.dumps({'id': 1}))
			"""
			# load the function that will be executed
			splits = func_name.split('.')
			func = getattr(import_module('.'.join(splits[:-1])), splits[-1])
			job = func(*func_input)
			# construct and start the execution of the wrapper job
			job.name = job_name
			job.func_name = func_name
			job_id = jmd.addJob(job)
			return HttpResponse(json.dumps({'id': job_id}))
			"""
		except Exception as ex:
			print ex
			return HttpResponse(json.dumps({'error': str(ex)}))


	def delete(self, request):
		"""
		Clean all job that are waiting for execution or already executed.
		WARNING: all previously computed results are lost!
		"""
		jmd.cleanJobs()
		return HttpResponse(json.dumps({'info' : True}))


class JobDetail(APIView):
        def get(self, request, pk, format=None):
		"""
		This view is used to return job information by its ID.
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
			    'result' : str(job.result), #[:500] + '...',
			    'progression': job.progression() }
		return HttpResponse(json.dumps(response, default=str))

	def post(self, request, pk):
		"""
		This method is used to compute if the result of a job has been
		computed or if it is still waiting for computation or the
		job is currently runnning.
		"""
		job = jmd.getJob(pk)
		if job:
			res = job.get_result()
			return HttpResponse(json.dumps(res, default=str))

		return HttpResponse(json.dumps({'error' : 'No job found'}))


        def put(self, request, pk):
		"""
                This method is used to return the result of a job, if any.
		If the jobs still running or waiting for execution the returned
		value will be None.
                """
                job = jmd.getJob(pk)
                res = job.get_result()
                return HttpResponse(json.dumps(res, default=str))

        def delete(self, request, pk):
		"""
		This view is used to abort a previous started job.
		Job and all associated task are stopped.
		"""
		res = jmd.abortJob(pk)
		return HttpResponse(json.dumps({'info': res}, default=str))

