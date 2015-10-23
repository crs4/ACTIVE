# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from django.contrib import admin

import job_manager.urls
import cluster_manager.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'job_processor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(job_manager.urls)),
    url(r'^api/', include(cluster_manager.urls)),
]

