"""
This module is used to define a REST API for generic items.
It is possible to create a new Item object, list all existing
and stored Item objects and handle a specific Item providing its id.
"""

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.models import Item
from core.items.serializers import ItemSerializer, ItemPagination
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class ItemList(EventView):
    """
    This class implements the views necessary to list
    all stored Item objects and create a new one, providing necessary
    data in a serialized format.
    """
    model = Item

    def get(self, request, format=None):
        """
        Method used to retrieve all data about stored Item objects.
        All data is returned in a JSON format (serialized).

        @param request: HttpRequest object used to retrieve all Item objects.
        @type request: HttpRequest
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all requested Item objects.
        @rtype: HttpResponse
        """
        logger.debug("Requested all stored Item objects")
        items = Item.objects.all()
        paginator = ItemPagination()
        result = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


class ItemDetail(EventView):
    """
    This class implement all methods necessary to retrieve, update or
    delete a Item object providing its id.
    """
    model = Item

    def get_object(self, pk):
        """
        Method used retrieve a Item object from its id.

        @param pk: Item primary key used to retrieve the object.
        @type pk: int
        @return: Item object corresponding to the provided id.
        @rtype: Item
        """
        try:
            return Item.objects.get(pk = pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve data about a specific Item.

        @param request: HttpRequest object used to retrieve an Item.
        @type request: HttpRequest
        @param pk: Item id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the requested item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        logger.debug('Requested Item object ' + str(pk))
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update information about a specific Item object
        providing the JSON serialized updated data.

        @param request: HttpRequest object containing the updated Item fields.
        @type request: HttpRequest
        @param pk: Item id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the uploaded item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        logger.debug('Requested edit on Item object ' + str(pk))
        with edit_lock:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Item object ' + str(pk) + ' successfully edited')
                return Response(serializer.data)

            logger.error('Provided data not valid for Item object ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete all data associated to a specific Item object
        providing its id.

        @param request: HttpRequest object used to delete a Item object.
        @type request: HttpRequest
        @param pk: Item's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of the Item object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on Item object ' + str(pk))
        item = self.get_object(pk)
        item.delete()
        logger.debug('Item object ' + str(pk) + ' successfully deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemFile(EventView):
    """
    This class has been defined in order to provide an endpoint which could be used
    to download the resource associated to a Item object, independently from its content type.
    The download could be done using a partial content response (if requested).
    It is possible to download different version of resource for a specific Item object.
    """
    model = Item

    def get(self, request, pk, format=None):
        """
        Method used to retrieve the resource associated to a Item object.
        It is possible to select the original file, the preview or its thumbnail image.

        @param request: HttpRequest used to retrieve the resource associated to a specific Item.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Item object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the retrieved resource, error otherwise.
        @rtype: HttpResponse
        """

        try:
            item = Item.objects.get(pk=pk)
            type = request.GET.get('type', 'original')

            # return the original resource file
            if type == 'original':
                logger.debug('Requested original resource for Item object ' + str(pk))
                response = HttpResponse(FileWrapper(item.file), content_type = item.mime_type)
                response['Content-Disposition'] = 'attachment; filename="' + item.filename + '"'
                return response

            # return the resource thumbnail image
            if type == 'thumb':
                logger.debug('Requested thumbnail resource for Item object ' + str(pk))
                response = HttpResponse(item.thumb, content_type = 'image/jpeg')
                return response

            # return the preview resource file
            if type == 'preview':
                logger.debug('Requested preview resource for Item object ' + str(pk))
                # detect what kind of request has been
                # if the entire item is requested
                if 'HTTP_RANGE' not in request.META :
                    response = HttpResponse(FileWrapper(item.preview))
                    response['Content-Disposition'] = 'filename="' + item.filename + '"'
                    response['Accept-Ranges'] = "bytes"                    
                    response['Content-Type'] = item.mime_type #'video/mp4'
                    response['Content-Length'] = item.preview.size
                    return response
                # otherwise the requested amount of bytes is returned
                else:
                    logger.debug('Partial content request for Item object preview ' + str(pk))
                    range = request.META['HTTP_RANGE']
                    start = int(range.split('=')[1].split('-')[0])
                    end   = item.preview.size
                    if len(range.split('=')[1].split('-')[1]) > 0:
                        end = int(range.split('=')[1].split('-')[1])

                    response = HttpResponse(status=206)
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Type'] = item.mime_type#'video/mp4'
                    response['Content-Range'] = "bytes %d-%d/%d" %(start , end-1, item.preview.size) # the range of data returned
                    response['Content-Length'] = end - start # amount of data returned
                    
                    if(start > item.preview.size or end > item.preview.size ):
                        return Response(status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
                        
                    # extract and return the amount of requested bytes
                    f = open(item.preview.path, 'rb')
                    f.seek(start)
                    response.content = f.read(end - start)
                    f.close()
              
                    return response

        except Item.DoesNotExist:
            raise Http404
