from django.http import HttpResponse, Http404, HttpRequest
from core.items.models import Item

from core.items.video.views import VideoItemList
from core.items.video.views import VideoItemDetail
from core.items.audio.views import AudioItemList
from core.items.audio.views import AudioItemDetail
from core.items.image.views import ImageItemList
from core.items.image.views import ImageItemDetail

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

import json

"""
stringa per testare l'upload di elementi distinti
curl -F "filename=dfdf" -F "owner=1" -F "duration=34567" -F "bitrate=454" -F "format=mpeg4" -F "file=@/var/spool/active/data/hand.png;type=image/video" 156.148.132.79:8000/api/items/
"""


"""
This file contains all methods necessary to invoke the correct view
for each digital item. The decision is based on the file type.

There are two view routers, one for CRUD operations while the other for
list all items togheter and for create a new item.

when a digital item is uploaded:
 - a unique id is created
 - a directory with this id as name is created on the file system
 - item creation and file storing is responsibility of the specific
   item view, that is invoked by file type.

"""


@csrf_exempt
@api_view(('GET','POST'))
def routerList(request):
	"""
	Function used to invoke the correct view based on the
	type of the multimedia file.
	"""
	# dictionary used to invoke the correct set of views
	mapping = {'video': VideoItemList.as_view(),
                   'image': ImageItemList.as_view(),
                   'audio': AudioItemList.as_view()}

	# handle the upload of a new item
	if(request.FILES):
		type = request.FILES['file'].content_type.split('/')[0]
                print(type)
		if type in mapping:
			# file upload is redirected to the new directory
			return mapping[type](request)
		return HttpResponse('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

	# return the list of items, serialized by type
	res = []
	for type in mapping.keys():
		res += mapping[type](request).data
	return Response(res)


@csrf_exempt
def routerDetail(request, pk):
	"""
	Function used to invoke the correct CRUD view based on the
	type of the multimedia file.
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
