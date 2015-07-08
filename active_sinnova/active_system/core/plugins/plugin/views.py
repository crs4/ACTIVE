"""
This module contains all classes needed to define a REST API for Plugin objects.
The classes and methods defined here are used to retrieve all stored Plugin objects
and invoke CRUD operation, providing an id if requested.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response

from core.plugins.models import Plugin
from core.plugins.plugin.serializers import PluginSerializer


class PluginList(EventView): 
    """
    List all existing Plugin objects.
    """

    queryset = Plugin.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        This method is used to retrieve all stored Plugin objects.
        Retrieved data is returned in a serialized format.

        @param request: HttpRequest used to retrieve Plugin objects data.
        @type request: HttpRequest
        @param format: Format used to serialize objects data.
        @type format: string
        @result: HttpResponse containing all serialized objects data.
        @rtype: HttpResponse
        """
        plugins = Plugin.objects.all()
        serializer = PluginSerializer(plugins, many=True)
        return Response(serializer.data)


class PluginDetail(EventView): 
    """
    Retrieve a plugin instance.
    """

    queryset = Plugin.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        """
        Method used to obtain a specific Plugin object by its id.

        @param pk: Primary key used to retrieve a Plugin.
        @type pk: int
        @result: Plugin object retrieved, error if it isn't available.
        @rtype: Plugin
        """
        try:
            return Plugin.objects.get(pk=pk)
        except Plugin.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to return serialized data of a Plugin.

        @param request: HttpRequest used to retrieve serialized Plugin object data.
        @type request: HttpRequest
        @param pk: Plugin object primary key.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @returns: HttpResponse containing the Plugin object serialized data.
        @rtype: HttpResponse
        """
        plugin = self.get_object(pk)
        serializer = PluginSerializer(plugin)
        return Response(serializer.data)
