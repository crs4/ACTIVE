"""
This module is used to detect and return all available ACTIVE Tools.
ACTIVE Tools are detected looking at the system variable containing
all application installed inside the platform "tools" directory.
"""

from rest_framework.views import APIView, Response
from django.conf import settings
from core.active_tools.models import ActiveTools
#from django.core.urlresolvers import reverse
#import json
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ActiveToolsList(APIView):
    """
    This class is used to retrieve all installed ACTIVE tools.
    It returns a dictionary which defines the association between tools and urls.
    """
    model = ActiveTools

    def get(self, request, format=None):
        """
        Method used to retrieve all available ACTIVE tools.

        @param request: HttpRequest use to retrieve all ACTIVE tools.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized ACTIVE tools.
        @rtype: HttpResponse
        """
        logger.debug('Requested all installed ACTIVE Tools')
        tools = [a for a in settings.INSTALLED_APPS if a.startswith('tools.')]
        dict = {}
        for t in tools:
            name = t.strip('tools').strip('.')
            dict[name] = t

        logger.debug('Returned all installed ACTIVE Tools')
        return Response(dict)