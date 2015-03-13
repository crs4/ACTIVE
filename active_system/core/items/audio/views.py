from django.shortcuts import render
from django.http import HttpResponse, Http404

from core.views import EventView
from rest_framework.response import Response
from rest_framework import status

from core.items.audio.models import AudioItem
from core.items.audio.serializers import AudioItemSerializer


class AudioItemList(EventView):
    def get(self, request, format=None):
	items = AudioItem.objects.all()
        serializer = AudioItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	serializer = AudioItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AudioItemDetail(EventView):
    """
    Retrieve, update or delete a Audio item instance.
    """
    def get_object(self, pk):
        try:
            return AudioItem.objects.get(item_ptr_id = pk)
        except AudioItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = AudioItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
	"""
	Method used to update user information providing
	serialized data.
	:param pk: Audio's id.
	:param format: Format used for data serialization.
        :returns: User data update status.
	"""
        item = self.get_object(pk)
        serializer = AudioItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	"""
        Method used to delete user information providing his ID.
        :param pk: User's id.
        :param format: Format used for data serialization.
        :returns: User data deletion status.
        """
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


