from __future__ import absolute_import
import multiprocessing
from celery import shared_task, chain
from jprocessor.cake import CacheManager
from jprocessor.jobs.commons.tasks import callback
from jprocessor.tools.xmp.xmp_extractor import XMPExtractor
from jprocessor.tools.xmp.xmp_embedder import XMPEmbedder
from jprocessor.tools.face_extraction.utils import get_frame_list, get_detected_faces
from jprocessor.tools.face_extraction.lib_face_extraction.face_detection import detect_faces_in_image
from jprocessor.tools.face_extraction.lib_face_extraction.face_recognition import recognize_face

"""
One-shot tasks.
"""

@shared_task
def extract_xmp(file_path):
    xmpExtractor = XMPExtractor()
    return xmpExtractor.extract(file_path)
    
@shared_task
def embed_xmp(component_id, component_path, changes):
	xmpEmbedder = XMPEmbedder()
	return xmpEmbedder.metadata_synch(component_id, component_path, changes)

@shared_task
def detect_faces(frame_path):
	return detect_faces_in_image(frame_path, None, False)
	
@shared_task
def recognize_faces(face_images):
	results = []
	
	cm = CacheManager()
	face_models = cm.getCachedModels('faceModels')
	
	for face in face_images:
		rec_result = recognize_face(face, face_models, None, False)
		results.append(rec_result)
		
	return results
	
"""
@shared_task
def recognition_voice(singola-sub-track):
	pass
"""

"""
Workflows - pipes and chunks.
"""
	
@shared_task
def task_extract_xmp(resource_path):
	job = (extract_xmp.s(resource_path) | callback.s())
	return job.apply_async()
	
@shared_task
def task_embed_xmp(component_id, component_path, changes):
	job = (embed_xmp.s(component_id, component_path, changes) | callback.s())
	return job.apply_async()
	
@shared_task
def task_detect_faces(resource_path):
	frame_list = get_frame_list(resource_path)
	return detect_faces.chunks(zip(frame_list), multiprocessing.cpu_count())
	
@shared_task
def task_recognize_faces(detection_result):
	detected_faces = get_detected_faces(detection_result)
	return recognize_faces.chunks(zip(detected_faces), multiprocessing.cpu_count())
	
@shared_task
def task_extract_faces(resource_path):
	job = (task_detect_faces.s(resource_path) | task_recognize_faces.s() | callback.s())
	return job.apply_async()
	
"""
@shared_task
def task_voice_extraction():
	#get list
	job = recognition_voice.chunks(zip(voice_list), multiprocessing.cpu_count())
	return job.apply_async()

@shared_task
def task_voice_extraction_callback():
	job = (task_voice_extraction.s(resource_path) | callback.s())
	return job.apply_async()
"""
