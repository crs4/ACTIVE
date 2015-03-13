from django.conf.urls import patterns, include, url
from django.contrib import admin
#import jobmonitor.urls
import jobmanager.urls
import clustermanager.urls
import pluginmanager.urls
#import jobmonitor.views

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'jobprocessor.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),

	# jobmonitor API definition, which allows to handle job execution
	#url(r'^jobmonitor/', include(jobmonitor.urls)), # vengono invocate in modo indiretto le view del jobmanager
	url(r'^jobmanager/', include(jobmanager.urls)), # vengono invocate in modo indiretto le view del jobmanager
	url(r'^cluster/', include(clustermanager.urls)),
	url(r'^plugin/', include(pluginmanager.urls)),
	
	#url(r'^api/job/', include(jobmanager.urls)),
	#url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
