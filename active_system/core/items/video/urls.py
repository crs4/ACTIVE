from django.conf.urls import patterns, include, url
from core.items.video.views import VideoItemDetail, VideoItemList

# TODO inserire una descrizione di quali saranno le URL raggiungibili

# items are redirect to a properly handler
urlpatterns = (
    url(r'^video/$', VideoItemList.as_view()),
    url(r'^video/(?P<pk>[0-9]+)/$', VideoItemDetail.as_view()),
)
