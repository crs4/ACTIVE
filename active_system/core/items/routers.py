from django.http import HttpResponse, Http404, HttpRequest
from core.items.models import Item

from core.items.video.views import VideoItemList, VideoItemDetail, VideoItemFile
from core.items.audio.views import AudioItemList, AudioItemDetail, AudioItemFile 
from core.items.image.views import ImageItemList, ImageItemDetail, ImageItemFile

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

import json


"""
This file contains all methods necessary to invoke the correct view
for each digital item. The decision is based on the file type.

There are two view routers, one for CRUD operations while the other for
list all items togheter and for create a new item.
"""


@csrf_exempt
@api_view(('GET','POST'))
def routerList(request):
	"""
	Function used to invoke the correct view based on the
	type of the multimedia file.
	It is possible to filter stored items by their file type.

	@param request: The HttpRequest used to retrieve items data.
	@type request: HttpRequest
	@param items_type: A field used to retrieve only specific types of digital items
	@type items_type: string
	@return: The HttpResponse object containing all retrieved items data.
	@rtype: HttpResponse
	"""
	# dictionary used to invoke the correct set of views
	mapping = {'video': VideoItemList.as_view(),
                   'image': ImageItemList.as_view(),
                   'audio': AudioItemList.as_view()}

	# obtain the filter type
	items_type = request.GET.get('type', 'ALL')

	# handle the upload of a new item
	if(request.FILES):
		type = request.FILES['file'].content_type.split('/')[0]
                print(type)
		if type in mapping:
			# file upload is redirected to the new directory
			return mapping[type](request)
		return HttpResponse('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

	# return the list of items, serialized and filtered by type
	res = []
	for type in mapping.keys():
		if items_type == 'ALL' or items_type == type:
			res += mapping[type](request).data
	return Response(res)


@csrf_exempt
def routerDetail(request, pk):
	"""
	Function used to invoke the correct CRUD view based on the
	type of the multimedia file.

	@param request: The HttpRequest used to retrieve item data.
	@type request: HttpRequest
	@param pk: Primary key of the requested digital item
	@type pk: int
	@return: An HttpResponse object containing item data or an error.
	@rtype: HttpResponse
	"""
	# dictionary used to invoke the correct set of views
	mapping = {'video': VideoItemDetail.as_view(),
		   'image': ImageItemDetail.as_view(),
                   'audio': AudioItemDetail.as_view()}
	
	# obtain an item and its specific data type
	try:
		i = Item.objects.get(pk=pk)
		return mapping[i.type](request, pk)
	except Item.DoesNotExist:
		return HttpResponse(json.dumps({'error' : 'Item not found'}), status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
def routerRendition(request, pk):
	"""
	Function used to invoke the correct CRUD view based on the
	type of the multimedia file.

	@param request: The HttpRequest used to retrieve item data.
	@type request: HttpRequest
	@param pk: Primary key of the requested digital item
	@type pk: int
	@return: An HttpResponse object containing item data or an error.
	@rtype: HttpResponse
	"""
	# dictionary used to invoke the correct set of views
	mapping = {'video': VideoItemFile.as_view(),
		   'image': ImageItemFile.as_view(),
                   'audio': AudioItemFile.as_view()}
	
	# obtain an item and its specific data type
	try:
		i = Item.objects.get(pk=pk)
		return mapping[i.type](request, pk)
	except Item.DoesNotExist:
		return HttpResponse(json.dumps({'error' : 'Item not found'}), status=status.HTTP_404_NOT_FOUND)
