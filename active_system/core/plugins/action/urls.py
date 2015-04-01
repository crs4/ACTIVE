from django.conf.urls import patterns, include, url

#from rest_framework.urlpatterns import format_suffix_patterns
from core.plugins.action.views import ActionDetail, ActionList


urlpatterns = [
    url(r'^actions/$', ActionList.as_view()),
    url(r'^actions/(?P<pk>[0-9]+)/$', ActionDetail.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)


