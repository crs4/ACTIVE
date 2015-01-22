"""
This file is used to define all skeletons supported by this framework in order to define and 
organize parallel computations. For each skeleton it will be described sematic and how to use it.
Moreover the semantic in a nutshel will be defined for each skeleton.
"""

from abc import ABCMeta, abstractmethod


class Skeleton:
	"""
	Abstract skeleton used to define common behaviours.
	"""
	__metaclass__ = ABCMeta


class Seq(Skeleton):
	"""
	Sequential skeleton used to wrap a function that will
	be computed in a distributed and/or paralle way.
	"""
	def __init__(self, execute):
		self.execute = execute

class Pipe(Skeleton):
	"""
	This skeleton pattern is the most simple that co
	TODO: documentazione e semantica
	"""
	def __init__(self, *stages):
		self.stages = []
		for stage in stages:
			self.stages.append(stage)
	

class Farm(Skeleton):
	"""
	This skeleton is used to introduce data parallelism in a set
	of computations. Given a vector of item of the same type, for each one
	it is possible to compute the same function in a parallel way.
	Computation executed could also be composed like another skeleton.
	TODO: definire semantica
 	"""
	def __init__(self, skeleton):
		self.subskel = skeleton


class Map(Skeleton):
	"""
	This skeleton could be described as a composition of previuos ones.
	In particular as: Pipe(split_skeleton, Farm(skeleton), merge_skeleton)
	But this skeleton have to be used for data parallelism computations, when
	a composed data struture must be divided in smaller data and then merged together.
	Parallelism is introduced on the indipendent computation of subsets of smaller data.
	TODO: definire semantica
	"""
	def __init__(self, split, skeleton, merge):
		self.split = split
		self.skeleton = skeleton
		self.merge = merge
