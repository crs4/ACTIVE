from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from core.plugins.serializers import EventSerializer
from core.plugins.views import EventDetail
from core.plugins.views import EventList


"""	
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plugin_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', run_plugins, name='run_plugins'),
)
"""

urlpatterns = [
    url(r'^events/$', EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', EventDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


