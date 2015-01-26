from abc import ABCMeta, abstractmethod
from skeleton.visit import on, when
from skeleton.skeletons import Seq, Pipe, Farm, Map
from skeleton.runners import DistributedRunner, ParallelRunner
from multiprocessing.dummy import Pool as ThreadPool

"""
This module contains all code necessary to implement the semantic of each skeleton.
In particular it has been defined a class that similarly to a visitor pattern allow to evaluate
a skeleton; it is decomposed in its subskeleton and input data is distributed over them.
Inside the Executor class there is an eval method for each skeleton type/class, each one with its
own implementation.
"""

# generic skeleton visitor
class SkeletonVisitor(object):
	"""
	Generic visitor pattern for skeletons.
	It contains an abstract method that will be responsible of skeleton evaluation.
	"""
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def eval(self, skeleton, values):
		"""
		:param skeleton: Skeleton that have to be evaluated.
		:param values: Input values provided to the skeleton.
		"""
		pass

# instatiate a kind of visitor pattern for skeletons
class Executor(SkeletonVisitor):
	"""
	This class is used to invoke the evaluation and also execution of a
	skeleton over a set of input item(s).
	"""
	@on('skeleton')
	def eval(self, skeleton, values):
		"""
		This is the generic method that initializes the dynamic dispatcher.
		"""
	
	@when(Seq)
	def eval(self, skeleton, values):
		"""
		This method is associated to the Sequential skeleton,
		which actually is computed in a distributed way.
		:param skeleton:	Sequential skeleton containing the function to compute.
		:values values:	Input values necessary for function computation.
		"""
		return DistributedRunner.run(skeleton, values)

	@when(Pipe)
	def eval(self, skeleton, values):
		"""
		This method is associated to the Pipeline skeleton, so it
		scans the stages evaluating one at time.
		At the end the final result is returned.
		:param skeleton: Pipeline skeleton containing subskeleton (stages).
		:param values: 	Input values for the first stage of the pipeline.
		"""
		result = values
		for stage in skeleton.stages:
			result = self.eval(stage, result)
		return result

	@when(Farm)
	def eval(self, skeleton, values):
		"""
		This method is associated to the Farm skeleton, so it evaluate its
		sub-skeleton for each provided input.
		Actually task parallelism is introduced as a parallel computation.
		The output is the set of computed results.
		:param skeleton:	Farm skeleton containing sub-skeleton that will be replicated.
		:param values:	Input values that could be processed independently.
		"""
		return ParallelRunner.run(skeleton.subskel, values, self)

	@when(Map)
	def eval(self, skeleton, values):
		"""
                This method is associated to the Map skeleton, so it evaluate its
                sub-skeletons. Also data parallelism is introduced as a parallel computation
		on the node that evaluate the skeleton.
		This skeleton first evaluate the splitter skeleton, obtaining a set of data from
		a single input item, compute each data and the compose all sub results.
                The output is the computed result.
                :param skeleton: Map skeleton containing split, merge and main sub-skeleton.
                :param values:   Input value that will be splitted in independent subsets.
                """
		splitted_values = self.eval(skeleton.split, values)
		mapped_values = ParallelRunner.run(skeleton.skeleton, splitted_values, self)
		return self.eval(skeleton.merge, mapped_values)
