# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.

from django.conf import settings
from search.mappers import Mapper
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout, RequestError

try:
	es = Elasticsearch(settings.ELASTICSEARCH_URL)
	if not es.indices.exists(index=settings.ELASTICSEARCH_INDEX):
		body = {
			"settings": getattr(Mapper(), 'setting_rules')(),
			"mappings": getattr(Mapper(), 'mapping_rules')()
		}
		es.indices.create(index=settings.ELASTICSEARCH_INDEX, body=body)
except (ConnectionError, ConnectionTimeout, RequestError) as err:
	pass
