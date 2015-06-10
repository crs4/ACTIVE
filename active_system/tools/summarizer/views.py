from django.shortcuts import render_to_response
from django.template import RequestContext


# return the static page 
def index(request, person_id):	
	return render_to_response("video_summarizer.html",{"personid": person_id},context_instance=RequestContext(request))
