# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define the URL patterns for the navigator tool.
"""

from django.conf.urls import patterns, include, url
from tools.navigator import views
from tools.navigator.views import SearchPeopleItem


urlpatterns = [
        url(r'^(?P<item_id>[0-9]+)/$', views.index, name="index"),
        url(r'^tags/(?P<pk>[0-9]+)/$', SearchPeopleItem.as_view()),
        
]
