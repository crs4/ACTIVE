"""
This module has been defined in order to emulate a method overload
in Python allowing the definition of a visitor pattern for skeletons.
"""

import inspect

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
