from django.test import TestCase

from skeleton.skeletons import Farm, Pipe, Map, Seq, If
from skeleton.visitors import Executor	
from time import sleep

# All following functional tests are distributed, parallel or both,
# so they require at least a running Celery node for correct completion.

delay = 2

# global sample functions, with a fake computational delay
def increase(val):
	# increase by one an integer
	sleep(delay)
	return val + 1

def decrease(val):
        # decrease by one an integer
        sleep(delay)
        return val - 1

def multiply(val):
	# multiply by two an integer
	sleep(delay)
	return val * 2

def identity(val):
	# return the input integer
	sleep(delay)
	return val

def sumRow(row):
	# return the sum of input values
        res = 0
        for val in row:
                res += val
        return res

def positive(val):
	# check if the number is positive
	return (val > 0)

def fact(val):
	# compute the factorial of an integer
	res = 1;
        while(val > 1):
                res *= val
		val -= 1
        return res

def split_fun(lists):
	# generate all integers in a give interval
	result = []
	for list in lists:
		result.append(range(list[0], list[-1]))
	return result

def merge_fun(lists):
	# take an interval and return its bounds
	result = []
	for list in lists:
		result.append([list[0], list[-1]])
	return result

def fun_skel(values):
	# creates and compute a simple skeleton
        stage1 = Seq(increase)
        stage2 = Seq(fact)
        stage3 = Seq(decrease)
        pipe = Pipe(stage1, stage2, stage3)
        farm = Farm(pipe)
	res = Executor().eval(farm, values)
	return res
def diarization(val):
	sleep(delay)
	return val

# test for the sequential skeleton (only distributed)
class TestSeq(TestCase):
	def test_1(self):
		# increase by one the input value
		seq = Seq(increase)
		res = Executor().eval(seq, 1)
		self.assertEqual(res, 2)
	
	def test_2(self):
		# multiply by two ther input value
		seq = Seq(multiply)
                res = Executor().eval(seq, 2)
                self.assertEqual(res, 4)

        def test_3(self):
		# simply return the input value
                seq = Seq(identity)
                res = Executor().eval(seq, 8)
                self.assertEqual(res, 8)

	def test_progress(self):
		# check the correct computational progress
                seq = Seq(identity)
		ex = Executor()
                res = ex.eval(seq, 8)
                self.assertEqual(100, ex.get_progress())

	def test_dia(self):
		# check
                seq = Seq(diarization)
		ex = Executor()
                res = ex.eval(seq, "2sec.properties")
                self.assertEqual(100, 100)

# tests for the pipeline skeleton
class TestPipe(TestCase):
	def test_1(self):
		# simple pipeline with only one sequential stage/skeleton
		pipe = Pipe(Seq(increase))
		res = Executor().eval(pipe, 1)
		self.assertEqual(res, 2)

	def test_2(self):
		# pipeline with three sequential stages/skeletons
		pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))
		res = Executor().eval(pipe, 1)
		self.assertEqual(res, 5)
	
        def test_progress(self):
		# check the correct computational progress
                pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))
		ex = Executor()
                res = ex.eval(pipe, 1)
                self.assertEqual(100, ex.get_progress())

	def test_3(self):
		# pipeline with a farm as stage/skeleton
		params = [1, 2, 3, 4]
		pipe = Pipe(Seq(identity), Farm(Seq(increase)))
		res = Executor().eval(pipe, params)
		self.assertEqual(res, [2, 3, 4, 5])

        def test_4(self):
		# pipeline with a large number of stages/skeletons
                params = [1, 2, 3, 4]
                pipe = Pipe(Seq(identity), Farm(Seq(increase)), Seq(identity), Farm(Seq(multiply)), Farm(Seq(increase)))
                res = Executor().eval(pipe, params)
                self.assertEqual(res, [5, 7, 9, 11])

	

# tests for the farm skeleton
class TestFarm(TestCase):
	def test_1(self):
		# simple farm with a sequential sub skeleton
		farm = Farm(Seq(increase))
		params = [1, 2, 3, 4]
		res = Executor().eval(farm, params)
		self.assertEqual(res, [2, 3, 4, 5])

	def test_2(self):
		# farm over a pipeline skeleton
		farm = Farm(Pipe(Seq(increase), Seq(identity), Seq(multiply)))
		params = [1, 2, 3, 4]
                res = Executor().eval(farm, params)
                self.assertEqual(res, [4, 6, 8, 10])

	def test_3(self):
		# farm over a generic skeleton
                farm = Farm(Pipe(Seq(identity), Farm(Seq(multiply)), Seq(identity)))
                params = [[1, 2], [3, 4]]
                res = Executor().eval(farm, params)
                self.assertEqual(res, [[2, 4], [6, 8]])

	def test_progress(self):
		# verify the correct computational progress
                farm = Farm(Pipe(Seq(identity), Farm(Seq(multiply)), Seq(identity)))
                params = [[1, 2], [3, 4]]
		ex = Executor()
                res = ex.eval(farm, params)
                self.assertEqual(100, ex.get_progress())

# tests for the map skeleton
class TestMap(TestCase):
	def test_1(self):
		# simple map with sequential skeletons
		params = [1, 2, 3, 4]
		my_map = Map(Seq(identity), Seq(increase), Seq(identity))
		res = Executor().eval(my_map, params)
		self.assertEqual(res, [2, 3, 4, 5])

	def test_2(self):
		# map with composed skeletons
		params = [1, 2, 3, 4]
		my_map = Map(Seq(identity), Pipe(Seq(increase), Seq(multiply)), Seq(identity))
                res = Executor().eval(my_map, params)
                self.assertEqual(res, [4, 6, 8, 10])

        def test_3(self):
		# map over composed skeletons and composed data
		# third level matrix
		params = [[1, 3],
			  [4, 6],
			  [7, 9]]
                my_map = Map(Seq(identity), Map(Seq(identity), Seq(increase), Seq(identity)), Seq(identity))
                res = Executor().eval(my_map, params)
                self.assertEqual(res,  [[2, 4],
					[5, 7],
					[8, 10]])
	
	def test_4(self):
		# simple map test
		split_phase = Seq(identity)
	        execute_phase = Seq(sumRow)
        	merge_phase = Seq(identity)
	        my_map = Map(split_phase, execute_phase, merge_phase)
        	res = Executor().eval(my_map, [[1, 2], [3, 4]])

		self.assertEqual([3, 7], res)
	
	def test_progress(self):
		# check the correct computational progress
                split_phase = Seq(identity)
                execute_phase = Seq(sumRow)
                merge_phase = Seq(identity)
                my_map = Map(split_phase, execute_phase, merge_phase)
		ex = Executor()
                res = ex.eval(my_map, [[1, 2], [3, 4]])

                self.assertEqual(100, ex.get_progress())


# tests for the If skeleton pattern
class TestIf(TestCase):
        def test_1(self):
		# increase only positive numbers
		cond = Seq(positive)
                inc  = Seq(increase)
		ide  = Seq(identity)
		if_ = If(cond, inc, ide)
                res = Executor().eval(if_, 1)
                self.assertEqual(res, 2)

        def test_2(self):
		# increase only positive numbers
                cond = Seq(positive)
                inc  = Seq(increase)
                ide  = Seq(identity)
                if_ = If(cond, inc, ide)
		farm= Farm(if_)
                res = Executor().eval(farm, [1, 2, -3])
                self.assertEqual(res, [2, 3, -3])

        def test_3(self):
		# increase positive numbers and
		# decrese negative ones
		# and then multiply all by 2
		cond = Seq(positive)
                inc  = Seq(increase)
                ide  = Seq(decrease)
                if_  = If(cond, inc, ide)
		mul  = Seq(multiply)
		pipe = Pipe(if_, mul)
                farm= Farm(pipe)
                res = Executor().eval(farm, [1, 2, -3])
                self.assertEqual(res, [4, 6, -8])

        def test_progress(self):
                # check the correct computational progress
		cond = Seq(positive)
                inc  = Seq(increase)
                ide  = Seq(identity)
                if_ = If(cond, inc, ide)
		ex = Executor()
		res = ex.eval(if_, 1)
                self.assertEqual(100, ex.get_progress())


# mixed tests (combining skeletons)
class TestMix(TestCase):
	def test_1(self):
		values = [1, 2, 3, 4]
		res = fun_skel(values)

		self.assertEqual(res, [1, 5, 23, 119])

	def test_heavy(self):
		values = range(100)
		res = fun_skel(values)
		self.assertEqual(len(res), len(values))



# example of massive usage of Farm pattern
def testFarm():
	values = range(10000)
	farm = Farm(Seq(fact))
	res = Executor().eval(farm, values)
	return res
