import cv2

import multiprocessing

from django.test import TestCase

from japp.tools.Constants import *

from japp.tasks import *


class TaskTest(TestCase):    

    def get_frame_list(self, resource_path):
        '''
        Save video frames on disk and returns list of frame paths
        
        :type resource_path: string
        :param resource_path: path of video file
        '''

        #frame_dir_path = '/home/federico/workspace-python/video/frames' # Federico
        
        frame_dir_path = r'C:\Active\Mercurial\jprocessor\Video\Frames' # Pc Lab
        
        capture = cv2.VideoCapture(resource_path)
        
        frame_list = []
        
        if capture is None or not capture.isOpened():
            
            error = 'Error in opening video file'

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

    
    def test_face_extraction(self):
		
		base_path = '/home/federico/workspace-python/video' + os.sep
			
		resource_path = base_path + 'videolina-10sec.mov'
	
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
			
			rame_nr = len(frame_list)
            
			faces_nr = len(detect_faces)
                    
            chunk_size = int(math.ceil(float(faces_nr) / cpu_nr))
			
			cm = CacheManager()
	
			cm.checkFaceModels()
			
			rjob = task_recognize_faces.chunks(zip(detect_faces), chunk_size)
		
			ret = rjob.apply_async()
		
			ret.get()
   
    
