from django.http import HttpResponse, Http404, HttpRequest
from core.items.models import Item

from core.items.views import VideoItemList
from core.items.views import VideoItemDetail
from core.items.views import AudioItemList
from core.items.views import AudioItemDetail
from core.items.views import ImageItemList
from core.items.views import ImageItemDetail

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
from rest_framework.response import Response

"""
stringa per testare l'upload di elementi distinti
curl -F "title=dfdf" -F "owner=1" -F "duration=34567" -F "frame_width=45" -F "frame_height=45" -F "bitrate=454" -F "format=mpeg4" -F "file=@/var/spool/active/data/hand.png;type=image/video" 156.148.132.79:8000/api/items/
"""





@csrf_exempt
@api_view(('GET',))
def routerList(request):
	mapping = {'video': VideoItemList.as_view(),
                   'image': ImageItemList.as_view(),
                   'audio': AudioItemList.as_view()}

	# se si sta caricando un nuovo file
	if(request.FILES):
		type = request.FILES['file'].content_type.split('/')[0]
		if type in mapping:
			return mapping[type](request)
		return HttpResponse('Content type not supported', status=status.HTTP_400_BAD_REQUEST)

	res = []
	for type in mapping.keys():
		res += mapping[type](request).data
	return Response(res)


@csrf_exempt
def routerDetail(request, pk):
	# dizionario riportante l'associazione tra viste e tipi di item
	mapping = {'video': VideoItemDetail.as_view(),
		   'image': ImageItemDetail.as_view(),
                   'audio': AudioItemDetail.as_view()}

	i = Item.objects.get(pk=pk)

	# applica la vista ai parametri di input
	return mapping[i.type](request, pk)
