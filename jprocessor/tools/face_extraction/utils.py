import cv2
import os
    
def get_frame_list(self, resource_path):
	
	frame_dir_path = '/home/federico/workspace-python/video/frames'
	
	capture = cv2.VideoCapture(resource_path)
	
	frame_list = []
	
	if capture is None or not capture.isOpened():
		
		error = 'Error in opening video file'
		
		print(error)

	else:       

		counter = 0
		
		while True:
			
			ret, frame = capture.read()
			
			if(not(ret)):
				
				break
				
			frame_name = str(counter) + '.jpg'
			frame_path = os.path.join(frame_dir_path, frame_name)
			cv2.imwrite(frame_path, frame)
			frame_list.append(frame_path)
			counter = counter + 1
	
	return frame_list
