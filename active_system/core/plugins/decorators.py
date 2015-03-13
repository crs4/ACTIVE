from core.plugins.event_manager import EventManager

"""
This module contain all decorators used to trigger an event when
a function is called (e.g. a view).
"""

def generate_event(func):
	"""
	This decorator could be associated to any function.
	When the function is called and executed without errors it generates an event passing 
	to the Event Manager the complete absolute path of the function as parameter.
	:param func: Function that will be called and executed.
	:returns: the result of the invoked function.
	"""
        def wrap(*args, **kwargs):
		# obtains the complete absolute path of the considered function
                func_path = '.'.join((func.__module__, args[0].__class__.__name__, func.__name__))
		print "E' stata invocata la funzione ", func_path
		# execute the function and collect the result
		res = func(*args, **kwargs)
                # generate an event passing as argument the function name and the result
                EventManager().start_plugins_by_view(func_path) #, res)
                return res

        return wrap
