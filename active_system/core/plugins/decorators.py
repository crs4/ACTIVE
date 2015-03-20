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
                func_path = '.'.join((func.__module__, type(func.__self__).__name__, func.__name__))
		# execute the function and collect the result
		res = func(*args, **kwargs)
		# add function results to available keyword arguments
		#kwargs['func_res'] = res
		#args =args + (res.data, )
		
		
		#args = (args[0].data, res.data, )
		#print args
		
		
                # generate an event passing as argument the function name and the result
                EventManager().start_scripts_by_view(func_path, args[0].data, res.data)
                print "E' stata invocata la funzione ", func_path
		return res

        return wrap
