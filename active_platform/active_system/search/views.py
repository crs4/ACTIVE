# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import json
import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from search.es_manager import ESManager
from core.views import EventView
from core.tags.person.models import Person
from core.tags.person.serializers import PersonSerializer, PersonPagination
from core.tags.keywords.models import Keyword
from core.tags.keywords.serializers import KeywordSerializer
from core.items.models import Item
from core.items.audio.models import AudioItem
from core.items.image.models import ImageItem
from core.items.video.models import VideoItem
from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination
from core.tags.models import Tag, Entity
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.dynamic_tags.serializers import DynamicTagSerializer
from core.tags.serializers import TagSerializer

# variable used for logging purposes
logger = logging.getLogger('active_log')


class ESExists(CreateAPIView):
	queryset = User.objects.none()

	@csrf_exempt	
	def post(self, request, format=None):
		esm = ESManager()
		res = esm.exists(json.loads(request.body))
		if 'error' in res:
			return JsonResponse(status=500, data=res, reason='es - exists failure')
		return JsonResponse(status=200, data=res, reason='es - exists')


class ESCreate(CreateAPIView):
	queryset = User.objects.none()

	@csrf_exempt	
	def post(self, request, format=None):
		esm = ESManager()
		res = esm.create(json.loads(request.body))
		if 'error' in res:
			return JsonResponse(status=500, data=res, reason='es - create failure')
		return JsonResponse(status=201, data=res, reason='es - create')


class ESUpdate(UpdateAPIView):
	queryset = User.objects.none()

	@csrf_exempt	
	def put(self, request, format=None):
		esm = ESManager()
		res = esm.update(json.loads(request.body))
		if 'error' in res:
			return JsonResponse(status=500, data=res, reason='es - update failure')
		return JsonResponse(status=200, data=res, reason='es - update')


class ESDelete(DestroyAPIView):
	queryset = User.objects.none()

	@csrf_exempt	
	def delete(self, request, format=None):
		esm = ESManager()
		res = esm.delete(json.loads(request.body))
		if 'error' in res:
			return JsonResponse(status=500, data=res, reason='es - delete failure')
		return JsonResponse(status=200, data=res, reason='es - delete')
		

class ESSearch(CreateAPIView):
	queryset = User.objects.none()

	@csrf_exempt	
	def post(self, request, format=None):
		esm = ESManager()
		res = esm.search(json.loads(request.body))
		if 'error' in res:
			return JsonResponse(status=500, data=res, reason='es - search failure')
		return JsonResponse(status=200, data=res, reason='es - search')


def find_person(first_name, last_name):
    """
    Check if the user already exists based on the first and last name.
    A boolean value is returned based on the size of the result set.

    @param first_name: First name of the person searched
    @type first_name: string
    @param last_name: Last name of the persona searched
    @type last_name: string
    @return: The result of the uniqueness search
    @rtype: boolean
    """
    #res = Person.objects.filter(first_name__iexact = first_name).filter(last_name__iexact= last_name)
    res = Person.objects.filter(first_name__iexact = first_name).filter(last_name__icontains= last_name)
    if res or len(res):
        logger.debug('Retrieved Person objects ' + str(len(res)))
        return res

    logger.debug('No Person object found with name ' + first_name + ' ' + last_name)
    return None


class PeopleSearch(EventView):
    """
    Class used to implement the method necessary to retrieve an existing person from
    its full name.
    """
    queryset = Person.objects.none()  # required for DjangoModelPermissions

    def get(self, request, first_name, last_name, format=None):
        """
        Method used to retrieve a Person object providing the full name of a person.
        It returns None if there is no person associated to this name.

        @param request: HttpRequest used to obtain the Person object
        @type request: HttpRequest
        @param first_name: First name of the searched person.
        @type: string
        @param last_name: Last name of the searched person.
        @type: string
        @param format: Format of the serialized Person object image
        @type format: string
        @return: HttpResponse containing the retrieved Person object
        @rtype: HttpResponse
        """
        logger.debug('Requested Person objects with name ' + first_name + ' ' + last_name)
        res = find_person(first_name, last_name)

        if res is None:
            return Response([], status=status.HTTP_200_OK)

        serializer = PersonSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonSearch(EventView):
    """
    Class used to implement the method necessary to retrieve an existing person from
    its full name.
    """
    queryset = Person.objects.none()  # required for DjangoModelPermissions

    def get(self, request, first_name, last_name, format=None):
        """
        Method used to retrieve a Person object providing the full name of a person.
        It returns None if there is no person associated to this name.

        @param request: HttpRequest used to obtain the Person object
        @type request: HttpRequest
        @param first_name: First name of the searched person.
        @type: string
        @param last_name: Last name of the searched person.
        @type: string
        @param format: Format of the serialized Person object image
        @type format: string
        @return: HttpResponse containing the retrieved Person object
        @rtype: HttpResponse
        """
        logger.debug('Requested Person object with name ' + first_name + ' ' + last_name)
        res = find_person(first_name, last_name)

        if res is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(res[0])
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeywordFind(EventView):
    """
    This class defines all methods necessary to find a Keyword object
    providing its character sequence.
    This approach is useful in order to create the minimum number of
    keyword stored in the db.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

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
        logger.debug('Searching a Keyword object with value ' + value)
        try:
            k = Keyword.objects.filter(description = value)
            if k and len(k) > 0:
                logger.debug('Find Keyword object ' + str(k[0].pk) + ' for value ' + value)
                serializer = KeywordSerializer(k[0])
                return Response(serializer.data)

            logger.error('No Keyword object found for value ' + value)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Http404


class KeywordSearch(EventView):
    """
    This class provides the methods necessary to search a specific keywords (if any)
    associated to a generic digital item.
    """
    queryset = Keyword.objects.none()  # required for DjangoModelPermissions

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
        logger.debug('Searching all Item objects associated to keyword list ' + keyword_list)
        # create a map to specific item object handlers
        item_map = { "audio" : [AudioItem, AudioItemSerializer, AudioItemPagination],
                     "image" : [ImageItem, ImageItemSerializer, ImageItemPagination],
                     "video" : [VideoItem, VideoItemSerializer, VideoItemPagination] }

        # check if the item type is supported
        if item_type not in item_map:
            logger.error('Provided item type for search is not supported - ' + item_type)
            return Response({'error' : 'The specified item type is not supported.'}, status=status.HTTP_400_BAD_REQUEST)

        # all items are returned if there is no keyword
        if len(keyword_list) == 0:
            logger.debug('Returned all Item objects of type ' + item_type)
            return Response(ItemSerializer(Item.user_objects.by_user(request.user).filter(type = item_type), many=True).data)

        item_list = []
        # retrieve the provided keywords (if they exist)
        keyword_list = set(keyword_list.strip().lower().replace(' ', '_').split(','))
        for k in keyword_list:
            keywords = Keyword.objects.filter(description__icontains = k)

            # retrieve all tags associated to each keyword
            temp = []
            for k2 in keywords:
                tags = Tag.user_objects.by_user(request.user).filter(entity__id = k2.id)
                temp += ([t.item.id for t in tags])
            item_list.append(temp)
        
        # intersect the list of item ids
        ids = set(item_list[0])
        for i in range(1, len(item_list)):
            ids = ids.intersection(item_list[i])

        # return the retrieved list of specific digital items
        logger.debug('Returning all Item objects found for keyword list ' + str(keyword_list))
        items = item_map[item_type][0].user_objects.by_user(request.user).filter(item_ptr_id__in = ids)
        paginator = item_map[item_type][2]()
        result = paginator.paginate_queryset(items, request)
        serializer = item_map[item_type][1](result, many=True)
        return paginator.get_paginated_response(serializer.data)


class SearchDynamicTagItem(EventView):
    """
    Class used to implement methods necessary to search all DynamicTags objects 
    filtering by the item id.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all DynamicTag objects containing
        the occurrences in a specific digital item (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a DynamicTag object.
        @type request: HttpRequest
        @param pk: Item object primary key, used to retrieve tag data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested all DynamicTag objects associated to Item object with id ' + str(pk))
        dtag = DynamicTag.objects.filter(tag__item__id = pk)
        serializer = DynamicTagSerializer(dtag, many=True)
        return Response(serializer.data)


class SearchDynamicTagPerson(EventView):
    """
    Class used to implement methods necessary to search all DynamicTags objects 
    filtering by the person id.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all DynamicTag objects containing
        the occurrences of a specific person (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a DynamicTag object.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested all DynamicTag objects associated to Entity object with id ' + str(pk))
        dtag = DynamicTag.objects.filter(tag__entity__id = pk)
        serializer = DynamicTagSerializer(dtag, many=True)
        return Response(serializer.data)
        
        

class SearchDynamicTagByTag(EventView):
    """
    Class used to implement methods necessary to search all DynamicTags objects 
    filtering by the person id.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all DynamicTag objects associated
        with a given Tag (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a DynamicTag object.
        @type request: HttpRequest
        @param pk: Tag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested all DynamicTag objects associated to Entity object with id ' + str(pk))
        dtag = DynamicTag.objects.filter(tag__id = pk)
        serializer = DynamicTagSerializer(dtag, many=True)
        return Response(serializer.data)


class SearchTagItem(EventView):
    """
    Class used to implement methods necessary to search all Tags
    objects associated to a specific digital item.
    """
    queryset = Tag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all Tag objects containing
        the occurrences in a specific digital item (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Item object primary key, used to retrieve tag data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Searching all Tag objects associated to Item object with id ' + str(pk))
        tag = Tag.user_objects.by_user(request.user).filter(item__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)


class SearchTagPerson(EventView):
    """
    Class used to implement methods necessary to search all Tags objects
    associated to a specific person.
    """
    queryset = Tag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all Tag objects containing
        the occurrences of a specific person (if any).
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Person primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Searching all Tag objects associated to Entity object with id ' + str(pk))
        tag = Tag.user_objects.by_user(request.user).filter(entity__id = pk)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
