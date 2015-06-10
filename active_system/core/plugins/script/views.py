from django.http import HttpResponse, Http404

from rest_framework.response import Response
from core.views import EventView

from core.plugins.models import Script
from core.plugins.script.serializers import ScriptSerializer
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ScriptList(EventView): 
    """
    This class implements the methods necessary to list all available Script objects
    and to create a new one providing the JSON serialized required data.
    """
    model = Script

    def get(self, request, format=None):
        """
        This method is used to retrieve all stored Script objects.
        Objects are returned in a serialized format, JSON by default.

        @param request: HttpRequest used to retrieve all stored Script objects.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing all serialized data.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored Script objects')
        scripts = Script.objects.all()
        serializer = ScriptSerializer(scripts, many=True)
        return Response(serializer.data)


class ScriptDetail(EventView): 
    """
    This class implements the methods necessary to retrieve a specific
    Script object providing its id.
    """
    model = Script

    def get_object(self, pk):
        """
        Method used to retrieve a Script object using its id.

        @param pk: Primary key used to retrieve a Script object.
        @type pk: int
        @returns: Script object containing retrieved data, otherwise HTTP error.
        @rtype: Script
        """
        try:
            return Script.objects.get(pk=pk)
        except Script.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve data of a specific Script object, providing its id.
        Script data is returned in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a specific Script object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Script object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Script object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested Script object ' + str(pk))
        script = self.get_object(pk)
        serializer = ScriptSerializer(script)
        return Response(serializer.data)