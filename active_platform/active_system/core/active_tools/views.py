# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to detect and return all available ACTIVE Tools.
ACTIVE Tools are detected looking at the system variable containing
all application installed inside the platform "tools" directory.
"""

from core.active_tools.models import ActiveTools
from django.conf import settings
from rest_framework.views import APIView, Response
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ActiveToolsList(APIView):
    """
    This class is used to retrieve all installed ACTIVE tools.
    It returns a dictionary which defines the association between tools and urls.
    """
    queryset = ActiveTools.objects.none()  # required for DjangoModelPermissions

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
