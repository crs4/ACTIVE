from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.items.views import ItemList, ItemDetail, ItemFile

import core.items.urls
import core.plugins.urls
import core.tags.urls
import core.users.urls

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


# items are redirect to a properly handler
urlpatterns = [
	url(r'^items/', include(core.items.urls)),
	url(r'', include(core.plugins.urls)),
	url(r'', include(core.tags.urls)),
	url(r'users/', include(core.users.urls)),

]

urlpatterns = format_suffix_patterns(urlpatterns)
