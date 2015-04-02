from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, Http404

from django.core.servers.basehttp import FileWrapper

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.video.models import VideoItem
from core.items.video.serializers import VideoItemSerializer


class VideoItemList(EventView):
    """
    This class implements two methods necessary to list all VideoItems objects
    and to create and store a new VideoItem object. 
    """

    def get(self, request, format=None):
	"""
	Method used to list all stored VideoItem objects.
	Objects data is returned in a JSON serialized format.

	@param request: HttpRequest used to retrieve VideoItem data.
        @type request: HttpRequest
	@param format: The format used to serialize objects data, JSON by default.
	@type format: string
	@return: HttpResponse containing all serialized data of retrieved VideoItem objects.
        @rtype: HttpResponse
	"""
	items = VideoItem.objects.all()
        serializer = VideoItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	"""
	Method used to create and store a new VideoItem object with the provided data.

	@param request: HttpRequest containing the serialized data that will be used to create a new VideoItem object.
        @type request: HttpRequest
	@param format: The format used to serialize objects data, JSON by default.
        @type format: string
	@return: HttpResponse containing the id of the new created VideoItem object, error otherwise.
        @rtype: HttpResponse
	"""
	serializer = VideoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoItemDetail(EventView):
    """
    Retrieve, update or delete a video item instance.
    """

    def get_object(self, pk):
	"""
	Method used to retrieve a VideoItem object using its id.
	
	@param request: HttpRequest containing the updated VideoItem field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a VideoItem object.
	@type pk: int
	@return: VideoItem object retrieved by the provided id, error if it isn't available.
        @rtype: VideoItem
	"""
        try:
            return VideoItem.objects.get(item_ptr_id = pk)
        except VideoItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
	"""
	Method used to retrieve data of an existing VideoItem object.
	The retrieved data is returned in a serialized format, JSON by default.

	@param request: HttpRequest containing the updated VideoItem field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
	@param format: Format used for data serialization.
	@type format: string
	@return: HttpResponse containing all serialized data of a VideoItem, error if it isn't available.
        @rtype: HttpResponse
	"""
        item = self.get_object(pk)
        serializer = VideoItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
	"""
	Method used to update stored information of a specific VideoItem object.
	The fresh data is provided in a serialized format.

	@param request: HttpRequest containing the updated VideoItem field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
	@param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all update object data.
        @rtype: HttpResponse
	"""
        item = self.get_object(pk)
        serializer = VideoItemSerializer(item, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	"""
        Method used to delete data about a specific VideoItem object, providing its id.

	@param request: HttpRequest used to delete a specific VideoItem.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
	@rtype: HttpResponse
        """
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# classe temporanea utilizzata per restituire i file e i rispettivi thumbnail
class VideoItemFile(EventView):
    def get(self, request, pk):
	"""
        Method used to retrieve the original file created for a video item or its thumbnail

        @param request: HttpRequest used to delete a specific VideoItem.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a VideoItem object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
        @rtype: HttpResponse
        """

	try:
            video = VideoItem.objects.get(item_ptr_id =pk)
            type = request.GET.get('type', 'original')

            response = None
            if(type == 'original'):
		# TODO risolvere il problema del caricamento lato web server
                response = HttpResponse(FileWrapper(video.file), content_type = 'video/quicktime')
                #response = StreamingHttpResponse(FileWrapper(video.file))
		#response.streaming_content = ['video/quicktime']
                response['Content-Disposition'] = 'attachment; filename="' + video.file.name + '"'
                return response

            if (type == 'thumb'):
                response = HttpResponse(video.thumb, content_type = 'image/png')
            	return response

        except VideoItem.DoesNotExist:
            raise Http404

