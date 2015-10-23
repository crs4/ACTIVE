# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from job_manager.views import JobDetail, JobList

"""
This module defines all URL patterns used to define the REST API
for the job manager module.

These are the relative paths that could be used to handle the job execution,
using the provided REST API. A short description for each URL pattern is defined:

GET	/api/jobs/?status=ALL		retrieve all Job objects filtering by status

POST	/api/jobs/			start the execution of a new Job

DELETE	/api/jobs/			remove alla completed or queued Jobs


GET	/api/jobs/12/		retrieve information about the Job with id = 12

POST	/api/jobs/12/		check if the result of the Job with id = 12 is available

PUT	/api/jobs/12/		retrieve the result of the Job with id = 12

DELETE	/api/jobs/12/		remove information about the Job with id = 12

"""

urlpatterns = [
    url(r'^jobs/$', JobList.as_view()),
    url(r'^jobs/(?P<pk>[A-Za-z0-9\-]+)/$', JobDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
