from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from job_manager.views import JobDetail, JobList


urlpatterns = [
    url(r'^jobs/$', JobList.as_view()),
    url(r'^jobs/(?P<job_id>[A-Za-z0-9\-]+)/$', JobDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
