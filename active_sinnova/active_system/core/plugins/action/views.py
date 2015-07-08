"""
This module contains all classes necessary to define a REST API for Action objects.
The defined classes contains all necessary methods in order to retrieve all stored
video item objects and apply CRUD operations, providing an id if necessary.
"""

from django.http import HttpResponse, Http404

from core.plugins.models import Action
from core.plugins.action.serializers import ActionSerializer

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status


class ActionList(EventView): 
    """
    List all existing Actions or create/save a new one.
    """

    queryset = Action.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        This method will be converted in a HTTP GET API and it
        will allow to list all already stored Action objects in the database.

        @param request: HttpRequest used to retrieve all stored Action objects.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing all serialized data.
        @rtype: HttpResponse

        """
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        This method will be converted in a HTTP POST API and it
        will allow to save new Event objects in the database.

        @param request: HttpRequest containing all data for the new Action object.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing the id of the new object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionDetail(EventView):
    """
    Retrieve, update or delete a action instance.
    """

    queryset = Action.objects.none()  # required for DjangoModelPermissions    

    def get_object(self, pk):
        """
        Method used to obtain action data by its id.

        @param pk: Primary key used to retrieve a Action object.
        @type pk: int
        @returns: Action object containing retrieved data, otherwise HTTP error.
        @rtype: Action
        """
        try:
            return Action.objects.get(pk=pk)
        except Action.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to return serialized data of a action.

        @param request: HttpRequest used to retrieve data of a specific Action object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Action object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Action object, error otherwise.
        @rtype: HttpResponse
        """
        action = self.get_object(pk)
        serializer = ActionSerializer(action)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update action information providing
        serialized data.

        @param request: HttpRequest which provide all update data fields.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Action object to update.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the Action updated serialized data, error otherwise.
        @rtype: HttpResponse
        """
        action = self.get_object(pk)
        serializer = ActionSerializer(action, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete action information providing its ID.

        @param request: HttpRequest used to delete a specific Action object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Action object to delete.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of Action object deletion.
        @rtype: HttpResponse
        """
        action = self.get_object(pk)
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
