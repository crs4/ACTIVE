"""
This module contains all class that will implement all methods required by the
REST API for DynamicTags objects.
With the provided class and methods it is possible to retrieve all stored
DynamicTag objects and invoke CRUD operations, providing a id when necessary.
"""

from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.tags.models import Tag
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.dynamic_tags.serializers import DynamicTagSerializer

from django.db.models import Q
import threading
import logging

# utilizzato per risolvere il problema dell'accesso concorrente agli item
edit_lock = threading.Lock()

# variable used for logging purposes
logger = logging.getLogger('active_log')

 
        
        

class DynamicTagList(EventView):
    """
    This class provides two methods, one for retrieving all available DynamicTags
    and another for creating a new DynamicTag.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, format=None):
        """
        Method used to retrieve all stored DynamicTags.
        These objects are serialized in a JSON format and then returned.

        @param request: HttpRequest use to retrieve all DynamicTags.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing all serialized DynamicTags.
        @rtype: HttpResponse
        """
        logger.debug('Requested all DynamicTag objects')
        tag = DynamicTag.objects.all()
        serializer = DynamicTagSerializer(tag, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method used to create a new DynamicTag object.
        The object data is provided in a serialized format.

        @param request: HttpRequest used to provide tag data.
        @type request: HttpRequest
        @param format: The format used for object serialization.
        @type format: string
        @return: HttpResponse containing the id of the new DynamicTag object, error otherwise.
        @rtype: HttpResponse
        """
        serializer = DynamicTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Created new DynamicTag object')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Error on creating a new DynamicTag object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DynamicTagDetail(EventView):
    """
    This class implements all methods necessary to handle
    an existing DynamicTag object providing its id.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        """
        Method used to retrieve an DynamicTag object by its id.

        @param pk: DynamicTag primary key.
        @type pk: int
        @return: Object containing the tag retrieved data, error otherwise.
        @rtype: DynamicTag
        """
        try:
            return DynamicTag.objects.get(pk = pk)
        except DynamicTag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all data about a specific DynamicTag object.
        Returned data is provided in a JSON serialized format.

        @param request: HttpRequest used to retrieve data of a DynamicTag object.
        @type request: HttpRequest
        @param pk: DynamicTag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        logger.debug('Requested details for DynamicTag object with id ' + str(pk))
        tag = self.get_object(pk)
        serializer = DynamicTagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Method used to update a DynamicTag object data, providing all
        fresh data in a serialized form.

        @param request: HttpRequest containing the updated DynamicTag field data.
        @type request: HttpRequest
        @param pk: DynamicTag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        with edit_lock:
            tag = self.get_object(pk)
            serializer = DynamicTagSerializer(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Updated data for DynamicTag object with id ' + str(pk))
                return Response(serializer.data)
            logger.error('Error on update of DynamicTag object with id ' + str(pk))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Method used to delete a DynamicTag object providing its id.

        @param request: HttpRequest used to delete a DynamicTag object.
        @type request: HttpRequest
        @param pk: DynamicTag primary key, used to retrieve object data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """
        logger.debug('Requested delete on DynamicTag object with id ' + str(pk))
        dtag = self.get_object(pk)
        dtag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        

class MergeUniformDynamicTag(EventView):
    """
    Class used to implement methods necessary to search all DynamicTags objects 
    filtering by the person id.
    """

    queryset = DynamicTag.objects.none()  # required for DjangoModelPermissions
    
    def __check_dtag_intersection(self, dtag1, dtag2):
        """
        Method used to check if there is a temporal overlapping between two 
        consecutive dynamic tags.
        The provided dynamic tags are ordered by start time.
        """
        if(dtag2.start < dtag1.start + dtag1.duration):
            if(dtag2.start + dtag2.duration < dtag1.start + dtag1.duration):
                return "total"
            else:
                return "partial"
        else:
            return None   
        
    
    def __mergedtags(self,item_id, entity_id, dtags):   
        joined_dtag = []
        if not len(dtags):  
            return None           
        ordered_dtags = sorted(dtags,key=lambda x: x.start, reverse=False)
        print "ordered_tags", ordered_dtags
        tag = Tag.objects.create(item_id = item_id, entity_id = entity_id, type = "face+speaker")        
        joined_dtag.append(DynamicTag.objects.create(tag = tag, start = ordered_dtags[0].start, duration = ordered_dtags[0].duration ))
        del ordered_dtags[0]
        for next_dtag in ordered_dtags:
            dtag_inter = self.__check_dtag_intersection(joined_dtag[-1],next_dtag)
            print dtag_inter
            if(dtag_inter == "partial"):
                start = joined_dtag[-1].start
                duration = next_dtag.start + next_dtag.duration - start
                #temp_inst = next_dtag.start + next_dtag.duration
                #next_dtag.start = joined_dtag[-1].start + joined_dtag[-1].duration
                #next_dtag.duration = temp_inst - next_dtag.start
                joined_dtag[-1].start = start
                joined_dtag[-1].duration = duration                
            elif dtag_inter is None:
                temp_dtag = DynamicTag.objects.create(tag = tag, start = next_dtag.start, duration = next_dtag.duration )
                joined_dtag.append(temp_dtag)
                
        for jdtag in joined_dtag:
            jdtag.save()
            
            
    def post(self, request, format=None):
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
        item_id = request.data['item_id']
        Tag.objects.filter(item__pk = item_id, type =  "face+speaker").delete()
        entities = Tag.objects.filter(item__pk = item_id).values("entity_id").distinct()
        for entity in entities:
            face_dtags = DynamicTag.objects.filter(tag__item__pk = item_id, tag__entity__pk = entity['entity_id'], tag__type="face")                   
            speaker_dtags = DynamicTag.objects.filter(tag__item__pk = item_id, tag__entity__pk = entity['entity_id'], tag__type="speaker")                   
            dtags = list(face_dtags) + list(speaker_dtags)

            self.__mergedtags(item_id, entity['entity_id'], dtags)
            
        return Response(status=status.HTTP_200_OK)

        
