import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager
from jobprocessor import celery

def get_frames(resource_path):
	return get_frame_list(resource_path)

def face_detection(frame_list):
	signature = detect_faces.chunks(zip(frame_list), multiprocessing.cpu_count())
	ret = signature.apply_async()
	ret = ret.get()
	return get_detected_faces(ret)
	
def check_models():
	cm = CacheManager()
	cm.checkCachedModels('faceModels')
	
def face_recognition(detected_faces):
	signature = recognize_faces.chunks(zip(detected_faces), multiprocessing.cpu_count())
	ret = signature.apply_async()
	ret = ret.get()
	
def face_extraction(resource_path):
	frame_list = get_frames(resource_path)
	detected_faces = face_detection(frame_list)
	check_models()
	face_recognition(detected_faces)
