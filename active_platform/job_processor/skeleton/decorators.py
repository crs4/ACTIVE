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

import inspect

"""
This module has been defined in order to emulate a method overload
in Python allowing the definition of a visitor pattern for skeletons.
"""

def on(param_name):
	'''
	This function is used to dispatch a function call on
	another function, simulating the function overload.
	@param param_name: Name of the parameter that will be used to dispatch the function call
	@type param_name: string
	@return: A function incapsulating the dispatcher
	@rtype: function
	'''
	def f(fn):
		dispatcher = Dispatcher(param_name, fn)
		return dispatcher
	return f

def when(param_type):
	'''
	This function is used to map a function to a specific parameter type.
	This allows the dispatcher to select the correct function by parameter value.
	@param param_type: Value of the considered parameter.
	@type param_type: string
	@return: The function mapped to the current parameter value.
	@rtype: function
	'''
	def f(fn):
		frame = inspect.currentframe().f_back
		dispatcher = frame.f_locals[fn.func_name]
		if not isinstance(dispatcher, Dispatcher):
			dispatcher = dispatcher.dispatcher
		dispatcher.add_target(param_type, fn)
		def ff(*args, **kw):
			return dispatcher(*args, **kw)
		ff.dispatcher = dispatcher
		return ff
	return f
 
class Dispatcher(object):
	'''
	Class used to implement the function dispatcher.
	This class will provide all necessary methods in order to
	emulate the function overload in Python.
	'''
	def __init__(self, param_name, fn):
		frame = inspect.currentframe().f_back.f_back
		top_level = frame.f_locals == frame.f_globals
		self.param_index = inspect.getargspec(fn).args.index(param_name)
		self.param_name = param_name
		self.targets = {}
 	
	def __call__(self, *args, **kw):
		typ = args[self.param_index].__class__
		d = self.targets.get(typ)

		if d is not None:
			return d(*args, **kw)
		else:
			issub = issubclass
			t = self.targets
			ks = t.iterkeys()
			return [t[k](*args, **kw) for k in ks if issub(typ, k)]
 
	def add_target(self, typ, target):
		self.targets[typ] = target
