# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to unify the REST API necessary to access to each data provided
by the plugin module (person, tags, dynamic tags and keywords).
From this module it is possible to access directly to generic Tags views (and HTTP methods).
Tags objects are returned in a JSON serialized format.

For each module it will be possible to obtain more information about
the available REST API inside the respective urls.py module.

GET     /training_set_manager/models/          obtain all stored EntityModel objects
POST    /training_set_manager/models/          create a new EntityModel object with the provided data
GET     /training_set_manager/models/12/       obtain stored data for EntityModel object with id = 12
PUT     /training_set_manager/models/12/       upload stored data for EntityModel object with id = 12
DELETE  /training_set_manager/models/12/       delete stored data for EntityModel object with id = 12

GET     /training_set_manager/instances/          obtain all stored Instance objects
POST    /training_set_manager/instances/          create a new Instance object with the provided data
GET     /training_set_manager/instances/12/       obtain stored data for Instance object with id = 12
PUT     /training_set_manager/instances/12/       upload stored data for Instance object with id = 12
DELETE  /training_set_manager/instances/12/       delete stored data for Instance object with id = 12

GET     /training_set_manager/models/instancesearch/?model_id=12/       obtain Instance objects for EntityModel with id = 12
"""

from django.conf.urls import include, url, patterns
from tools.training_set_manager.views import EntityModelList, EntityModelDetail, BuildEntityModel
from tools.training_set_manager.views import InstanceList, InstanceDetail, InstanceFile
from tools.training_set_manager.views import SearchInstance, SearchModelByEntity


urlpatterns = patterns('tools.training_set_manager.views',
    url(r'^$', 'index', name='index'),
    url(r'^models/$', EntityModelList.as_view()),
    url(r'^models/(?P<pk>[0-9]+)/$', EntityModelDetail.as_view()),
    url(r'^models/build/(?P<pk>[0-9]+)/$', BuildEntityModel.as_view()),
    url(r'^models/instancesearch/(?P<pk>[0-9]+)/$', SearchInstance.as_view()),
    url(r'^models/entitysearch/(?P<pk>[0-9]+)/$', SearchModelByEntity.as_view()),
    url(r'^instances/$', InstanceList.as_view()),
    url(r'^instances/(?P<pk>[0-9]+)/$', InstanceDetail.as_view()),
    url(r'^instances/file/(?P<pk>[0-9]+)/$', InstanceFile.as_view()),
)
