"""
Thid module defines the URL pattern for the summurizer tool.
"""

from django.conf.urls import patterns, include, url
from tools.summarizer import views


urlpatterns = [
        url(r'^(?P<person_id>[0-9]+)/$', views.index, name="index"),
]
