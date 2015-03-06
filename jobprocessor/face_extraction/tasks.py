from __future__ import absolute_import
from celery import shared_task
from face_extraction.libs.face_detection import detect_faces_in_image
from face_extraction.libs.face_recognition import recognize_face
from face_extraction.cake import CacheManager

#@shared_task
def detect_faces(frame_path):
	return detect_faces_in_image(frame_path, None, False)
	
#@shared_task
def recognize_faces(face_images):
	results = []
	
	cm = CacheManager()
	face_models = cm.checkCachedModels('faceModels')
	
	for face in face_images:
		rec_result = recognize_face(face, face_models, None, False)
		results.append(rec_result)
		
	return results
