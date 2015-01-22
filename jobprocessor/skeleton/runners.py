from abc import ABCMeta, abstractmethod
from skeleton.tasks import *
from multiprocessing.dummy import Pool as ThreadPool

class SkeletonRunner:
	__metaclass__ = ABCMeta
		
	@abstractmethod	
	def run(skeleton, values, *params):
		pass

class ParallelRunner(SkeletonRunner):
	@staticmethod
	def run(skeleton, values, *params):
		pool = ThreadPool(24)
		results = [pool.apply_async(params[0].eval, args=(skeleton, value)) for value in values]
		return [result.get() for result in results]

class DistributedRunner(SkeletonRunner):
	@staticmethod
	def run(skeleton, values, *params):
		sign = eval_distributed.delay(skeleton, values)
		return sign.get()

