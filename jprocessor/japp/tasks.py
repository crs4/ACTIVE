from __future__ import absolute_import

from celery import shared_task

from japp.tools.face_detection import detect_faces_in_image

@shared_task
def task_detect_faces(frame_path):
    
	results = detect_faces_in_image(frame_path, None, False)
    
	return results
