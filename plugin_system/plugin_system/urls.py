from django.conf.urls import patterns, include, url
from django.contrib import admin
from system_core import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plugin_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.run_plugins, name='run_plugins'),

)
