from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from japp.models import Job
from japp.serializers import JobSerializer
		
		
@api_view(['GET', 'POST'])
def job_list(request, format = None):
	
	"""
	List all jobs or create a new job.
	"""
	
	if request.method == 'GET':
		
		jobs = Job.objects.all()
		serializer = JobSerializer(jobs, many = True)
		return Response(serializer.data)
		
	elif request.method == 'POST':
		
		serializer = JobSerializer(data = request.DATA)
		
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def job_details(request, job_id, format = None):
	
	"""
	Fetch, update or delete a job.
	"""
	
	job = get_object_or_404(Job, pk = job_id)
	
	if request.method == 'GET':
		
		serializer = JobSerializer(job)
		return Response(serializer.data)
		
	elif request.method == 'PUT':
		
		serializer = JobSerializer(job, data = request.DATA)
		
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		
	elif request.method == 'DELETE':
		
		job.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)
		

class ScriptList(APIView):
	
	"""
	List all scripts or create a new script.
	"""
	
	def get(self, request, format = None):
		
		jobs = Job.objects.all()
		
		serializer = JobSerializer(jobs, many = True)
		
		return Response(serializer.data)
		
	def post(self, request, format = None):
		
		serializer = JobSerializer(data = request.DATA)
		
		if serializer.is_valid():
			
			serializer.save()
			
			return Response(serializer.data, status = status.HTTP_201_CREATED)
			
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	
	
class ScriptDetails(APIView):
	
	"""
	Fetch, update or delete a script.
	"""
	
	def get_job(self, job_id):
		
		return get_object_or_404(Job, pk = job_id)
	
	def get(self, request, job_id, format = None):
		
		job = self.get_job(job_id)
		
		serializer = JobSerializer(job)
		
		return Response(serializer.data)
		
	def put(self, request, job_id, format = None):
		
		job = self.get_job(job_id)
		
		serializer = JobSerializer(job, data = request.DATA)
		
		if serializer.is_valid():
			
			serializer.save()
			
			return Response(serializer.data)
			
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		
	def delete(self, request, job_id, format = None):
		
		job = self.get_job(job_id)
		
		job.delete()
		
		return Response(status = status.HTTP_204_NO_CONTENT)
