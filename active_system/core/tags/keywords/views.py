"""
This module contains all class that will implement methods required by the
REST API for Keyword object data.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.tags.keywords.models import Keyword
from core.tags.keywords.serializers import KeywordSerializer

from core.tags.models import Tag
from core.items.models import Item
from core.items.serializers import ItemSerializer

from core.items.audio.models import AudioItem
from core.items.audio.serializers import AudioItemSerializer

from core.items.image.models import ImageItem
from core.items.image.serializers import ImageItemSerializer

from core.items.video.models import VideoItem
from core.items.video.serializers import VideoItemSerializer


# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock()


class KeywordList(EventView):
    """
    This class provides the methods necessary to list all available
    Keyword objects and to create and store a new one, providing necessary data.
    """

    def get(self, request, format=None):
        """
        Method used to retrieve all stored Keyword objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.@rtype: HttpResponse
        """
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new Keyword object.
        If the provided keyword already exists, the existing one is returned.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide keywords data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new Keyword object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = KeywordSerializer(data=request.data)

        if serializer.is_valid() :
            # create and store a new keyword
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif len(Keyword.objects.filter(description__iexact = serializer.data['description'])) :
            # return an already existing
            keywords = Keyword.objects.get(description__iexact = serializer.data['description'])
            serializer = KeywordSerializer(keywords)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeywordDetail(EventView):
    """
    Retrieve, update or delete a Keyword instance.
    """

    def get_object(self, pk):
        """
        Method used to retrieve a Keyword object by its id.

        @param pk: Keyword object primary key.
        @type pk: int
        @return: Object containing the keywords retrieved data, error otherwise.
        @rtype: Keyword
        """
        try:
            return Keyword.objects.get(entity_ptr_id = pk)
        except Keyword.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific Keyword object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a Keyword object.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        keyword = self.get_object(pk)
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a Keyword object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated Keyword field data.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        with edit_lock:
            keyword = self.get_object(pk)
            serializer = KeywordSerializer(keyword, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a Keyword object providing its id.

        @param request: HttpRequest used to delete a Keyword object.
        @type request: HttpRequest
        @param pk: Keyword primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        keyword = self.get_object(pk)
        keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class KeywordFind(EventView):
    """
    This class defines all methods necessary to find a keyword object
    providing its character sequence.
    This approach is useful in order to create the minimum number of
    keyword stored in the db.
    """

    def get(self, request, value, format=None):
        """
        Method used to retrieve an existing Keyword object,
        providing its character value.
        The object is serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword.
        @type request: HttpRequest
        @param value: The string associated to a keyword.
        @type value: string
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.
        @rtype: HttpResponse
        """
        try:
            k = Keyword.objects.filter(description = value)
            if k and len(k) > 0:
                serializer = KeywordSerializer(k[0])
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Http404

# TODO da spostare in modulo distinto e allo stesso livello di core date le dipendenze?
class KeywordSearch(EventView):
    """
    This class provides the methods necessary to search a specific keywords (if any)
    associated to a generic digital item.
    """

    def get(self, request, item_type, keyword_list,  format=None):
        """
        Method used to retrieve all stored Keyword objects.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all Keyword.
        @type request: HttpRequest
        @param item_type: The type of digital item searched.
        @type item_type: string
        @param keyword_list: The keywords that will be searched in the selected digital items.
        @type keyword_list: List of strings
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized Keyword.
        @rtype: HttpResponse
        """
        # create a map to specific item object handlers
        item_map = { "audio" : [AudioItem, AudioItemSerializer],
                     "image" : [ImageItem, ImageItemSerializer],
                     "video" : [VideoItem, VideoItemSerializer] }

        # check if the item type is supported
        if item_type not in item_map:
            return Response({'error' : 'The specified item type is not supported.'}, status=status.HTTP_400_BAD_REQUEST)

        # all items are returned if there is no keyword
        if len(keyword_list) == 0:
            return Response(ItemSerializer(Item.objects.filter(type = item_type), many=True).data)

        item_list = []
        # retrieve the provided keywords (if they exist)
        keyword_list = set(keyword_list.strip().lower().replace(' ', '_').split(','))
        for k in keyword_list:
            keywords = Keyword.objects.filter(description__icontains = k)

            # retrieve all tags associated to each keyword
            temp = []
            for k2 in keywords:
                tags = Tag.objects.filter(entity__id = k2.id)
                temp += ([t.item.id for t in tags])
            item_list.append(temp)

        # intersect the list of item ids
        ids = set(item_list[0])
        for i in range(1, len(item_list)):
            ids = ids.intersection(item_list[i])

        # return the retrieved list of specific digital items
        items = item_map[item_type][0].objects.filter(item_ptr_id__in = ids)
        serializer = item_map[item_type][1](items, many=True)
        return Response(serializer.data)