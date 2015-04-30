from django.conf.urls import patterns, include, url
from tools.navigator import views




urlpatterns = [
        url(r'^(?P<item_id>[0-9]+)/$', views.index, name="index"),
]
