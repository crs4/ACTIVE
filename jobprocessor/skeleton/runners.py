from abc import ABCMeta, abstractmethod
from skeleton.tasks import *
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

"""
This module is used to create an abstracton level between how parallel and distributed computations
are implemented and how they are organized through algorithmic skeleton primitives.
So the abstract class SkeletonRunner define a metod necessary to evaluate a generic skeleton,
providing input values and additional parameters.
SkeletonRunner abstract class could be implemented in different way, this leaves a great flexibility for
the definition of how computations are executed over a cluster of nodes or over a workstation.
"""

# abstract exector of skeleton computations
class SkeletonRunner:
	__metaclass__ = ABCMeta
		
	@abstractmethod	
	def run(skeleton, values, *params):
		"""
		Abstract method that will implement the evaluation and execution of a skeleton
		using some kind of parallel and distributed primitives.
		:param skeleton: Skeleton object representing how parallel computations should be done.
		:param values: Input values that will be passed to the skeleton for the correct execution.
		:param params: List of optional parameters that will be passed to enable the computation.
		"""
		pass

# runner used to introduce some parallel
# computations during skeleton evaluation
class ParallelRunner(SkeletonRunner):
	@staticmethod
	def run(skeleton, values, *params):
		# create a pool of thread, each one evaluate the skeleton
		# on a portion of the input (supposed to be a list) and wait the computation

		pool = ThreadPool(multiprocessing.cpu_count()) ### limit imposed by available resources ###
		results = [pool.apply_async(params[0].eval, args=(skeleton, value)) for value in values]
		return [result.get() for result in results]

# runner used to introduce some distributed 
# computation during skeleton evaluation
class DistributedRunner(SkeletonRunner):
	@staticmethod
	def run(skeleton, values, *params):
		# skeleton evaluation is done using a celery task
		# distributing the computation over a cluster
		sign = eval_distributed.delay(skeleton, values)
		return sign.get()
