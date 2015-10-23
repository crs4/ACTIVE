# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines the views provided by the navigator tool.
It simply returns a template providing the item id as parameter.
"""

from core.views import EventView
from core.tags.models import Tag
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.person.models import Person
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.response import Response
from rest_framework import status
import json
import logging
import threading

# return the static page 
def index(request, item_id):	
	return render_to_response("video_viewer.html",{"itemid": item_id},context_instance=RequestContext(request))


class SearchPeopleItem(EventView):
    """
    Class used to implement methods necessary to search all people details
    associated to Tags objects in a specific digital item.
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
        people_data = []
        tags = Tag.user_objects.by_user(request.user).filter(item__id = pk)
        if not tags:
            raise Http404
        for tag in tags:
            if "keyword" not in tag.type:
                person_dict = {}
                starts = []
                durations = []
                dtags = DynamicTag.objects.filter(tag__id = tag.id)
                person = Person.objects.get(entity_ptr_id = tag.entity)                
                for dt in dtags:                    
                    starts.append(dt.start/float(1000))
                    durations.append(dt.duration/float(1000))
                
                person_dict['first_name'] = person.first_name
                person_dict['last_name'] = person.last_name
                person_dict['tag_type'] = tag.type
                person_dict['starts'] = starts
                person_dict['durations'] = durations
                person_dict['tad_id'] = tag.id
                person_dict['person_id'] = tag.entity.id
                
                people_data.append(json.dumps(person_dict))
        
        return Response(people_data)
