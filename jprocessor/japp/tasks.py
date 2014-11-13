from __future__ import absolute_import

from django.core.cache import cache

from celery import shared_task

from japp.tools.face_detection import detect_faces_in_image
from japp.tools.FaceModelsLBP import FaceModelsLBP
from japp.tools.face_recognition import recognize_face

@shared_task
def task_detect_faces(frame_path):
    
	results = detect_faces_in_image(frame_path, None, False)
    
	return results
	
	
@shared_task
def task_recognize_faces(face_images):
	
	results = []
	
	face_models = get_face_models()
	
	for face in face_images:
	
		rec_result = recognize_face(face, face_models, None, False)
		
		results.append(rec_result)
		
	return results
	
	
def get_face_models():
		
	data = cache.get('model')
	
	if data is not None:
		
		return data
			
	else:
		
		face_models = FaceModelsLBP()

		face_recognizer = face_models.model

		histograms = face_recognizer.getMatVector("histograms")
        
		labels = face_recognizer.getMat("labels")
		
		tags = face_models.get_tags()
            
		fm_dict = {}
		
		fm_dict["histograms"] = histograms

		fm_dict["labels"] = labels
		
		fm_dict["tags"] = tags
			
		cache.set('model', fm_dict, 60)
			
		return fm_dict
