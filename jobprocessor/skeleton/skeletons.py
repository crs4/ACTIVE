from abc import ABCMeta, abstractmethod

"""
This file is used to define all supported skeletons in order to define/organize 
parallel and distributed computations.
For each skeleton it will be described how and when use it.
Class defined in this module allow just to define how computations are structured
but does not implement any kind of parallelism and don't process data directely.
"""

# generic skeleton structure
class Skeleton:
	"""
	Abstract skeleton used to define common behaviours.
	"""
	__metaclass__ = ABCMeta

# sequential skeleton
class Seq(Skeleton):
	"""
	Sequential skeleton used to wrap a function that will
	be executed sequentially on the provided parameters.
	"""
	def __init__(self, execute):
		"""
		:param execute Sequential stateless function that will be executed in
				a parallel and/or distributed way oo provided paramters.
				It must be a modular function with less dependences from
				local resources as possibile.
		"""
		self.execute = execute

# pipeline skeleton
class Pipe(Skeleton):
	"""
	Pipeline skeleton used to define the order on which other skeleton have to be executed.
	A pipeline is a sequence of stages, where each stage has as input the output of the previous stage.
	First stage needs an input for the computation.
	Last stage provides ads output the computaton result.
	"""
	def __init__(self, *stages):
		"""
		:param params A set of skeletons corresponding to the ordered list of stages.
		"""
		self.stages = []
		for stage in stages:
			self.stages.append(stage)

# farm (master&slave) skeleton
class Farm(Skeleton):
	"""
	This skeleton is used to introduce task parallelism. So given a skeleton and
	a set of items, it will apply the skeleton to each input item.
	The result is a set of values obtained from the individual evaluations.
 	"""
	def __init__(self, skeleton):
		"""
		:param skeleton Input skeleton that will be applyed/evaluated on each input item.
		"""
		self.subskel = skeleton

# map skeleton
class Map(Skeleton):
	"""
	This skeleton is used to introduce data parallelism. So given a composed data structure
	that could be decomposed in subset of items, each subset could be computed independently
	from others, and then results are composed again a whole data structure.
	So parallelism is introduced in the computation of subsets of smaller data.
	"""
	def __init__(self, split, skeleton, merge):
		"""
		:param split 	Skeleton used to transform the Map skeleton input in subsets of smaller data.
		:param skeleton	This skeleton will be applyed/evaluated on each subset of data.
		:param merge	Skeleton used to convert the set of results in a unique data structure.
		"""
		self.split = split
		self.skeleton = skeleton
		self.merge = merge
