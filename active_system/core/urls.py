from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.items.views import ItemList, ItemDetail, ItemFile

import core.items.video.urls
import core.items.image.urls
import core.items.audio.urls


#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


# items are redirect to a properly handler
urlpatterns = [
    url(r'^items/$', ItemList.as_view()),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view()),
    url(r'^items/file/(?P<pk>[0-9]+)/$', ItemFile.as_view()),
    url(r'^items/', include(core.items.video.urls)),
    url(r'^items/', include(core.items.image.urls)),
    url(r'^items/', include(core.items.audio.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
