import cv2

import os

import sys

from django.test import TestCase

from test_app.tasks import *

sys.path.append("..")

from tools.Constants import *

from tools.FaceModelsLBP import FaceModelsLBP


class TaskTest(TestCase):
    
    def test_face_extraction_by_passing_models(self):
        
        resource_path = r'C:\Active\Mercurial\mprocessor\test_app\video\videolina-10sec.mov'
        
        frame_list = self.get_frame_list(resource_path)
                
        chunk_size = 20
                
        face_models =  FaceModelsLBP()
        
        face_recognizer = face_models.model
        
        histograms = face_recognizer.getMatVector("histograms")
        
        labels = face_recognizer.getMat("labels")
        
        frame_nr = len(frame_list)
        
        fm_list = []
        
        for i in range(0, frame_nr):
            
            fm_dict = {}
            
            fm_dict["histograms"] = histograms
            
            fm_dict["labels"] = labels
            
            fm_list.append(fm_dict)
                
        job = task_extract_faces.chunks(zip(frame_list, fm_list), chunk_size)
            
        result = job.apply_async()
        
    def test_face_extraction(self):
        
        resource_path = r'C:\Active\Mercurial\mprocessor\test_app\video\videolina-10sec.mov'
        
        frame_list = self.get_frame_list(resource_path)
                
        chunk_size = 2
                
        job = task_extract_faces.chunks(zip(frame_list), chunk_size)
            
        result = job.apply_async()    

    def test_face_detection(self):
        
        resource_path = r'C:\Active\Mercurial\mprocessor\test_app\video\videolina-10sec.mov'

        frame_list = self.get_frame_list(resource_path)
                
        chunk_size = 11
        
        job = task_detect_faces.chunks(zip(frame_list), chunk_size)
        
        result = job.apply_async()
        
    def test_hybrid_face_extraction(self):
        
        resource_path = r'C:\Active\Mercurial\mprocessor\test_app\video\videolina-10sec.mov'

        frame_list = self.get_frame_list(resource_path)
                
        chunk_size = 22
        
        job = task_detect_faces.chunks(zip(frame_list), chunk_size)
        
        result = job.apply_async()
        
        face_models =  FaceModelsLBP()
        
        for inner_list in result.get():
            
            for result in inner_list:
        
                detection_error = result[ERROR_KEY]
        
                if(not(detection_error)):
        
                    face_images = result[FACE_IMAGES_KEY]
                
                    for face in face_images:
                    
                        rec_result = recognize_face(face, face_models, None, False)
        
    def test_face_recognition(self):

       resource_path = r'C:\Active\Mercurial\mprocessor\test_app\video\videolina-10sec.mov'
        
       frame_list = self.get_frame_list(resource_path)
                
       chunk_size = 10  
       
       job = task_detect_and_recognize.chunks(zip(frame_list), chunk_size)
       
       result = job.apply_async()       
    
    def get_frame_list(self, resource_path):

        frame_dir_path = r'C:\Active\Mercurial\mprocessor\test_app\video\frames'
        
        capture = cv2.VideoCapture(resource_path)
        
        frame_list = []
        
        if capture is None or not capture.isOpened():

            error = 'Error in opening video file'
            
            print error

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
