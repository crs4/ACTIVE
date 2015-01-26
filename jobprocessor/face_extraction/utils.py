import cv2
import os
from face_extraction.libs.Constants import ERROR_KEY, FACE_IMAGES_KEY
    
def get_frame_list(resource_path):
	
	frame_dir_path = '/var/spool/active/data/frames'
	
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

def get_detected_faces_from_group_result(detection_results):
	
	detect_faces = []

	for async_result in detection_results.results:
		inner_list = async_result.result
		for result in inner_list:
			detection_error = result[ERROR_KEY]
			if(not(detection_error)):
				face_images = result[FACE_IMAGES_KEY]
				if len(face_images) > 0:
					detect_faces.append(face_images)
					
	return detect_faces
	
def get_detected_faces(detection_results):
	
	detected_faces = []

	#for detection_result in detection_results:
	for dict_result in detection_results: #
		detection_error = dict_result[ERROR_KEY]
		if(not(detection_error)):
			face_images = dict_result[FACE_IMAGES_KEY]
			if len(face_images) > 0:
				detected_faces.append(face_images)
				
	return detected_faces
