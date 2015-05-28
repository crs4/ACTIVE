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

# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()



class ItemList(EventView):
    """
    This class implements the views necessary to list
    all stored digital items in a serialized format.
    """

    def get(self, request, format=None):
        """
        Method used to retrieve all data about stored items.
        All data is returned in a JSON format (serialized).

        @param request: HttpRequest object used to retrieve all Items.
        @type request: HttpRequest
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all requested items data.
        @rtype: HttpResponse
        """
        items = Item.objects.all()
        paginator = ItemPagination()
        result = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


class ItemDetail(EventView):
    """
    Retrieve, update or delete a Item instance.
    """

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
        @return: HttpResponse containing the requested audio item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update the Item information providing
        serialized fresh data.

        @param request: HttpRequest object contining the updated AudioItem fields.
        @type request: HttpRequest
        @param pk: Item id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the uploaded item data, error if it doesn't exists.
        @rtype: HttpResponse
        """
        with edit_lock:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print serializer.data, '\n\n\n'
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete user information providing his ID.

        @param request: HttpRequest object used to delete a AudioItem object.
        @type request: HttpRequest
        @param pk: Audio Item's id.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of the item deletion.
        @rtype: HttpResponse
        """
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemFile(EventView):
    """
    This class has been defined in order to provide an endpoint which could be used
    to download a digital item, independently from its type.
    The download could be done using a partial content response.
    It is possible to download a digital item or its thumbnail.
    """
    def get(self, request, pk, format=None):
        """
        Method used to retrieve the original file created for a digital item or its thumbnail

        @param request: HttpRequest used to retrieve the resource associated to a specific Item.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve the Item object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the retrieved resource, error otherwise.
        @rtype: HttpResponse
        """
        # TODO errore 416 se il range richiesto non e' valido

        try:
            item = Item.objects.get(pk=pk)
            type = request.GET.get('type', 'original')
            
            print pk, item, type

            # return the requested thumbnail
            if type == 'thumb':
                response = HttpResponse(item.thumb, content_type = 'image/jpeg')
                return response
            # return the original resource file
            if type == 'original':
                response = HttpResponse(item.file, content_type = item.mime_type)
                return response
            # return the preview resource file
            if type == 'preview':
                # detect what kind of request has been
                # if the entire item is requested
                if 'HTTP_RANGE' not in request.META :
                    response = HttpResponse(FileWrapper(item.preview))
                    response['Content-Disposition'] = 'attachment; filename="' + item.file.name + '"'
                    response['Accept-Ranges'] = "bytes"
                    response['Content-Type'] = 'video/mp4'
                    response['Content-Length'] = item.preview.size
                    return response
                # otherwise the requested amount of bytes is returned
                else:
                    range = request.META['HTTP_RANGE']
                    start = int(range.split('=')[1].split('-')[0])
                    end   = item.preview.size
                    if(len(range.split('=')[1].split('-')[1]) > 0):
                        end = int(range.split('=')[1].split('-')[1])

                    response = HttpResponse(status=206)
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Type'] = 'video/mp4'
                    response['Content-Range'] = "bytes %d-%d/%d" %(start , end-1, item.preview.size) # the range of data returned
                    response['Content-Length'] = end - start # amount of data returned
                    
                    # extract and return the amount of requested bytes
                    f = open(item.preview.path, 'rb')
                    f.seek(start)
                    response.content = f.read(end - start)
                    f.close()

                    return response
        except Item.DoesNotExist:
            raise Http404
        except Exception as e:
            print e
