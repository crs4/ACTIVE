from django.conf.urls import patterns, include, url
from core.tags.person.views import PersonDetail, PersonList

"""
This module is used to unify the REST API necessary to access Person object data.
"""

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


urlpatterns = (
    url(r'^people/$', PersonList.as_view()),
    url(r'^people/(?P<pk>[0-9]+)/$', PersonDetail.as_view()),
)

