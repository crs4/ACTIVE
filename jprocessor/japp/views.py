import cv2
import json

from abc import ABCMeta, abstractmethod

#from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from japp.models import Job
from japp.serializers import JobSerializer
from japp.tasks import *

from japp.tools.Constants import *
from japp.tools.FaceModelsLBP import FaceModelsLBP
from japp.tools.face_recognition import recognize_face
		

class Runner(object):
	
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def run(self, request, *args, **kwargs):
		pass
	"""
	@abstractmethod
	def pause(self, request, *args, **kwargs):
		pass
		
	@abstractmethod
	def kill(self, request, *args, **kwargs):
		pass
		
	@abstractmethod
	def details(self, request, *args, **kwargs):
		pass
	"""

class JobList(Runner, GenericAPIView):
	
	serializer_class = JobSerializer
	
	def get(self, request, *args, **kwargs):
		#return self.run(request, *args, **kwargs)
		pass
		
	def post(self, request, *args, **kwargs):
		
		return self.run(request, *args, **kwargs)

"""
class JobDetails(Runner, GenericAPIView):
	
	serializer_class = JobSerializer
	
	def get(self, request, job_id):
		
		return self.details(request, *args, **kwargs)
		
	def put(self, request, job_id):
		
		return self.pause(request, *args, **kwargs)
		
	def delete(self, request, job_id):
		
		return self.kill(request, *args, **kwargs)

"""
class FaceExtractorList(JobList):
	"""
	def get_face_models(self):
		
		data = cache.get('model')
		
		if data is not None:
			
			return data
			
		else:
			
			data = FaceModelsLBP()
			
			cache.set('model', data, 60)
			
			return data
	
	"""
	def get_frame_list(self, resource_path):

		frame_dir_path = '/home/federico/workspace-python/video/frames'
		
		capture = cv2.VideoCapture(resource_path)
        
		frame_list = []
        
		if capture is None or not capture.isOpened():
			
			error = 'Error in opening video file'
			
			return Response(data = error, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

		else:       

			counter = 0
            
			while True:
                
				ret, frame = capture.read()
                
				if(not(ret)):
                    
					break
                    
				frame_name = str(counter) + '.bmp'
                    
				frame_path = os.path.join(frame_dir_path, frame_name)
					
				cv2.imwrite(frame_path, frame)

				frame_list.append(frame_path)

				counter = counter + 1
		
		return frame_list
	
	
	def run(self, request, *args, **kwargs):
		
		base_path = '/home/federico/workspace-python/video/'
		
		if request.method == 'POST':
			
			body = json.loads(request.body)
			
			resource_path = base_path + body['resourceName']
		
			frame_list = self.get_frame_list(resource_path)
					
			chunk_size = 22

			job = task_detect_faces.chunks(zip(frame_list), chunk_size)
			
			result = job.apply_async()
			
			face_models = FaceModelsLBP()
			
			final_result = []
			
			for inner_list in result.get():
				
				for result in inner_list:
			
					detection_error = result[ERROR_KEY]
			
					if(not(detection_error)):
			
						face_images = result[FACE_IMAGES_KEY]
					
						for face in face_images:
							
							final_result.append(recognize_face(face, face_models, None, False))
			
			serializer = JobSerializer(Job(resource = body['resourceName'], data = final_result))
                        
			return Response(serializer.data, status = status.HTTP_200_OK)
		
		else:
			
			return Response(data = [], status = status.HTTP_400_BAD_REQUEST)
