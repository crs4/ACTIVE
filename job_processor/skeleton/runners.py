from abc import ABCMeta, abstractmethod
from skeleton.tasks import eval_distributed
from multiprocessing.dummy import Pool
from time import sleep

"""
This module is used to create an abstracton level between how parallel and distributed computations
are implemented and how they are organized through algorithmic skeleton primitives.
So the abstract class SkeletonRunner define a metod necessary to evaluate a generic skeleton,
providing input values and additional parameters.
SkeletonRunner abstract class could be implemented in different way, this leaves a great flexibility for
the definition of how computations are executed over a cluster of nodes or over a workstation.
"""

class SkeletonRunner:
	"""
	Abstract class used to define a generic runner for skeleton evaluation.
	It wiil be possible to instatiate a generic runner, using different
	configurations of the system and different technologies.
	"""
	__metaclass__ = ABCMeta
		
	@abstractmethod	
	def run(self, skeleton, values, *params):
		"""
		Abstract method that will implement the evaluation and execution of a skeleton
		using some kind of parallel and distributed primitives.

		@param skeleton: Skeleton object representing how parallel computations should be done.
		@type skeleton: Skeleton
		@param values: Input values that will be passed to the skeleton for the correct execution.
		@type values: List of objects
		@param params: List of optional parameters that will be passed to enable the computation.
		@type params: list of generic parameters.
		@return: The result provided by skeleton evaluation.
		@rtype: Object
		"""
		pass



class eval_parallel():
	"""
        This class is used to solve the pickle problem introduced by Celery
        when it tries to spread the function over cluster nodes.
        It simply evaluates a skeleton with its parameters and return the results
        """
	def __init__(self, skeleton, executor, percentage):
		"""
		@param skeleton: Skeleton that will be evaluated.
		@type skeleton: Skeleton
	        @param executor: Instance of SkeletonVisitor that will execute skeleton evaluation.
		@type executor: SkeletonVisitor
	        @param percentage: Percentage associated to this skeleton (fraction of the total progress portion).
		@type percentage: int
		"""
		self.skeleton = skeleton
		self.executor = executor
		self.percentage = percentage

	def __call__(self, values):
		"""
		@param values: Input values that will be provided to that skeleton.
		@type values: List of objects
		@return: The result of the skeleton evaluation over the provided input.
		@rtype: Object
		"""
		return self.executor.eval(self.skeleton, values, self.percentage)


class ParallelRunner(SkeletonRunner):
	"""
	This class is used to evaluate a skeleton through parallel primitives.
	This runner allows to execute skeleton evaluation exploiting the
	parallel architecture, using all available processing elements.
	The parallelism is exploited evaulating the skeleton with different
	input elements in parallel and then joining all results.
	"""

	def __init__(self):
		self.pool = Pool(processes=36)
		
	def __del__(self):
		self.pool.close()
		self.pool.terminate()

	def run(self, skeleton, values, *params):
		results = self.pool.map(eval_parallel(skeleton, params[1], params[0]), values)
		self.pool.close()
		return results


class DistributedRunner(SkeletonRunner):
	"""
	This class is used to define the distributed version of skeleton evaluation.
	Celery has been used for the spreading of functions over cluster nodes,
	result collection and fault tolerance.
	The number of processing elements dependes from the number of cluster nodes
	and the parallelism provided by each one.
	Skeleton evaluation is executed synchronously, returning the value only when
	the computation is completed (no asynch result wrapper must be handled).
	"""

	def __init__(self):
		self.result = None

	def __del__(self):
		if(not self.result.ready()):
			self.result.revoke(terminate=True)

	def run(self, skeleton, values, *params):
		self.result = eval_distributed.delay(skeleton, values)
		return self.result.get()
