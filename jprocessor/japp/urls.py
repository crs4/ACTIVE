from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from japp.views import *

urlpatterns = patterns('',

	url(r'^faceextractor/$', FaceExtractorList.as_view(), name='face_extractor_list'),
	
)

urlpatterns = format_suffix_patterns(urlpatterns)
