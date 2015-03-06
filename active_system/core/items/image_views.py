from django.shortcuts import render
from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.items.models import ImageItem
from core.items.serializers import ImageItemSerializer


class ImageItemList(APIView):
    def get(self, request, format=None):
	items = ImageItem.objects.all()
        serializer = ImageItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	serializer = ImageItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ImageItemDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
	"""
	Method used to obtain item data by his id.
	:param pk: Image's id.
	:returns: Object containing user data if any, HTTP error otherwise.
	"""
        try:
            return ImageItem.objects.get(item_ptr_id = pk)
        except ImageItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
	"""
	Method used to return serialized data of a user.
	:param pk: User's id.
	:param format: Format used for data serialization.
	:returns: Image serialized data.
	"""
        item = self.get_object(pk)
        serializer = ImageItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
	"""
	Method used to update user information providing
	serialized data.
	:param pk: Image id.
	:param format: Format used for data serialization.
        :returns: User data update status.
	"""
        item = self.get_object(pk)
        serializer = ImageItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	"""
        Method used to delete user information providing his ID.
        :param pk: Image id.
        :param format: Format used for data serialization.
        :returns: User data deletion status.
        """
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


