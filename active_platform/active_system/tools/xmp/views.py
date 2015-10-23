# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from core.items.models import Item
from django.http import Http404
from django.conf import settings
from libxmp import XMPFiles
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tools.xmp.models import XMPMetadata
from tools.xmp.serializers import XMPMetadataSerializer
import os


class XMPMetadataList(generics.ListCreateAPIView):
    """
    Class used to retrieve all stored XMPMetadata objects
    from the database and return them in a JSON serialized format.
    Moreover it is possible to create a new XMPMetadata object
    provided all requested and valid fields in the request.
    """
    queryset =  XMPMetadata.objects.none()
    serializer_class =  XMPMetadataSerializer


class XMPMetadataDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Class used to define the operations used to retrieve, edit
    and delete a specifi XMPMetadata object from the database
    providing its id inside the request.
    """
    queryset =  XMPMetadata.objects.none()
    serializer_class =  XMPMetadataSerializer


class XMPMetadataExtraction(APIView):
    """
    Class used to start the execution of the task necessary
    to extract the XMP metadata from the specified digital item.
    It is necessary to provide the item id.
    """
    queryset = XMPMetadata.objects.none()

    def get(self, request, pk, format=None):
        try:
            # retrieve the item from the file system
            item = Item.objects.get(pk=pk)
            item_path = os.path.join(settings.MEDIA_ROOT, str(item.file))
            # extract the XMP metadata
            xmpfile = XMPFiles()
            xmpfile.open_file(item_path)
            metadata = xmpfile.get_xmp()
            xmpfile.close_file()
            # save a new XMPMetadata object with the association
            obj = XMPMetadata()
            obj.item     = item
            obj.metadata = metadata
            obj.save()
            # return the extracted metadata
            serializer = XMPMetadataSerializer(obj)
            return Response(serializer.data)
        except Exception as e:
            print e
            return Response(status=status.HTTP_404_NOT_FOUND)
