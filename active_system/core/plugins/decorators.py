from core.plugins.event_manager import EventManager

"""
This module contain all decorators used to trigger an event when a function is called (e.g. a view).
"""

def generate_event(func):
	"""
	This decorator could be associated to any function.
	When the function is called and executed without errors it generates an event passing 
	to the Event Manager the complete absolute path of the function as parameter.

	@param func: Function that will be called and executed.
	@type func: function
	@return: The result of the invoked function.
	@rtype: depends on called function
	"""
        def wrap(*args, **kwargs):
		# extract the absolute path of the function
                func_path = '.'.join((func.__module__, type(func.__self__).__name__, func.__name__))
		# execute the function and collect the result
		res = func(*args, **kwargs)
                # generate an event over the called function and its parameters
		input_data = {}
		output_data ={}		
		try:
			input_data = {} #args[0].data
			output_data = res.data
		except Exception as e:
			print(e)
                
		EventManager().start_scripts_by_action(func_path, input_data, output_data )
                print 'Function ', func_path, 'triggered some event'
		return res

        return wrap
