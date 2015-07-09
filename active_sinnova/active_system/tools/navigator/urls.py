"""
Module used to define the URL patterns for the navigator tool.
"""

from django.conf.urls import patterns, include, url
from tools.navigator import views


urlpatterns = [
        url(r'^(?P<item_id>[0-9]+)/$', views.index, name="index"),
]
