from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq, If
from skeleton.visitors import Executor
from jobmanager.job import SkeletonJob
from time import sleep

import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager


# Codice generico utilizzato per costruire il job attraverso gli skeleton

def test_2(func_input, job_name):
                pipe = Pipe(Seq(get_frame_list), Farm(Seq(detect_faces)), Seq(get_detected_faces))
		job = SkeletonJob(Executor(), (pipe, func_input[0]), job_name)
		return job








class TestFarm(TestCase):
	def test_2(self):
		pipe = Pipe(Seq(get_frame_list), Farm(Seq(detect_faces)), Seq(get_detected_faces))
		res = Executor().eval(pipe, '/var/spool/active/data/videolina-10sec.mov')



def split_fun(frames):
	length = 24
	return [frames[i:i+length] for i in range(0, len(frames), length)]

def execute_fun(frame_list):
	return map(detect_faces, frame_list)

def merge_fun(detected_faces):
	res = []
	for faces in detected_faces:
		res += faces
	return res


class TestMap(TestCase):
	def test_2(self):
		my_map = Map(Seq(get_frame_list), Seq(detect_faces), Seq(get_detected_faces))
		res = Executor().eval(my_map, '/var/spool/active/data/videolina-10sec.mov')

	def test_3(self):
		pipe = Pipe(Seq(get_frame_list), Seq(split_fun), Farm(Seq(execute_fun)), Seq(merge_fun))
		#res = Executor().eval(pipe, '/var/spool/active/data/FicMix.mov')
		res = Executor().eval(pipe, '/var/spool/active/data/videolina-10sec.mov')
	

	def test_4(self):
		pipe = Pipe(Seq(get_frame_list), Map(Seq(split_fun), Seq(execute_fun), Seq(merge_fun)))
		res = Executor().eval(pipe, '/var/spool/active/data/videolina-10sec.mov')
		#res = Executor().eval(pipe, '/var/spool/active/data/FicMix.mov')
