"""
This module contains all classes necessary to define a REST API for Action objects.
The defined classes contains the methods necessary to retrieve all stored
Action objects and apply CRUD operations, providing an id if necessary.
"""

from django.http import HttpResponse, Http404

from core.plugins.models import Action
from core.plugins.action.serializers import ActionSerializer

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ActionList(EventView): 
    """
    List all existing Action objects or create/save a new one.
    """
    model = Action

    def get(self, request, format=None):
        """
        This method will be converted in a HTTP GET API and it
        will allow to list all stored Action objects in the database.

        @param request: HttpRequest used to retrieve all stored Action objects.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing all serialized data.
        @rtype: HttpResponse
        """
        logger.debug('Requested all stored Action objects')
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        This method will be converted in a HTTP POST API and it
        will allow to save a new Action object in the database.

        @param request: HttpRequest containing all data for the new Action object.
        @type request: HttpRequest
        @param format: The format used to serialize objects data.
        @type format: string
        @return: HttpResponse containing the new Action object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Creating a new Action object')
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('New Action object saved - ' + str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Provided data not valid for Action object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionDetail(EventView):
    """
    This class implements all methods necessary to retrieve, update or
    delete a Action object providing its id and additional JSON serialized data.
    """
    model = Action

    def get_object(self, pk):
        """
        Method used to obtain a Action object providing its id.

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
        Method used to return serialized data of a Action object providing its id.

        @param request: HttpRequest used to retrieve data of a specific Action object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a Action object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the serialized data of a Action object, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested Action object ' + str(pk))
        action = self.get_object(pk)
        serializer = ActionSerializer(action)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update information of a specific Action object, providing
        its id and JSON serialized updated data.

        @param request: HttpRequest which provide all update data fields.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Action object to update.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the Action updated serialized data, error otherwise.
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on Action object ' + str(pk))
        action = self.get_object(pk)
        serializer = ActionSerializer(action, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Action object ' + str(pk) + ' successfully edited')
            return Response(serializer.data)

        logger.error('Provided data not valid for Action object ' + str(pk))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a specific Action object providing its id.

        @param request: HttpRequest used to delete a specific Action object.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Action object to delete.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of Action object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on Action object ' + str(pk))
        action = self.get_object(pk)
        action.delete()
        logger.debug('Action object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
