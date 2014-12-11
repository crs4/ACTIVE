from django.conf.urls import patterns, include, url
from django.contrib import admin
from proxy.views import *

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'jobprocessor.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),

	# definizione delle API che deve fornire un generico Job Processor (tutti metodi GET)
	url(r'^api/task/start/',  view_start_task,  name="view_start_task"),   # avvia un task in modo asincrono
	url(r'^api/task/result/', view_result_task, name="view_result_task"),  # ottiene il risultato di una computazione asincrona (attesa bloccante)
	url(r'^api/task/stop/',   view_stop_task,   name="view_stop_task"),    # interrompere l'esecuzione di un task
)
