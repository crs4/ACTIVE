# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url
from search.views import ESExists, ESCreate, ESUpdate, ESDelete, ESSearch
from search.views import SearchTagItem, SearchTagPerson
from search.views import SearchDynamicTagItem, SearchDynamicTagPerson, SearchDynamicTagByTag
from search.views import KeywordSearch, KeywordFind, PersonSearch, PeopleSearch


urlpatterns = patterns('search.views',

    url(r'^items$', ESSearch.as_view()),
    url(r'^items/exists$', ESExists.as_view()),
    url(r'^items/create$', ESCreate.as_view()),
    url(r'^items/update$', ESUpdate.as_view()),
    url(r'^items/delete$', ESDelete.as_view()),
    
    url(r'^tags/item/(?P<pk>[0-9]+)/$', SearchTagItem.as_view()),
    url(r'^tags/person/(?P<pk>[0-9]+)/$', SearchTagPerson.as_view()),
    
    url(r'^dtags/item/(?P<pk>[0-9]+)/$', SearchDynamicTagItem.as_view()),
    url(r'^dtags/person/(?P<pk>[0-9]+)/$', SearchDynamicTagPerson.as_view()),
    url(r'^dtags/tag/(?P<pk>[0-9]+)/$', SearchDynamicTagByTag.as_view()),
    
    url(r'^keywords/(?P<value>[\w]+)/$', KeywordFind.as_view()),
    url(r'^keywords/(?P<item_type>[0-9A-Za-z]+)/(?P<keyword_list>[\w,]+)/$', KeywordSearch.as_view()),
    
    url(r'^person/(?P<first_name>[\w]+)/(?P<last_name>[\w]+)/$', PersonSearch.as_view()),
    url(r'^people/(?P<first_name>[\w]+)/(?P<last_name>[\w]+)/$', PeopleSearch.as_view()),
)
