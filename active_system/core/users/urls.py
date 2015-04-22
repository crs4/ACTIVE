from django.conf.urls import patterns, include, url
#from rest_framework.urlpatterns import format_suffix_patterns
from core.users.views import ActiveUserList, ActiveUserDetail

urlpatterns = [
    url(r'^$', ActiveUserList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ActiveUserDetail.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
