"""
This module contains the definition of the URL patterns that must be used
to interact with the REST API for handling User, Group, Permission, ContentType
objects through CRUD operations.
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from core.users.views import UserList, UserDetail, GroupList, GroupDetail
from core.users.views import PermissionList, PermissionDetail, ContentTypeList, ContentTypeDetail

urlpatterns = [
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^groups/$', GroupList.as_view()),
    url(r'^groups/(?P<pk>[0-9]+)/$', GroupDetail.as_view()),
    url(r'^permissions/$', PermissionList.as_view()),
    url(r'^permissions/(?P<pk>[0-9]+)/$', PermissionDetail.as_view()),
    url(r'^content_types/$', ContentTypeList.as_view()),
    url(r'^content_types/(?P<pk>[0-9]+)/$', ContentTypeDetail.as_view())
]

