# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all classes needed to define the serializers
for Instance and EntityModel objects. These serializers are defined in order
to provide a REST API converting the objects from and to a JSON format.
"""

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from tools.training_set_manager.models import Instance, EntityModel


class EntityModelSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for EntityModel object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = EntityModel
        fields = ('id', 'name', 'entity', 'model_file', 'type','last_update')


class EntityModelPagination(PageNumberPagination):
    """
    This class is used to create a paginator for EntityModel
    object. Results are returned providing the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32


class InstanceSerializer(serializers.ModelSerializer):
    """
    This class define a base serializer for Instance object.
    Object fields are converted in a JSON format.
    """
    class Meta:
        model = Instance
        fields = ('id', 'thumbnail', 'features', 'type', 
                  'trusted', 'entity_model', 'item', 'dtag')


class InstancePagination(PageNumberPagination):
    """
    This class is used to create a paginator for Instance
    object. Results are returned providing the maximum number of results per page.
    """
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 32
