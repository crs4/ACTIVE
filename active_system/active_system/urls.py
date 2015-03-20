from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
import core.users.urls
import core.items.urls
import core.plugins.urls

#import jobmonitor.urls


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
    url(r'^api/', include(core.users.urls)),
    url(r'^api/', include(core.items.urls)),
    url(r'^api/', include(core.plugins.urls)),
   # url(r'^jobmonitor/', include(jobmonitor.urls)),
)
