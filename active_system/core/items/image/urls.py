from django.conf.urls import patterns, include, url
from core.items.image.views import ImageItemDetail, ImageItemList

# TODO inserire una descrizione di quali saranno le URL raggiungibili

# items are redirect to a properly handler
urlpatterns = (
    url(r'^image/$', ImageItemList.as_view()),
    url(r'^image/(?P<pk>[0-9]+)/$', ImageItemDetail.as_view()),
)
