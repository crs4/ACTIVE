from django.conf.urls import patterns, include, url
from core.items.audio.views import AudioItemDetail, AudioItemList

# TODO inserire una descrizione di quali saranno le URL raggiungibili


# items are redirect to a properly handler
urlpatterns = (
    url(r'^audio/$', AudioItemList.as_view()),
    url(r'^audio/(?P<pk>[0-9]+)/$', AudioItemDetail.as_view()),
)
