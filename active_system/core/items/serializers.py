"""
This module is used to define a REST API able to generate JSON serialized data.
Two classes has been defined:
    - a serializer used to convert generic Item objects in JSON format;
    - a paginator necessary to handle the potentially big amount of retrieved items.
"""

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from core.items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for generic digital items.
    Only main field of a digital item are converted in a JSON format.
    """
 
    class Meta:
        model = Item
        #fields = ('id', 'description', 'type', 'mime_type', 'filename',
        #          'filesize', 'visibility', 'uploaded_at', 'published_at',
        #          'file', 'thumb', 'preview', 'state', 'owner')


    """
    def update(self, instance, validated_data):

        # keys selected fot item update
        keys = validated_data.keys()
        if 'id' in keys:
            keys.remove('id')
        print keys

        # update all fields but the id
        for attr, value in validated_data.items():
            if attr != 'id':
               setattr(instance, attr, value)

        # save the instance with the updated fields
        instance.save(update_fields=keys)

        ""
        if self.partial :
            if validated_data:
                print validated_data
                print validated_data.keys()

                for attr, value in validated_data.items():
                   setattr(instance, attr, value)

                instance.save(update_fields=validated_data.keys())
            else:
                instance.save()
        else:
            super(serializers.ModelSerializer, self).update(instance, validated_data)

        return self.instance
        """

class ItemPagination(PageNumberPagination):
    """
    This class is used to create a paginator for Item objects.
    object. Results are returned providing the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32

