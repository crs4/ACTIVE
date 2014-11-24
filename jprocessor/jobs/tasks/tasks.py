from __future__ import absolute_import
import multiprocessing
from celery import shared_task, chain
from jprocessor.jobs.commons.tasks import callback
from jprocessor.tools.xmp.xmp_extractor import XMPExtractor
from jprocessor.tools.xmp.xmp_embedder import XMPEmbedder
from jprocessor.tools.face_extraction.utils import get_frame_list

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
def detect_faces(arg):
	pass
	
@shared_task
def recognize_faces(arg):
	pass


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
def task_recognize_faces():
	pass
	
@shared_task
def task_extract_faces(resource_path):
	job = (task_detect_faces.s(resource_path) | task_recognize_faces.s() | callback.s())
	return job.apply_async()
