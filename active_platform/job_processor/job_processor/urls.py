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

