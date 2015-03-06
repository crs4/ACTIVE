import inspect

"""
This module has been defined in order to emulate a method overload
in Python allowing the definition of a visitor pattern for skeletons.
"""

"""
def revoke(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		print(args)
		# interrupt function execution
		#if(aborted):
		#	raise Exception("Aborted activity")
			#return None
	
		# wrapper used to pass function arguments
		return func(*args, **kwds)
	return wrapper
"""


def on(param_name):
	def f(fn):
		dispatcher = Dispatcher(param_name, fn)
		return dispatcher
	return f

def when(param_type):
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




