# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to define the API REST of the entire ACTIVE system.
For each module embedded in the system (core, tools, authentication) a include
directive is reported, collecting the corresponding available URL patterns (APIs).
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

import core.urls

import tools.navigator.urls
import tools.summarizer.urls
import tools.job_monitor.urls
import tools.training_set_manager.urls
import tools.xmp.urls
import search.urls


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'active_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(
        regex=r'^$',
        view=TemplateView.as_view(template_name='auth/home.html'),
        name='home'
    ),
	url(
        regex=r'^accounts/login/$',
        view='django.contrib.auth.views.login',
        kwargs={'template_name': 'auth/login.html'}
    ),
    url(
        regex='^accounts/logout/$',
        view='django.contrib.auth.views.logout',
        kwargs={'next_page': reverse_lazy('home')}
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include(core.urls)),
    url(r'^job_monitor/', include(tools.job_monitor.urls)),
    url(r'^navigator/', include(tools.navigator.urls)),
    url(r'^summarizer/', include(tools.summarizer.urls)),
    url(r'^training_set_manager/', include(tools.training_set_manager.urls)),
    url(r'^xmp/', include(tools.xmp.urls)),
    url(r'^api/search/', include(search.urls)),
)
