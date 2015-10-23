# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

class Mapper:

	def setting_rules(self):
		return {
			"analysis": {
				"filter": {
					"trigrams_filter": {
						"type": "ngram",
						"min_gram": 3,
						"max_gram": 3
					}
			    	},
			    	"analyzer": {
					"trigrams": {
					    	"type": "custom",
					    	"tokenizer": "standard",
					    	"filter": [
							"lowercase",
							"trigrams_filter"
					    	]
					}
			    	}
			}
		}

	def mapping_rules(self):
		return {
			"items": {
				"_all": {"enabled": False},
				"properties": {
					"item_id": {
						"type": "long",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"type": {
						"type": "string",
						"store": "yes"
					},
					"filename": {
						"type": "string",
						"store": "yes"
					},
					"description": {
						"type": "string",
						"store": "yes",
						"analyzer": "trigrams"
					},
					"owner": {
						"type": "long",
						"store": "yes"
					},
					"keywords": {
						"type": "string",
						"store": "yes",
						"analyzer": "trigrams"
					},
					"file": {
						"type": "string",
						"index": "not_analyzed",
						"store": "yes"
					},
					"format": {
						"type": "string",
						"index": "not_analyzed",
						"store": "yes"
					},
					"mime_type": {
						"type": "string",
						"index": "not_analyzed",
						"store": "yes"
					},
					"filesize": {
						"type": "string",
						"index": "not_analyzed",
						"store": "yes"
					},
					"state": {
						"type": "string",
						"index": "not_analyzed",
						"store": "yes"
					},
					"frame_width": {
						"type": "long",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"frame_height": {
						"type": "long",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"frame_rate": {
						"type": "double",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"duration": {
						"type": "double",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"uploaded_at": {
						"type": "date",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"sample_rate": {
						"type": "long",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"num_channels": {
						"type": "long",
						"index": "not_analyzed", 
						"store": "yes"
					},
					"visibility": {
						"type": "boolean",
						"index": "not_analyzed", 
						"store": "yes"
					}
				}
			}
		}
	
