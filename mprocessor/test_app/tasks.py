from __future__ import absolute_import

import cv2

import datetime

import os

import sys

from celery import shared_task, chain

from celery.signals import task_prerun, task_postrun

sys.path.append("..")

from tools.face_extractor import FaceExtractor

from tools.face_detection import detect_faces_in_image

from tools.face_recognition import recognize_face

from tools.Constants import *


first_time = True

start_time = -1

task_counter = 0

@shared_task 
def task_extract_faces(frame_path, face_models = None):
    
    fe = FaceExtractor(face_models)
    
    handle = fe.extractFacesFromImage(frame_path)
    
    results = fe.getResults(handle)
    
    return results
    
@shared_task
def task_detect_faces(frame_path):
    
    results = detect_faces_in_image(frame_path, None, False)
    
    return results
    
@shared_task
def task_detect_faces_for_recognition(frame_path):
    
    results = detect_faces_in_image(frame_path, None, False)
    
    face_images = results[FACE_IMAGES_KEY]
    
    return face_images

@shared_task
def task_recognize_face(face_images):
    
    results = []
    
    for face in face_images:
        
        rec_result = recognize_face(face, None, None, False)
        
        results.append(rec_result)
        
    return results
    
@shared_task
def task_detect_and_recognize(frame_path):
    
    job = chain(task_detect_faces_for_recognition.s(frame_path), task_recognize_face.s())
    
    job.apply_async()
    
@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    
    #res_file_path = r'C:\Active\Mercurial\mprocessor\test_app\video\prerun.txt'
        
    #sys.stdout = open(res_file_path, 'w')
    
    global first_time
    
    global start_time
    
    if(first_time):
        # Save processing time
        start_time = cv2.getTickCount()
        
        first_time = False
    
#@task_success.connect
#def task_postrun_handler(result):
    
    #global task_counter
    
    #task_counter = task_counter + 1
    
#@task_failure.connect
#def task_failure_handler(task_id, exception, *args, **kwargs, traceback, einfo):
    
    #global task_counter
    
    #task_counter = task_counter + 1
        
        
      
