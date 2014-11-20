from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from japp.views import *

urlpatterns = patterns('',

	url(r'^extractor/face/$', FaceExtractorList.as_view(), name='face_extractor'),
	url(r'^extractor/xmp/$', XMPExtractorList.as_view(), name='xmp_extractor'),
	url(r'^embedder/xmp/$', XMPEmbedderList.as_view(), name='xmp_embedder'),
	
)

urlpatterns = format_suffix_patterns(urlpatterns)
