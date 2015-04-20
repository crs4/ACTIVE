from django.conf.urls import patterns, include, url
from core.tags.dynamic_tags.views import DynamicTagDetail, DynamicTagList
from core.tags.dynamic_tags.views import SearchDynamicTagItem, SearchDynamicTagPerson

"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (plugin, script, event, action).
Moreover it is possible to trigger events and scripts by id.
"""

#TODO descrizione dettagliata delle URL, dei metodi HTTP e dei parametri richiesti


urlpatterns = (
    url(r'^dtags/$', DynamicTagList.as_view()),
    url(r'^dtags/(?P<pk>[0-9]+)/$', DynamicTagDetail.as_view()),   
    url(r'^dtags/search/item/(?P<pk>[0-9]+)/$', SearchDynamicTagItem.as_view()),
    url(r'^dtags/search/person/(?P<pk>[0-9]+)/$', SearchDynamicTagPerson.as_view()),
)

