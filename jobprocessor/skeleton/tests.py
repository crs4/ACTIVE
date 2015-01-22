from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep

import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager



# global sample functions
def increase(num):
	sleep(1)
	return num + 1

def multiply(num):
	sleep(1)
	return num * 2

def identity(val):
	return val

# It instantiates and executes a skeleton on a single sinput value
def compute_skeleton(value):
	# define a pipeline over the previuos skeletons
	pipe = Pipe(Seq(increase), Seq(multiply))
	
	# execute the skeleton with the provided input
	return Executor().eval(pipe, value)


class TestPipe(TestCase):
	def test_1(self):
		# define a pipeline over a single sequential skeleton
		pipe = Pipe(Seq(increase))
		# execute the skeleton with a sample input
		res = Executor().eval(pipe, 1)
		# skeleton computation result check
		self.assertEqual(res, 2)

	def test_2(self):
		# define a sequential skeleton for each function
		# define a pipeline over the previuos skeletons
		pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))

		# execute the skeleton with a sample input
		res = Executor().eval(pipe, 1)

		# skeleton computation result check
		self.assertEqual(res, 5)
		
	def test_3(self):
		# for each sample value instantiate a skeleton object and execute it in parallel
		# using paralle primitives of python (CELERY PRIMITIVES NOT USED HERE)
		params = [1, 2, 3, 4]
		farm = Farm(Pipe(Seq(increase), Seq(multiply), Seq(increase)))
		
		res = Executor().eval(farm, params)

		# skeleton computation result check
		self.assertEqual(res, [5, 7, 9, 11])



class TestFarm(TestCase):
	def test_1(self):
		# define a farm composed by a sequential skeleton
		farm = Farm(Seq(increase))
		# define input values
		values = [1, 2, 3, 4]
		res = Executor().eval(farm, values)
		# check computation results
		self.assertEqual(res, [2, 3, 4, 5])

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
	def test_1(self):
		my_map = Map(Seq(identity), Seq(increase), Seq(identity))
		res = Executor().eval(my_map, [1, 2, 3, 4])
		self.assertEqual(res, [2, 3, 4, 5])

	def test_2(self):
		my_map = Map(Seq(get_frame_list), Seq(detect_faces), Seq(get_detected_faces))
		res = Executor().eval(my_map, '/var/spool/active/data/videolina-10sec.mov')

	def test_3(self):
		pipe = Pipe(Seq(get_frame_list), Seq(split_fun), Farm(Seq(execute_fun)), Seq(merge_fun))
		res = Executor().eval(pipe, '/var/spool/active/data/videolina-10sec.mov')
	

	def test_4(self):
		pipe = Pipe(Seq(get_frame_list), Map(Seq(split_fun), Seq(execute_fun), Seq(merge_fun)))
		res = Executor().eval(pipe, '/var/spool/active/data/videolina-10sec.mov')
		#res = Executor().eval(pipe, '/var/spool/active/data/FicMix.mov')
