# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import math
from django.conf import settings
from elasticsearch import Elasticsearch
from search.query_maker import QueryMaker


class SearchManager(object):
	"""
	Class used to define an abstract Search Manager,
	containing the main methods that must be implemented.
	"""

	class Meta:
		abstract = True

	def exists():
		""" Method used to check if an object has already been indexed. """
		pass

	def create():
		""" Method used to index an object (not previuosly indexed). """
		pass

	def update():
		""" Method used to update a previously indexed object. """
		pass

	def delete():
		""" Method used to delete the indexed data for an existing object. """
		pass

	def search():
		""" Method used to search in the collection of indexed objects. """
		pass


class ESManager(SearchManager):
	"""
	This class provides an implementation of a SearchManager, using
	Elastic Search to index and retrieve the Item object data.
	"""

	def __check_next_page(self, params, count):
		"""
		Method used to return paginated results
		"""
		total_pages = math.ceil(count/params['size'])
		next_page = (params['from']/params['size']) + 2
		if next_page >= total_pages:
			next_page = None
		return next_page

	def __parse_search_results(self, params, results):
		"""
		Method used to parse the search results
		"""
		count = results['hits']['total']
		hits  = results['hits']['hits']
		for hit in hits:
			hit['_source']['id'] = hit['_id']
		results = [hit['_source'] for hit in hits]
		next = self.__check_next_page(params, count)
		return {'count':count, 'next':next, 'results':results}

	def __common_kwargs(self, params):
		"""
		Method used to convert the result in a common form.
		"""
		kwargs = {}
		kwargs['index'] = settings.ELASTICSEARCH_INDEX
		kwargs['doc_type'] = params['doc_type']
		return kwargs

	def __get_query_name(self, query_params):
		"""
		Method used to detect the type of the search.
		"""
		if len(query_params.keys()) == 1 and 'query' in query_params:
			return 'query'
		if len(query_params.keys()) == 1 and 'filter' in query_params:
			return 'filter'
		if len(query_params.keys()) == 2 and 'query' in query_params and 'filter' in query_params:
			return 'filtered_query'
		return None

	def __invoke(self, op_name, kwargs):
		try:
			self.__es = Elasticsearch(settings.ELASTICSEARCH_URL)
			res = getattr(self.__es, op_name)(**kwargs)
			return res
		except Exception as err:
			msg = 'generic search module error'
			if len(err.args):
				msg = str(err.args)
			return {'error': msg}

	def exists(self, params):
		"""
		Method used to check if an object has already been indexed.
		"""
		kwargs = self.__common_kwargs(params)
		kwargs['id'] = params['params']['id']
		results = self.__invoke('exists', kwargs)
		return {'results': results}

	def create(self, params):
		"""
		Method used to index an object (not previuosly indexed).
		"""
		kwargs = self.__common_kwargs(params)
		if 'id' in params['params']:
			kwargs['id'] = params['params']['id']
		kwargs['body'] = params['params']
		return self.__invoke('create', kwargs)

	def update(self, params):
		"""
		Method used to update a previously indexed object.
		"""
		kwargs = self.__common_kwargs(params)
		kwargs['id'] = params['params']['id']
		kwargs['body'] = {'doc': params['params']}
		kwargs['retry_on_conflict'] = 5
		return self.__invoke('update', kwargs)

	def delete(self, params):
		"""
		Method used to delete the indexed data for an existing object.
		"""
		kwargs = self.__common_kwargs(params)
		kwargs['id'] = params['params']['id']
		results = self.__invoke('delete', kwargs)
		return {'results': results}

	def search(self, params):
		"""
		Method used to search in the collection of indexed objects.
		"""
		kwargs = self.__common_kwargs(params)
		query_name = self.__get_query_name(params['query_params'])
		func = getattr(QueryMaker(), query_name)
		kwargs['body'] = func(params['query_params'])
		if 'size' in params and 'from' in params:
			kwargs['body']['size'] = params['size']
			kwargs['body']['from'] = params['from']
		results = self.__invoke('search', kwargs)
		return self.__parse_search_results(params, results)

