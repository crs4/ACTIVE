from __future__ import absolute_import

from django.core.cache import cache

from celery import shared_task, chain
from celery.signals import task_postrun

from japp.cake import CacheManager

from japp.tools.face_detection import detect_faces_in_image
from japp.tools.face_recognition import recognize_face
from japp.tools.xmp.xmp_extractor import XMPExtractor
from japp.tools.xmp.xmp_embedder import XMPEmbedder
#from japp.tools.cmd.generic_cmd import GenericCmdline

@shared_task
def callback(ret):
    return ret
    
@task_postrun.connect
def on_task_postrun(sender = None, signal = None, task_id = None, task = None, args = None, kwargs = None, retval = None, state = None):
    if task.name == 'japp.tasks.callback':
        print(task_id)
        print(state)
        print(retval)

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

@shared_task
def extract_xmp(resource_path):
    xmpExtractor = XMPExtractor()
    return xmpExtractor.extract(resource_path)
    
@shared_task
def embed_xmp(component_id, component_path, changes):
    xmpEmbedder = XMPEmbedder()
    return xmpEmbedder.metadata_synch(component_id, component_path, changes)
    
@shared_task
def task_extract_xmp(resource_path):
    job = (extract_xmp.s(resource_path) | callback.s())
    return job.apply_async()
    
@shared_task
def task_embed_xmp(component_id, component_path, changes):
    job = (embed_xmp.s(component_id, component_path, changes) | callback.s())
    return job.apply_async()

""" 
@shared_task
def task_execute_cmd(cmd, args, env = {}, progress_url = None):
    
    genericCmdline = GenericCmdline()
    
    genericCmdline.call(cmd = cmd, args = args, env = env, progress_url = progress_url)"""
    
    
