"""
This module implements the views functions necessary to provide a REST API for the Training Set Manager.
It is possible to edit all data related to EntityModel objects and Instance objects.
"""

from django.http import Http404, HttpResponse
from django.shortcuts import render

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from tools.training_set_manager.models import EntityModel, Instance
from tools.training_set_manager.serializers import EntityModelSerializer, InstanceSerializer
from tools.training_set_manager.serializers import EntityModelPagination, InstancePagination

import threading

# utilizzato per risolvere il problema dell'accesso concorrente agli item
edit_lock = threading.Lock()



def index(request):
    """
    View used to return the template associated to the training set manager.
    
    @param request: The HTTP request used to retrieve the TrainingSetManager interface
    @type request: HttpRequest
    @return: The HTTP response containing the page that will be shown
    @rtype: HttpResponse
    """
    return render(request, "model_manager_index.html")


class EntityModelList(EventView):
    """
    Class used to retrieve all Entity models and create a new one.
    """
    queryset = EntityModel.objects.none()

    def get(self, request, format=None):
        """
        Method used to retrieve all stored EntityModel objects.
        Objects are returned in a serialized way.

        @param request: The HTTP request used to retrieve all EntityModel objects.
        @type request: HttpRequest
        @return: The HttpResponse containing all requested EntityModel objects.
        @rtype: HttpResponse
        """
        type = request.query_params.get('type', None)
        name = request.query_params.get('q', None)

        models = EntityModel.objects.all()
        if type is not None:
            models = models.filter(type=type)
        if name is not None:
            models = models.filter(name__icontains=name)
        
        paginator = EntityModelPagination()
        result = paginator.paginate_queryset(models, request)
        serializer = EntityModelSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create and save a new EntityModel object.
        The new object is returned in a serialized way.

        @param request: The HTTP request used to provide the EntityModel data.
        @type request: HttpRequest
        @return: A HTTP response containing the new EntityModel object seialized in a JSON format.
        @rtype: HttpResponse
        """
        serializer = EntityModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EntityModelDetail(EventView):
    """
    This class implement all methods necessary to retrive, edit
    or delete a EntityModel object.
    """
    queryset = EntityModel.objects.none()

    def __get_object(self, pk):
        """
        Method used to retrieve a specific EntityModel object.

        @param pk: The id of a EntityModel object.
        @type pk: int
        @return: The requested EntityModel object.
        @rtype: EntityModel object
        """
        try:
            return EntityModel.objects.get(pk=pk)
        except EntityModel.DoesNotExist:
            raise Http404
    

    def get(self, request, pk, format=None):
        """
        Method used to retrieve a specific EntityModel object.

        @param request: The HTTP request used to retrieve a EntityModel object
        @type request: HttpRequest
        @param pk: The id of the requested EntityModel object
        @type pk: int
        @return: The HTTP response containing the requested EntityModel object
        @rtype: HttpResponse
        """
        instance = self.__get_object(pk)
        serializer = EntityModelSerializer(instance)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        """
        Method used to edit a specific EntityModel object.

        @param request: The HTTP request used to update a specific EntityModel object
        @type request: HttpRequest
        @param pk: The id of the EntityModel object that will be updated
        @type pk: int
        @return: The HTTP response containing the update EntityModel object
        @rtype: HttpResponse
        """
        with edit_lock:
            model = self.__get_object(pk)
            serializer = EntityModelSerializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a specific EntityModel object.

        @param request: The HTTP request used to delete a specific EntityModel object
        @type request: HttpRequest
        @param pk: The id of the EntityModel object that will be deleted
        @type pk: int
        @return: The HTTP response containing the result fo the EntityModel deletion
        @rtype: HttpResponse
        """
        model = self.__get_object(pk)
        instances = Instance.objects.filter(entity_model=model)
        for i in instances:
            i.entity_model = None
            i.save()
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstanceList(EventView):
    """
    View used to retrieve all stored Instances and create a new one.
    Data is provided in a JSON serialized format.
    """
    queryset = Instance.objects.none()

    def get(self, request, format=None):
        """
        Method used to retrieve all stored Instance objects.
        Objects are returned in a serialized way. 

        @param request: The HttpRequest used to retrieve all stored Instance objects.
        @type request: HttpRequest
        @return: The HTTP response containing all stored Instance objects
        @rtype: HttpResponse
        """
        used    = request.query_params.get('used', None)
        type = request.query_params.get('type', None)
        
        instances = None
        if used is not None and used == 'false':
            instances = Instance.objects.filter(entity_model=None)
            if type is not None:
                instances = instances.filter(type = type)
        else:
            instances = Instance.objects.all()
            
        paginator = InstancePagination()
        result = paginator.paginate_queryset(instances, request)
        serializer = InstanceSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create and save a new Instance object.
        The new object created is returned in a serialized way.

        @param request: The HTTP request containing the data for a new Instance object
        @type request: HttpRequest
        @return: The HTTP response containing the new Instance object
        @rtype: HttpResponse
        """
        serializer = InstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstanceDetail(EventView):
    """
    View used to retrieve or delete a specific Instance object.
    Data is provided in a JSON serialized format.
    """
    queryset = Instance.objects.none()

    def __get_object(self, pk):
        """
        Method used to retrieve a specific EntityModel object.

        @param pk: The id of the requested Instance object
        @type pk: int
        @return: The requested Instance object
        @rtype: Instance object
        """
        try:
            return Instance.objects.get(pk=pk)
        except Instance.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve a specific Instance object by its id.

        @param request: The HTTP request used to retrieve a specific Instance object
        @type request: HttpRequest
        @param pk: The id of the requested Instance object
        @type pk: int
        @return: The HTTP response containing the requested Instance object 
        @rtype: HttpResponse
        """
        instance = self.__get_object(pk)
        serializer = InstanceSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to edit a specific Instance object.

        @param request: The HTTP request used to update a specific Instance object
        @type request: HttpRequest
        @param pk: The id of the Instance object that will be updated
        @type pk: int
        @return: The HTTP response containing the update Instance object
        @rtype: HttpResponse
        """
        with edit_lock:
            instance = self.__get_object(pk)
            serializer = InstanceSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to remove a specific Instance object.
        It is possible to delete all data associated to a Instance
        object or to remove its association to an EntityModel object.

        @param request: The HTTP requested used to delete a Instance object 
        @type request: HttpRequest
        @param pk: The id of the Instance object that will be deleted
        @type pk: int
        @return: The HTTP response containing the deletion result
        @rtype: HttpResponse
        """
        instance = self.__get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstanceFile(EventView):
    """
    This class has been defined in order to provide an endpoint which could be used
    to download all available instance files (actually thumbanail or feature) by their types.
    """
    queryset = Instance.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve the original file created for a Instance objects

        @param request: HttpRequest used to retrieve the resource associated to a specific Item.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Instance object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the retrieved resource, error otherwise.
        @rtype: HttpResponse
        """
        try:
            instance = Instance.objects.get(pk=pk)
            type = request.GET.get('type', 'thumb')
           
            # return the requested thumbnail
            if type == 'thumb':
                response = HttpResponse(instance.thumbnail, content_type='image/jpeg')
                return response
    
            response = HttpResponse(instance.features, content_type='application/octect-stream')
            response['Content-Disposition'] = 'attachment; filename="' + instance.features.name + '"'
            return response
        except Instance.DoesNotExist:
            raise Http404


class SearchInstanceByModel(EventView):
    """
    View used to retrieve all stored Instances and create a new one.
    Data is provided in a JSON serialized format.
    """
    queryset = Instance.objects.none()

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all stored Instance objects associated to a EntityModel.
        Objects are returned in a serialized way.

        @param request: The HttpRequest used to retrieve all stored Instance objects.
        @type request: HttpRequest
        @param pk: The id of the Entitymodel used 
        @type pk: int
        @return: The HTTP response containing all stored Instance objects
        @rtype: HttpResponse
        """
        instances = Instance.objects.filter(entity_model=pk)
        paginator = InstancePagination()
        result = paginator.paginate_queryset(instances, request)
        serializer = InstanceSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
