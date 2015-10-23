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
from skeleton.decorators import on, when
from skeleton.skeletons import Seq, Pipe, Farm, Map, If
from skeleton.runners import DistributedRunner, ParallelRunner
from multiprocessing import Queue

"""
This module contains all code necessary to implement the semantic of each skeleton.
In particular it has been defined a class that similarly to a visitor pattern allow to evaluate
a skeleton; it is decomposed in its subskeleton and input data is distributed over them.
Inside the Executor class there is an eval method for each skeleton type/class, each one with its
own implementation.

Moreover each executor has a progress field used to provide an estimation of the current
evaluation progress. This field contains an integer percentage value which could be accessed by many thread
concurrently and each one tries to increment the progress values.
"""


class SkeletonVisitor(object):
	"""
	Generic visitor pattern for skeletons. this allows to define different
	ways to evaluate the skeleton tree.
	It contains an abstract method that will be responsible of skeleton evaluation.
	"""
	__metaclass__ = ABCMeta


	@abstractmethod
	def eval(self, skeleton, values, percentage=100):
		"""
		This function is used to evaluate a generic skeleton.
		Given a set of function (one per skeleton) a recursive evaluation is applied.

		@param skeleton: Skeleton that have to be evaluated.
		@type skeleton: Skeleton
		@param values: Input values provided to the skeleton.
		@type values: List of objetcs
		@param percentage: The percentage of the total progress associated to each skeleton.
		@type percentage: int
		@return: The result of skeleton evaluation.
		@rtype: Object
		"""
		pass

	@abstractmethod
        def abort(self):
		"""
		This method is used to stop the evaluation of a skeleton if already started.
		Otherwise it will not be possible to start the evaluation of any provided skeleton. 
		"""
		pass


class Executor(SkeletonVisitor):
	"""
	This class is used to invoke the evaluation and also execution of a
	skeleton over a set of input item.
	The processing progress is tracked using an internal private variable
	that is edit after each sub-skeleton evaluation.
	"""

	def __init__(self):
		# queue shared to handle the processing progress
		self.__progress_queue = Queue()
		# variable used to store the total progress 
		self.__progress = 0
		# set the variable used to stop the skeleton evaluation
		self.__aborted = False	
	
	def __call__(self, skeleton, values):
		"""
		This method makes the evaluator a callable object.
		It is the same as invoking the 'eval' function.

		@param skeleton: Skeletom that must be evaluated.
		@type skeleton: Skeleton
		@param values: The input parameter for skeleton evaluation.
		@type values: List of objects
		@return: The result of skeleton evaluation.
		@rtype: Object
		"""
		return self.eval(skeleton, values)
	
	def add_progress(self, val):
		"""
		This method is used to increase the value
		of the processing progress, adding the parameter
		to the progress queue. Only positive integers are allowed.

		@param val: The value that will increase the progress.
		@type val: int
		"""
		try:
			if(val > 0):
				self.__progress_queue.put(val)
		except:
			pass
	
	def get_progress(self):
		"""
		Method used to compute and return the current value
		of computational progress, in the skeleton evaluation.

		@return: The current computational progress value.
		@rtype: int
		"""
		try:
			# check for any update in the shared queue and sum it to the shared variable
			while(self.__progress_queue.qsize() > 0):
				val = self.__progress_queue.get()
				self.__progress += val
		except:
			pass

		# return the update progress level
		return self.__progress

	def abort(self):
		"""
		This function is used to stop the evaluation of the skeleton (if started)
		or to avoid that it will be started later.
		An internal flag is setted in order to skipt the evaluation.
		"""
		self.__aborted = True

	@on('skeleton')
	def eval(self, skeleton, values, percentage=100):
		"""
		This is the generic method that initializes the dynamic dispatcher.
		"""

	@when(Seq)
	def eval(self, skeleton, values, percentage=100):
		"""
		This method is associated to the Sequential skeleton,
		which actually is computed in a distributed way.
		"""
		if(self.__aborted):
			return None

		result = DistributedRunner().run(skeleton, values)
		self.add_progress(percentage)
		return result

	@when(Pipe)
	def eval(self, skeleton, values, percentage=100):
		"""
		This method is associated to the Pipeline skeleton, so it
		scans the stages evaluating one at time.
		At the end the final result is returned.
		"""
		result = values
		self.add_progress(percentage%len(skeleton.stages))
		for stage in skeleton.stages:
			result = self.eval(stage, result, percentage/len(skeleton.stages))
		return result


	@when(Farm)
	def eval(self, skeleton, values, percentage=100):
		"""
		This method is associated to the Farm skeleton, so it evaluates its
		sub-skeleton for each provided input.
		Actually task parallelism is introduced as a parallel computation.
		The output is the set of computed results.
		"""
		if(self.__aborted):
                        return None

		res = ParallelRunner().run(skeleton.subskel, values, percentage/len(values), self)
		self.add_progress(percentage%len(values))
		return res

	@when(Map)
	def eval(self, skeleton, values, percentage=100):
		"""
                This method is associated to the Map skeleton, so it evaluate its
                sub-skeletons. Also data parallelism is introduced as a parallel computation
		on the node that evaluate the skeleton.
		This skeleton first evaluate the splitter skeleton, obtaining a set of data from
		a single input item, compute each data and the compose all sub results.
                The output is the computed result.
                """
		if(self.__aborted):
                        return None

		splitted_values = self.eval(skeleton.split, values, percentage/3)
		self.add_progress(percentage%3)

		mapped_values = ParallelRunner().run(skeleton.skeleton, splitted_values, (percentage/3)/len(splitted_values), self)
		self.add_progress((percentage/3)%len(splitted_values))

		return self.eval(skeleton.merge, mapped_values, percentage/3)

	@when(If)
        def eval(self, skeleton, values, percentage=100):
                """
                This method is associated to the If skeleton, a control flow skeleton pattern
		based on skeleton evaluation.
		It evaluates a boolean skeleton as condition for the flow execution and then
		it chooses which sub-skeleton must be evaluated.
                """
		if(self.__aborted):
                        return None

                self.add_progress(percentage%3)
                condition = self.eval(skeleton.condition, values, percentage/3)
		if(condition):
			return self.eval(skeleton.true_skeleton, values, (2*percentage)/3)
		return self.eval(skeleton.false_skeleton, values, (2*percentage)/3)
