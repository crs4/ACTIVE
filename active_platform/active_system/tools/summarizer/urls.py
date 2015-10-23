# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Thid module defines the URL pattern for the summurizer tool.
"""

from django.conf.urls import patterns, include, url
from tools.summarizer import views


urlpatterns = [
        url(r'^(?P<person_id>[0-9]+)/$', views.index, name="index"),
        url(r'^tags/(?P<pk>[0-9]+)/$', views.SearchItemPerson.as_view()),
]
