from __future__ import absolute_import

from django.core.cache import cache

from celery import shared_task

from japp.cake import CacheManager

from japp.tools.face_detection import detect_faces_in_image
from japp.tools.face_recognition import recognize_face

@shared_task
def task_detect_faces(frame_path):
    
	results = detect_faces_in_image(frame_path, None, False)
    
	return results
	
	
@shared_task
def task_recognize_faces(face_images):
	
	results = []
	
	cm = CacheManager()
	
	face_models = cm.getCachedModels('faceModels')
	
	for face in face_images:
	
		rec_result = recognize_face(face, face_models, None, False)
		
		results.append(rec_result)
		
	return results
