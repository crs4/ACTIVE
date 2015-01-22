from __future__ import absolute_import
import luigi
import csv
import pickle
import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager
from jobprocessor import celery

class FrameExtractor(luigi.Task):
	resource_path = luigi.Parameter()
	
	def run(self):
		frame_list = get_frame_list(self.resource_path)
		with self.output().open('w') as output:
			outcsv = csv.writer(output, delimiter=',', quotechar='"')
			for frame in frame_list:
				if frame:
					outcsv.writerow([frame])
		
	def output(self):
		return luigi.LocalTarget('/home/federico/target_frames.csv')

class FaceDetection(luigi.Task):
	resource_path = luigi.Parameter()
	
	def requires(self):
		return FrameExtractor(self.resource_path)
		
	def run(self):
		with self.input().open('r') as infile:
			incsv = csv.reader(infile, delimiter=',', quotechar='"')
			frame_list = []
			for line in incsv:
				frame_list.append(line[0])
			signature = detect_faces.chunks(zip(frame_list), multiprocessing.cpu_count())
			ret = signature.apply_async()
			ret = ret.get()
			detected_faces = get_detected_faces(ret)
			
		
		with self.output().open('w') as output:
			pickle.dump(detected_faces, output)
		
	def output(self):
		return luigi.LocalTarget('/home/federico/target_detection.pkl')
	
class FaceRecognition(luigi.Task):
	cm = CacheManager()
	cm.checkCachedModels('faceModels')
	
	def requires(self):
		return FaceDetection(resource_path = '/home/federico/workspace-python/video/videolina-10sec.mov')
		
	def run(self):
		with self.input().open('r') as infile:
			detected_faces = pickle.load(infile)
			signature = recognize_faces.chunks(zip(detected_faces), multiprocessing.cpu_count())
			ret = signature.apply_async()
			ret = ret.get()
			
		with self.output().open('w') as output:
			outcsv = csv.writer(output, delimiter=',', quotechar='"')
			for result in ret:
				if result:
					outcsv.writerow([result])
		
	def output(self):
		return luigi.LocalTarget('/home/federico/target_recognition.csv')
		

if __name__ == "__main__":
	luigi.run()
	#luigi.run(['--task', 'FaceDetection', '--workers', '2'], use_optparse=True)
	#luigi.run(main_task_cls=FaceDetection)
