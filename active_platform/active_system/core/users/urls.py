# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains the definition of the URL patterns that must be used
to interact with the REST API for handling User, Group, Permission, ContentType
objects through CRUD operations.

PS: the REST API endpoints for Group, Permission and ContentType editing had
been commented because it is not useful to expose them. If necessary they can
be edited by the administrator or uncomment the urls patterns.
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from core.users.views import UserList, UserDetail, GroupList, GroupDetail
from core.users.views import PermissionList, PermissionDetail, ContentTypeList

urlpatterns = [
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^groups/$', GroupList.as_view()),
    #url(r'^groups/(?P<pk>[0-9]+)/$', GroupDetail.as_view()),
    #url(r'^permissions/$', PermissionList.as_view()),
    #url(r'^permissions/(?P<pk>[0-9]+)/$', PermissionDetail.as_view()),
    #url(r'^content_types/$', ContentTypeList.as_view())
]

