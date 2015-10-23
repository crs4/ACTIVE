# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2

import re


class QueryDict(dict):	
	def __init__(self):
		self.__query = {}
		
	def __getitem__(self, path):
		schema = self.__query
		for key in path.split('.'):
			schema = schema[key]
		return schema
	
	def __setitem__(self, path, value):
		schema = self.__query
		p_list = path.split('.')
		target = reduce(lambda d, k: d.setdefault(k, {}), p_list[:-1], schema)
		target[p_list[-1]] = self.__parse_value(value)
		return schema
		
	def __parse_value(self, value):
		if isinstance(value, str):
			value.lower()
			value = re.sub(r'[^\w]', ' ', value)
			value = ' '.join(value.split())
		return value 
				
	def query(self):
		return self.__query


class QueryMaker(object):
	def filter(self, query_params):
		field = query_params['filter']['field']
		value = query_params['filter']['value']
		qd = QueryDict()
		qd['query.filtered.filter.term.' + field] = value
		return qd.query()
		
	def query(self, query_params):
		base = 'query.multi_match.'
		qd = QueryDict()
		qd[base + 'query'] = query_params['query']['text']
		qd[base + 'fields'] = query_params['query']['fields']
		return qd.query()

	def filtered_query(self, query_params):
		base = 'query.filtered.'
		qd = QueryDict()
		qd[base + 'filter.term.' + query_params['filter']['field']] = query_params['filter']['value']
		qd[base + 'query.multi_match.query'] = query_params['query']['text']
		qd[base + 'query.multi_match.fields'] = query_params['query']['fields']
		return qd.query()

	def geo_points_distance(self, query_params):
		base = 'query.filtered.filter.geo_distance.'
		qd = QueryDict()
		qd[base + 'distance'] = query_params['dist'] + 'km'
		qd[base + 'distance_type'] = 'plane'
		qd[base + 'geocode.lat'] = query_params['lat']
		qd[base + 'geocode.lon'] = query_params['lon']
		return qd.query()

