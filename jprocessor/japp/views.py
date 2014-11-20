from __future__ import absolute_import

import cv2
import json
import os
import math
import multiprocessing

from abc import ABCMeta, abstractmethod

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from japp.models import Job
from japp.serializers import JobSerializer
from japp.tasks import *
from japp.cake import CacheManager

from japp.tools.Constants import *
        

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

class XMPExtractorList(JobList):
    
    def run(self, request, *args, **kwargs):
        """
        Da modificare - passiamo path dalla request
        """
        
        if request.method == 'POST':
            
            body = json.loads(request.body)
            
            resource_path = body['resourcePath']
        
            #infile = fc.abspath(infile)
            
            result = task_extract_xmp.delay(resource_path)
            
            serializer = JobSerializer(Job(resource = body['resourcePath'], data = result.get()))
                            
            return Response(serializer.data, status = status.HTTP_200_OK)
            
        else:
            
            return Response(data = {}, status = status.HTTP_400_BAD_REQUEST)
            
            
class XMPEmbedderList(JobList):
    
    def run(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            
            body = json.loads(request.body)
            
            componentId = body['componentId']
            
            componentPath = body['componentPath']
            
            changeDict = body['changeDict']
            
            result = task_embed_xmp.apply_async((componentId, componentPath, changeDict))
            
            serializer = JobSerializer(Job(resource = body['componentId'], data = result.get()))
                            
            return Response(serializer.data, status = status.HTTP_200_OK)
            
        else:
            
            return Response(data = {}, status = status.HTTP_400_BAD_REQUEST)
    

class FaceExtractorList(JobList):
    

    def get_frame_list(self, resource_path):
        '''
        Save video frames on disk and returns list of frame paths
        
        :type resource_path: string
        :param resource_path: path of video file
        '''

        frame_dir_path = '/home/federico/workspace-python/video/frames' # Federico
        
        #frame_dir_path = r'C:\Active\Mercurial\jprocessor\Video\Frames' # Pc Lab
        
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
        
        base_path = '/home/federico/workspace-python/video' + os.sep # Federico
        #base_path = r'C:\Active\Mercurial\jprocessor\Video' + os.sep # Pc Lab
        
        if request.method == 'POST':
            
            body = json.loads(request.body)
            
            resource_path = base_path + body['resourceName']
        
            frame_list = self.get_frame_list(resource_path)
            
            frame_nr = len(frame_list)
            
            cpu_nr = multiprocessing.cpu_count()
                    
            chunk_size = int(math.ceil(float(frame_nr) / cpu_nr))

            djob = task_detect_faces.chunks(zip(frame_list), chunk_size)
            
            result = djob.apply_async()
            
            detect_faces = []
            
            for inner_list in result.get():
                
                for result in inner_list:
            
                    detection_error = result[ERROR_KEY]
            
                    if(not(detection_error)):
            
                        face_images = result[FACE_IMAGES_KEY]
                        
                        if len(face_images) > 0:
                        
                            detect_faces.append(face_images)
                            
            
            if len(detect_faces) > 0:
                
                cm = CacheManager()
        
                cm.checkFaceModels()
                    
                faces_nr = len(detect_faces)
                        
                chunk_size = int(math.ceil(float(faces_nr) / cpu_nr))
                
                rjob = task_recognize_faces.chunks(zip(detect_faces), chunk_size)
                
                ret = rjob.apply_async()
                
                serializer = JobSerializer(Job(resource = body['resourceName'], data = ret.get()))
                            
                return Response(serializer.data, status = status.HTTP_200_OK)
        
        else:
            
            return Response(data = [], status = status.HTTP_400_BAD_REQUEST)
            
            
class CaptionExtractor(JobList):
    
    def run(self, request, *args, **kwargs):
        
        base_path = '/home/federico/workspace-python/image' + os.sep
        
        if request.method == 'POST':
            
            body = json.loads(request.body)
            
            resource_path = base_path + body['resourceName']
            
        else:
            
            return Response(data = [], status = status.HTTP_400_BAD_REQUEST)
