from abc import ABCMeta, abstractmethod

from skeleton.utils.visit import on, when
from skeleton.skeletons import Seq, Pipe, Farm, Map

from skeleton.runners import DistributedRunner, ParallelRunner

from multiprocessing.dummy import Pool as ThreadPool

class SkeletonVisitor(object):
	"""
	TODO
	"""
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def eval(self, skeleton, values):
		pass


class Executor(SkeletonVisitor):

	@on('skeleton')
	def eval(self, skeleton, values):
		"""
		This is the generic method that initializes the dynamic dispatcher.
		"""
	
	@when(Seq)
	def eval(self, skeleton, values):
		return DistributedRunner.run(skeleton, values)

	@when(Pipe)
	def eval(self, skeleton, values):
		result = values
		for stage in skeleton.stages:
			result = self.eval(stage, result)
		return result

	@when(Farm)
	def eval(self, skeleton, values):
		return ParallelRunner.run(skeleton.subskel, values, self)

	@when(Map)
	def eval(self, skeleton, values):
		splitted_values = self.eval(skeleton.split, values)
		mapped_values = ParallelRunner.run(skeleton.skeleton, splitted_values, self)
		return self.eval(skeleton.merge, mapped_values)


