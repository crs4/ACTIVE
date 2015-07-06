from django.shortcuts import render_to_response
from django.template import RequestContext


# return the static page 
def index(request, item_id):	
	return render_to_response("video_viewer.html",{"itemid": item_id},context_instance=RequestContext(request))
