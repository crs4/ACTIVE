import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager
from face_extraction.factory import * 
from jobprocessor import celery
from time import sleep

NUM_CHUNKS = 6

def get_frames(resource_path):
	print "Estrazione frame file ", resource_path
	return get_frame_list(resource_path)

def face_detection(frame_list):
	print "Frame detection su frame", len(frame_list)
	signature = detect_faces.chunks(zip(frame_list), NUM_CHUNKS)
	ret = signature.apply_async()
	res = ret.get()
	return get_detected_faces(res)
	
def check_models():
	cm = CacheManager()
	cm.checkCachedModels('faceModels')

def face_recognition(detected_faces):
	print "Sono state trovate facce", len(detected_faces)
	signature = recognize_faces.chunks(zip(detected_faces), NUM_CHUNKS)
	ret = signature.apply_async()
	print ret.get()
	
def face_extraction(resource_path):
	frame_list = get_frames(resource_path)
	sleep(10)
	detected_faces = face_detection(frame_list)
	check_models()
	face_recognition(detected_faces)
"""


class GetFrames(Execute):
	def __init__(self, resource_path):
		self.resource_path = resource_path
		
	def execute(self):
		return get_frame_list(resource_path)
		
class FaceDetection(Execute):
	def __init__(self, frame_list):
		self.frame_list = frame_list
		
	def execute(self):
		signature = detect_faces.chunks(zip(self.frame_list), multiprocessing.cpu_count())
		ret = signature.apply_async()
		ret = ret.get()
		return get_detected_faces(ret)
		
class CheckModel(Execute):
	def execute(self):
		cm = CacheManager()
		cm.checkCachedModels('faceModels')
		
class FaceRecognition(Execute):
	def __init__(self, detected_faces):
		self.detected_faces = detected_faces
		
	def execute(self):
		signature = recognize_faces.chunks(zip(self.detected_faces), multiprocessing.cpu_count())
		ret = signature.apply_async()
		ret = ret.get()
		return ret
		
if __name__ == '__main__':
	pipe = Pipe()
	pipe.add_stages([GetFrames(), CheckModel()])"""
