# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define all views provided by the summarizer tool.
It simply returns a template page providing the person id parameter.
"""

from core.views import EventView
from core.items.models import Item
from core.tags.models import Tag
from core.tags.dynamic_tags.models import Tag, DynamicTag
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import status
import logging
import threading
import json

# return the static page 
def index(request, person_id):	
	return render_to_response("video_summarizer.html",{"personid": person_id},context_instance=RequestContext(request))


class SearchItemPerson(EventView):
    """
    Class used to implement methods necessary to search all item details 
    associated to a specific Person object in a digital item.
    """
    queryset = Tag.objects.none()  # required for DjangoModelPermissions

    def get(self, request, pk, format=None):
        """
        Method used to retrieve all Tag objects containing
        the occurrences in a specific digital item (if any).

        @param request: HttpRequest used to retrieve data of Tag objects.
        @type request: HttpRequest
        @param pk: Item object primary key, used to retrieve tag data.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse
        @rtype: HttpResponse
        """
        item_data = []
        tags = Tag.user_objects.by_user(request.user).filter(entity__id = pk)
        if not tags:
            raise Http404
        for tag in tags:
            if tag.type == "face+speaker":
                item_dict = {}
                starts = []
                durations = []
                dtags = DynamicTag.objects.filter(tag__id = tag.id)
                item = Item.user_objects.by_user(request.user).get(pk = tag.item.id)                
                for dt in dtags:                    
                    starts.append(dt.start/float(1000))
                    durations.append(dt.duration/float(1000))
                
                item_dict['title'] = item.filename
                item_dict['url'] = "/api/items/file/"+str(item.id)+"?type=preview"
                item_dict['starts'] = starts
                item_dict['durations'] = durations
                
                item_data.append(json.dumps(item_dict))
        
        return Response(item_data)
