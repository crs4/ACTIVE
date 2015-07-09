"""
This module contain all decorators used to trigger an event when a function is called (e.g. a view).
"""

from core.plugins.event_manager import EventManager


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
        try:
            request = args[0]
            auth_data = {}
            func_data = res.data

            # detect user credentials and embed them as event input parameter
            if args[0].user and args[0].auth:
                auth_data['user_id'] = args[0].user.pk
                auth_data['token']   = 'Bearer ' + str(args[0].auth.token)
                auth_data['is_root'] = args[0].user.is_superuser or Group.objects.filter(name = 'Admin') in args[0].user.groups.all()
                #print 'Authenticated user ' + str(args[0].user.pk) + ' on event'
                #print auth_data, func_data
                EventManager().start_scripts_by_action(func_path, auth_data, func_data )
        except Exception as e:
            print(e)
        
        print 'Function ', func_path, 'triggered some event'
        return res

    return wrap
