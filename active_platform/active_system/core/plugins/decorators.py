# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contain all decorators used to trigger an event when a function is called (e.g. a view).
"""

from django.contrib.auth.models import Group
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
                auth_data['is_root'] = args[0].user.is_superuser or len(args[0].user.groups.filter(name='Admin'))
                EventManager().start_scripts_by_action(func_path, auth_data, func_data )
        except Exception as e:
            print(e)
        
        return res

    return wrap
