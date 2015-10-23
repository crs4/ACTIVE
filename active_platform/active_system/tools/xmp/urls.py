# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tools.xmp.views import XMPMetadataList
from tools.xmp.views import XMPMetadataDetail
from tools.xmp.views import XMPMetadataExtraction


urlpatterns = [
    url(r'^$', XMPMetadataList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', XMPMetadataDetail.as_view()),
    url(r'^item/(?P<pk>[0-9]+)/$', XMPMetadataExtraction.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
