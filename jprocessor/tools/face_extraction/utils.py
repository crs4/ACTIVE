import cv2
import os

from jprocessor.tools.face_extraction.lib_face_extraction.Constants import ERROR_KEY, FACE_IMAGES_KEY
    
def get_frame_list(resource_path):
	
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


def get_detected_faces(detection_result):
	
	detect_faces = []
	
	for inner_list in detection_result.results:
		
		inner_list = inner_list.result
		
		for result in inner_list:

			detection_error = result[ERROR_KEY]
	
			if(not(detection_error)):
				face_images = result[FACE_IMAGES_KEY]
				if len(face_images) > 0:
					detect_faces.append(face_images)
					
	return detect_faces
