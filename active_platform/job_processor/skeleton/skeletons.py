# Copyright (c) 2015, CRS4 S.R.L.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its 
# contributors may be used to endorse or promote products derived 
# from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.

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
		@param execute: Sequential stateless function that will be executed in
				a parallel and/or distributed way oo provided paramters.
				It must be a modular function with less dependences from
				local resources as possibile.
		@type execute: function
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
		@param stages: A set of skeletons corresponding to the ordered list of stages.
		@type stages: List of Skeleton
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
		@param skeleton: Input skeleton that will be applyed/evaluated on each input item.
		@type skeleton: Skeleton
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
		@param split: Skeleton used to transform the Map skeleton input in subsets of smaller data.
		@type split: Skeleton
		@param skeleton: This skeleton will be applyed/evaluated on each subset of data.
		@type skeleton: Skeleton
		@param merge: Skeleton used to convert the set of results in a unique data structure.
		@type merge: Skeleton
		"""
		self.split = split
		self.skeleton = skeleton
		self.merge = merge


# if (conditional) skeleton 
class If(Skeleton):
        """
        This skeleton is used to introduce a control flow based on skeleton evaluation.
	Given two skeleton with the same input and output types, this skeleton pattern evaluates 
	the former skeleton if a boolean condition is true and the latter if the condition is false.
	The boolean condition is another skeleton which determine how the execution flow should
	continue based on the provided input parameters. The same input is provided to the 
	chosed skeleton.
        """
        def __init__(self, cond_skel, true_skel, false_skel):
                """
                @param cond_skel: Skeleton used to decide which one will be used
		@type cond_skel: Skeleton
                @param true_skel: Skeleton evaluated if the boolean condition returns a True value.
		@type true_skel: Skeleton
                @param false_skel: Skeleton evaluated if the boolean condition returns a False value.
		@type false_skel: Skeleton
                """
                self.condition = cond_skel
                self.true_skeleton = true_skel
                self.false_skeleton = false_skel
