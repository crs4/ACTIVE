from django.http import HttpRequest
from rest_framework.request import Request

from core.tags.models import Tag
from core.tags.person.models import Person

from core.items.audio.models import AudioItem
from core.items.image.models import ImageItem
from core.items.video.models import VideoItem

from core.items.audio.serializers import AudioItemSerializer, AudioItemPagination
from core.items.image.serializers import ImageItemSerializer, ImageItemPagination
from core.items.video.serializers import VideoItemSerializer, VideoItemPagination

"""
class SearchItemByPersonName(EventView):
    ""
    Class used to implement methods necessary to search all Item objects
    associated to a specific person name.
    Moreover it is possibile to define which type of digital item it
    must be returned
    ""
    model = Item
"""

#def getItems("""self, request,""" type, person_name, format=None):
def getItems(type, person_name, format=None):
	"""
	Method used to retrieve all Item objects containing
	the occurrences of a specific person (if any).
	Returned data is provided in a JSON serialized format.

	@param request: HttpRequest used to retrieve data of Item objects.
	@type request: HttpRequest
	@param type: Type of the item that will be returned.
	@type type: string
	@param person_name: Person name and surname comma separated.
	@type person_name: string
	@param format: Format used for data serialization.
	@type format: string
	@return: HttpResponse containing all JSON serialized item objects.
	@rtype: HttpResponse
	"""
	#logger.debug('Searching all Item objects of type ' + type + ' associated to person ' + person_name)
	item_type = {'audio': [AudioItem, AudioItemSerializer, AudioItemPagination], 
		     'image': [ImageItem, ImageItemSerializer, ImageItemPagination],
		     'video': [VideoItem, VideoItemSerializer, VideoItemPagination]}
	if type not in item_type:
	    return Response(json.dumps([]))

	# find all people with the provided name
	person_name = person_name.split(',')

	people = Person.objects.all()
	people = people.filter(first_name = person_name[0])
	if len(person_name) > 0:
	    people = people.filter(last_name = person_name[1])

	# for each person search the tags where he appears
	item_ids = []
	for person in people:
	    tags = Tag.objects.filter(entity__id = person.pk)
	    print "Retrieved " + len(tags) + ' tags for person ' + person.pk
	    
	    items_ids += [ tag.item.pk for tag in tags if tag.item.type == item_type and tag.type == 'person']

	print 'Items found ' + item_ids

	items = item_type[type][0].objects.filter(pk in sets.Set(item_ids))
	paginator = item_type[type][2]()
        request = Request(HttpRequest()) ############################
	result = paginator.paginate_queryset(items, request)
	serializer = item_type[type][1](items, many=True)
	return paginator.get_paginated_response(serializer.data)
