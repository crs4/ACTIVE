from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'activemetadata.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^person/all$', 'core.views.get_all_person'),
    url(r'^person/$', 'core.views.get_person'),
    url(r'^item/$', 'core.views.get_item'),
    url(r'^occurrence/$', 'core.views.get_occurrences'),
    url(r'^admin/', include(admin.site.urls)),
)
