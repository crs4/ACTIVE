from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq
from skeleton.visitors import Executor	
from time import sleep

import multiprocessing
from face_extraction.utils import get_frame_list, get_detected_faces
from face_extraction.tasks import detect_faces, recognize_faces
from face_extraction.cake import CacheManager



# global sample functions, with a fake computational delay
def increase(val):
	sleep(1)
	return val + 1

def multiply(val):
	sleep(1)
	return val * 2

def identity(val):
	sleep(1)
	return val

# represent an interval of integers as a couple of indexes in a list
# this function generate the extended representation for each list
def split_fun(lists):
	result = []
	for list in lists:
		result.append(range(list[0], list[-1]))
	print result
	return result
# this function take the list of extended intervals and compress them
def merge_fun(lists):
	result = []
	for list in lists:
		result.append([list[0], list[-1]])
	
	print result
	return result



# test for the sequential skeleton (no parallelization)
class TestSeq(TestCase):
	def test_1(self):
		seq = Seq(increase)
		res = Executor().eval(seq, 1)
		self.assertEqual(res, 2)
	
	def test_2(self):
		seq = Seq(multiply)
                res = Executor().eval(seq, 2)
                self.assertEqual(res, 4)

        def test_3(self):
                seq = Seq(identity)
                res = Executor().eval(seq, 8)
                self.assertEqual(res, 8)


# tests for the pipeline skeleton
class TestPipe(TestCase):
	# simple pipeline with only one sequential stage/skeleton
	def test_1(self):
		pipe = Pipe(Seq(increase))
		res = Executor().eval(pipe, 1)
		self.assertEqual(res, 2)

	# pipeline with three sequential stages/skeletons
	def test_2(self):
		pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))
		res = Executor().eval(pipe, 1)
		self.assertEqual(res, 5)

	# pipeline with a farm as stage/skeleton
	def test_3(self):
		params = [1, 2, 3, 4]
		pipe = Pipe(Seq(identity), Farm(Seq(increase)))
		res = Executor().eval(pipe, params)
		self.assertEqual(res, [2, 3, 4, 5])

	# pipeline with a large number of stages/skeletons
        def test_4(self):
                params = [1, 2, 3, 4]
                pipe = Pipe(Seq(identity), Farm(Seq(increase)), Seq(identity), Farm(Seq(multiply)), Farm(Seq(increase)))
                res = Executor().eval(pipe, params)
                self.assertEqual(res, [5, 7, 9, 11])

# tests for the farm skeleton
class TestFarm(TestCase):
	# simple farm with a sequential sub skeleton
	def test_1(self):
		farm = Farm(Seq(increase))
		params = [1, 2, 3, 4]
		res = Executor().eval(farm, params)
		self.assertEqual(res, [2, 3, 4, 5])

	# farm over a pipeline skeleton
	def test_2(self):
		farm = Farm(Pipe(Seq(increase), Seq(identity), Seq(multiply)))
		params = [1, 2, 3, 4]
                res = Executor().eval(farm, params)
                self.assertEqual(res, [4, 6, 8, 10])

	# farm over a generic skeleton
	def test_3(self):
                farm = Farm(Pipe(Seq(identity), Farm(Seq(multiply)), Seq(identity)))
                params = [[1, 2], [3, 4]]
                res = Executor().eval(farm, params)
                self.assertEqual(res, [[2, 4], [6, 8]])

# tests for the map skeleton
class TestMap(TestCase):
	# simple map with sequential skeletons
	def test_1(self):
		params = [1, 2, 3, 4]
		my_map = Map(Seq(identity), Seq(increase), Seq(identity))
		res = Executor().eval(my_map, params)
		self.assertEqual(res, [2, 3, 4, 5])

	# map with composed skeletons
	def test_2(self):
		params = [1, 2, 3, 4]
		my_map = Map(Seq(identity), Pipe(Seq(increase), Seq(multiply)), Seq(identity))
                res = Executor().eval(my_map, params)
                self.assertEqual(res, [4, 6, 8, 10])

	 # map over composed skeletons and composed data
        def test_3(self):
		# third level matrix
		params = [[1, 3],
			  [4, 6],
			  [7, 9]]
                my_map = Map(Seq(identity), Map(Seq(identity), Seq(increase), Seq(identity)), Seq(identity))
                res = Executor().eval(my_map, params)
                self.assertEqual(res,  [[2, 4],
					[5, 7],
					[8, 10]])
