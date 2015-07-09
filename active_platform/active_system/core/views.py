"""
This module is used to create a standard view that could be extended in order
to handle the interaction with the REST API.
Interaction with main HTTP methods are intercepted and an event is generated
for each action (function called).
The interception of events is executed associating as a decorator to each function.
"""

from rest_framework.views import APIView
from core.plugins.decorators import generate_event
import inspect


class EventView(APIView):
    """
    This class could be used as a mixin (multiple inheritance) in order to extend the base APIView
    methods defined in the Django REST framework which are converted in HTTP methods.
    Extending this class it is possible to generate an event every time that one of the main methods
    are called and executed without any thrown (unhandled) exception.
    """

    def __init__(self):
        """
        Constructor used to associate the generate_event decorator to any overridden function.
        """
        super(EventView, self).__init__()
        for x in inspect.getmembers(self, (inspect.ismethod)):
            if x[0] in ('get', 'post', 'put', 'delete', 'as_view', 'options'): #).startswith('__'):
                setattr(self, x[0], generate_event(getattr(self, x[0])))