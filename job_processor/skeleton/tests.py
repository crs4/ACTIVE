"""
This module contains the tests necessary to execute some skeletons in a
parallel and distributed enviroment.
They have been created only for functional test (performances are not involved).
"""

from django.test import TestCase
from skeleton.skeletons import Farm, Pipe, Map, Seq, If
from skeleton.visitors import Executor	
from time import sleep

# delay introduced for debug purposes
delay = 0.1


def increase(val):
    """
    Function used to increase by one an integer parameter.

    @param val: Value that will be increased by one.
    @type val: int
    @return: The parameter increased by one.
    @rtype: int
    """
    # increase by one an integer
    sleep(delay)
    return val + 1

def decrease(val):
    """
    Function used to decrease by one an integer parameter.

    @param val: Value that will be decreases by one.
    @type val: int
    @return: The parameter decreased by one.
    @rtype: int
    """
    sleep(delay)
    return val - 1

def multiply(val):
    """
    Function used to multiply by two an integer parameter.

    @param val: Value that will be multiplied by two.
    @type val: int
    @return: The parameter multiplied for two.
    @rtype: int
    """
    sleep(delay)
    return int(val) * 2

def identity(val):
    """
    Function that return the input value.

    @param val: Value that will be returned.
    @type val: int
    @return: The input parameter value.
    @rtype: int
    """
    sleep(delay)
    return val

def sumRow(row):
    """
    Function that sum an array of integers and return the computed value.

    @param row: Array of integers values that will be summed.
    @type row: Array of int
    @return: The sum of input values.
    @rtype: int
    """
    res = 0
    for val in row:
            res += val
    return res

def positive(val):
    """
    Function used to check if integer parameter is positive or not.

    @param val: Integer parameter checked for positive value.
    @type val: int
    @return: The boolean check result.
    @rtype: bool
    """
    return (val > 0)

def fact(val):
    """
    Function used to compute the factorial of an integer parameter.

    @param val: Integer input value.
    @type val: int
    @return: The factorial of the input parameter.
    @rtype: int
    """
    res = 1
    while(val > 1):
            res *= val
            val -= 1
    return res

def split_fun(lists):
    """
    Function used to create a list of sequences of integers,
    starting from a list of couples of integer values.

    @param lists: List of integer couples.
    @param lists: List of list of integer
    @return: List of sequence of integers.
    @rtype: List of list of integers
    """
    result = []
    for list in lists:
        result.append(range(list[0], list[-1]))
    return result

def merge_fun(lists):
    """
    Function used to take a sequence of integers and
    return its boundaries.
    
    @param lists: List of sequence of integers.
    @type lists: List of list of integer
    @return: List of couple of integers, corresponding to sequence boundaries.
    @rtype: List of list of integers
    """
    result = []
    for list in lists:
        result.append([list[0], list[-1]])
    return result

def fun_skel(values):
    """
    Function used to evaluate a skeleton, which given a sequence
    of integers try to compute in parallel the:
    - increase by one of each integer
    - factorial of the previous result
    - decrease by one of the previous result
    
    @param values: List of integers that will be provided to the skeleton.
    @type values: List of integer
    @return: List of computed values.
    @rtype: List of integer
    """
    stage1 = Seq(increase)
    stage2 = Seq(fact)
    stage3 = Seq(decrease)
    pipe = Pipe(stage1, stage2, stage3)
    farm = Farm(pipe)
    res = Executor().eval(farm, values)
    return res


class TestSeq(TestCase):
    """
    Class used to test the Sequential skeleton execution.
    Sequential skeletons are executed in a distributed environment.
    """
    def test_1(self):
        """
        Increase by one the input value.
        """
        seq = Seq(increase)
        res = Executor().eval(seq, (1,))
        self.assertEqual(res, 2)
	
    def test_2(self):
        """
        Multiply by two the input value.
        """
        seq = Seq(multiply)
        res = Executor().eval(seq, (2,))
        self.assertEqual(res, 4)

    def test_3(self):
        """
        Simply return the input value.
        """
        seq = Seq(identity)
        res = Executor().eval(seq, (8,))
        self.assertEqual(res, 8)

    def test_progress(self):
        """
        Check the correct computational progress
        """
        seq = Seq(identity)
        ex = Executor()
        res = ex.eval(seq, (8,))
        self.assertEqual(100, ex.get_progress())


class TestPipe():#TestCase):
    """
    Class used to test the pipeline skeleton
    """
    
    def test_1(self):
        """
        Simple pipeline with only one sequential stage/skeleton.
        """
        pipe = Pipe(Seq(increase))
        res = Executor().eval(pipe, 1)
        self.assertEqual(res, 2)

    def test_2(self):
        """
        Pipeline with three sequential stages/skeletons.
        """
        pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))
        res = Executor().eval(pipe, 1)
        self.assertEqual(res, 5)
	
    def test_progress(self):
        """
        Check the correct computational progress.
        """
        pipe = Pipe(Seq(increase), Seq(multiply), Seq(increase))
        ex = Executor()
        res = ex.eval(pipe, 1)
        self.assertEqual(100, ex.get_progress())

    def test_3(self):
        """
        Pipeline with a farm as stage/skeleton.
        """
        params = [1, 2, 3, 4]
        pipe = Pipe(Seq(identity), Farm(Seq(increase)))
        res = Executor().eval(pipe, params)
        self.assertEqual(res, [2, 3, 4, 5])

    def test_4(self):
        """
        Pipeline with a large number of stages/skeletons.
        """
        params = [1, 2, 3, 4]
        pipe = Pipe(Seq(identity), Farm(Seq(increase)), Seq(identity), Farm(Seq(multiply)), Farm(Seq(increase)))
        res = Executor().eval(pipe, params)
        self.assertEqual(res, [5, 7, 9, 11])

	
class TestFarm():#TestCase):
    """
    Class used to test the Farm skeleton.
    """
    
    def test_1(self):
        """
        Simple farm with a sequential sub skeleton.
        """
        farm = Farm(Seq(increase))
        params = [1, 2, 3, 4]
        res = Executor().eval(farm, params)
        self.assertEqual(res, [2, 3, 4, 5])

    def test_2(self):
        """
        Farm over a pipeline skeleton that is executed on each parameter.
        """
        farm = Farm(Pipe(Seq(increase), Seq(identity), Seq(multiply)))
        params = [1, 2, 3, 4]
        res = Executor().eval(farm, params)
        self.assertEqual(res, [4, 6, 8, 10])

    def test_3(self):
        """
        Farm over a generic skeleton (pipeline of sequential stages).
        """
        farm = Farm(Pipe(Seq(identity), Farm(Seq(multiply)), Seq(identity)))
        params = [[1, 2], [3, 4]]
        res = Executor().eval(farm, params)
        self.assertEqual(res, [[2, 4], [6, 8]])

    def test_progress(self):
        """
        Check the computational progress.
        """
        farm = Farm(Pipe(Seq(identity), Farm(Seq(multiply)), Seq(identity)))
        params = [[1, 2], [3, 4]]
        ex = Executor()
        res = ex.eval(farm, params)
        self.assertEqual(100, ex.get_progress())


class TestMap():#TestCase):
    """
    Class used to test the Map skeleton evaluation.
    """
    
    def test_1(self):
        """
        Simple Map with sequential skeletons as sub skeletons.
        """
        params = [1, 2, 3, 4]
        my_map = Map(Seq(identity), Seq(increase), Seq(identity))
        res = Executor().eval(my_map, params)
        self.assertEqual(res, [2, 3, 4, 5])

    def test_2(self):
        """
        Map with composed skeletons.
        """
        params = [1, 2, 3, 4]
        my_map = Map(Seq(identity), Pipe(Seq(increase), Seq(multiply)), Seq(identity))
        res = Executor().eval(my_map, params)
        self.assertEqual(res, [4, 6, 8, 10])

    def test_3(self):
        """
        Check the Map skeleton using composed skeletons and composed data.
        """
        # third level matrix
        params = [[1, 3], [4, 6], [7, 9]]
        my_map = Map(Seq(identity), Map(Seq(identity), Seq(increase), Seq(identity)), Seq(identity))
        res = Executor().eval(my_map, params)
        self.assertEqual(res,  [[2, 4], [5, 7], [8, 10]])

    def test_4(self):
        """
        Simple Map skeleton test.
        """
        split_phase = Seq(identity)
        execute_phase = Seq(sumRow)
        merge_phase = Seq(identity)
        my_map = Map(split_phase, execute_phase, merge_phase)
        res = Executor().eval(my_map, [[1, 2], [3, 4]])
        self.assertEqual([3, 7], res)

    def test_progress(self):
        """
        Check the correct computational progress.
        """
        split_phase = Seq(identity)
        execute_phase = Seq(sumRow)
        merge_phase = Seq(identity)
        my_map = Map(split_phase, execute_phase, merge_phase)
        ex = Executor()
        res = ex.eval(my_map, [[1, 2], [3, 4]])
        self.assertEqual(100, ex.get_progress())


class TestIf():#TestCase):
    """
    Class used to test the If skeleton over different sub skeletons.
    """

    def test_1(self):
        """
        Increase by one only positive numbers
        """
        cond = Seq(positive)
        inc  = Seq(increase)
        ide  = Seq(identity)
        if_ = If(cond, inc, ide)
        res = Executor().eval(if_, 1)
        self.assertEqual(res, 2)

    def test_2(self):
        """
        Increase only positive numbers in an array of integers.
        """
        cond = Seq(positive)
        inc  = Seq(increase)
        ide  = Seq(identity)
        if_ = If(cond, inc, ide)
        farm= Farm(if_)
        res = Executor().eval(farm, [1, 2, -3])
        self.assertEqual(res, [2, 3, -3])

    def test_3(self):
        """
        Increase by one positive integers and decrease by one negative integers.
        The results are then multiplied by two.
        """
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
        """
        Check the correct computational progress.
        """
        cond = Seq(positive)
        inc  = Seq(increase)
        ide  = Seq(identity)
        if_ = If(cond, inc, ide)
        ex = Executor()
        res = ex.eval(if_, 1)
        self.assertEqual(100, ex.get_progress())


class TestMix():#TestCase):
    """
    Class used to execute mix tests and check if all values are computed.
    """

    def test_1(self):
        """
        Execute a custom skeleton on a list of interges.
        """
        values = [1, 2, 3, 4]
        res = fun_skel(values)
        self.assertEqual(res, [1, 5, 23, 119])

    def test_heavy(self):
        """
        Execute a custom skeleton on a list of 100 integers and then
        compare the input and output cardinalities.
        """
        values = range(1000)
        res = fun_skel(values)
        self.assertEqual(len(res), len(values))

    def test_light(self):
        """
        Test the parallel and distributed execution through Farm skeleton.
        """
        values = range(1000)
        farm = Farm(Seq(increase))
        res = Executor().eval(farm, values)
        return res
