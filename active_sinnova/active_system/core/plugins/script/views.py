from django.http import HttpResponse, Http404

from rest_framework.response import Response
from core.views import EventView

from core.plugins.models import Script
from core.plugins.script.serializers import ScriptSerializer


class ScriptList(EventView): 
    """
    List all existing Script objects.
    """

    queryset = Script.objects.none()  # required for DjangoModelPermissions

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
        scripts = Script.objects.all()
        serializer = ScriptSerializer(scripts, many=True)
        return Response(serializer.data)


class ScriptDetail(EventView): 
    """
    Retrieve a script instance.
    """

    queryset = Script.objects.none()  # required for DjangoModelPermissions
 
    def get_object(self, pk):
        """
        Method used to retrieve an Script objects using its id.

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
        Method used to retrieve all data of a specific Script object, providing its id.
        Script data is returned in a serialized format.

        @param request: HttpRequest used to retrieve data of a specific Script object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Script object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Script object, error otherwise.
        @rtype: HttpResponse
        """
        script = self.get_object(pk)
        serializer = ScriptSerializer(script)
        return Response(serializer.data)
