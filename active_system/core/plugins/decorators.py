"""
This module contain all decorators used to trigger an event when a function is called (e.g. a view).
"""

from core.plugins.event_manager import EventManager
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


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
        input_data  = {}
        output_data = {}
        try:
            output_data = res.data
        except Exception as e:
            logger.error('Error on event parameter extraction for ' + func_path)
            print e

        if args[0].user:
            input_data['user_id'] = args[0].user.pk
        if args[0].auth:
            input_data['token']   = args[0].auth.token

        logger.info('Triggered all events associated to ' + func_path)
        EventManager().start_scripts_by_action(func_path, input_data, output_data)

        return res

    return wrap
