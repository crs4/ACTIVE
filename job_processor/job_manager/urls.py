"""
This module is used to define the URL pattern for the Job Manager modules.
It is possible to interact with the Job Manager using a predefined set of
methods/endpoints allowing CRUD operations on Job objects.

Here there are all available endpoints, defined by a URL pattern and an HTTP method:

GET     /api/jobs/      retrieve all stored Job objects

POST    /api/jobs/      create a new Job object with provided data


GET     /api/jobs/12    retrieve the Job object with id = 12

PUT     /api/jobs/12    edit information of Job object with id = 12

DELETE  /api/jobs/12    delete information of Job object with id = 12
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from job_manager.views import JobDetail, JobList


urlpatterns = [
    url(r'^jobs/$', JobList.as_view()),
    url(r'^jobs/(?P<pk>[A-Za-z0-9\-]+)/$', JobDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
