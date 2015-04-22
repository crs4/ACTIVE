from django.conf.urls import patterns, include, url
#from rest_framework.urlpatterns import format_suffix_patterns

import core.tags.person.urls
import core.tags.dynamic_tags.urls
from core.tags.views import TagList, TagDetail

"""
TODO
"""

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


urlpatterns = (
        url(r'^tags/$', TagList.as_view()),
        url(r'^tags/(?P<pk>[0-9]+)/$', TagDetail.as_view()),
        url(r'^people/', include(core.tags.person.urls)),
        url(r'^dtags/', include(core.tags.dynamic_tags.urls)),
)

#urlpatterns = format_suffix_patterns(urlpatterns)
