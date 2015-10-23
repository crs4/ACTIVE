# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2

"""
This module has been defined in order to test the available
internal search API. All tests are divided by related module.
"""

from core.items.models import Item
from core.items.serializers import ItemSerializer
from core.tags.dynamic_tags.models import DynamicTag
from core.tags.keywords.models import Keyword
from core.tags.person.models import Person
from django.contrib.auth.models import User
from django.test import TestCase
from search.es_manager import ESManager
from time import sleep

class IndexTest(TestCase):
    """
    Class used to define all tests related to objects indexing.
    """
    def setUp(self):
        """
        Setup the database and index some objects.
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()

        # create the search manager
        self.sm = ESManager()
        
        # create and index some items
        for i in range(10):
            item = Item()
            item.type = 'image'
            item.filename = 'test_' + str(i)
            item.mime_type = 'image/png'
            item.owner = user
            item.save()

            serializer = ItemSerializer(item)
            self.sm.create({'doc_type' : 'items', 'params' : serializer.data })

    def tearDown(self):
        """
        Remove the objects previuosly indexed.
        """
        for i in range(11):
            if self.sm.exists({'doc_type' : 'items', 'params': { 'id' : i+1 }})['results']:
                self.sm.delete({'doc_type': 'items', 'params': { 'id' : i+1 }})

    def test_exists(self):
        """
        Test used to check if an object has already been indexed.
        """
        result = self.sm.exists({'doc_type' : 'items', 'params': { 'id' : 1 }})
        self.assertEqual(result['results'], True)

    def test_not_exists(self):
        """
        Test used to check if not indexed objects are detected.
        """
        result = self.sm.exists({'doc_type' : 'items', 'params': { 'id' : 0 }})
        self.assertEqual(result['results'], False)

    def test_create(self):
        """
        Method used to index a new object.
        """
        item = Item()
        item.type = 'image'
        item.filename = 'test_'
        item.mime_type = 'image/png'
        item.owner = User.objects.all()[0]
        item.save()

        serializer = ItemSerializer(item)
        result = self.sm.create({'doc_type' : 'items', 'params' : serializer.data })
        self.assertEqual(result['created'], True)
        
    def test_update(self):
        """
        Method used to update the fields of an existing object.
        """
        data = {'uploaded_at': '2015-09-14T17:03:21.780176Z', 'description': 'Custom file', 
                'state': 'STORED, ANALYZED', 'visibility': False, 'filename': 'test_1', 
                'published_at': None, 'filesize': '', 'owner': 1,  'type': 'image',
                'id': 1, 'mime_type': 'image/png'}
        result = self.sm.update({'doc_type' : 'items', 'params': data})
        self.assertNotEqual(result['_version'], 1)

    def test_delete(self):
        """
        Method used to remove indexed data of an existing object.
        """
        result = self.sm.delete({'doc_type' : 'items', 'params': { 'id' : 1 }})
        self.assertNotEqual(result['results']['_version'], 1)


class ItemSearchTest(TestCase):
    """
    Class used to define all tests related to Item objects search.
    """

    def setUp(self):
        """
        Setup the database and index some objects.
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()

        # create the search manager
        self.sm = ESManager()
        
        # create and index some items
        for i in range(100):
            item = Item()
            item.type = 'image'
            item.filename = 'test_' + str(i)
            item.description = 'test'
            item.mime_type = 'image/png'
            item.owner = user
            item.save()

            serializer = ItemSerializer(item)
            self.sm.create({'doc_type' : 'items', 'params' : serializer.data })
        sleep(1)

    def tearDown(self):
        """
        Remove the objects previuosly indexed.
        """
        for i in range(101):
            if self.sm.exists({'doc_type' : 'items', 'params': { 'id' : i+1 }})['results']:
                self.sm.delete({'doc_type' : 'items', 'params': { 'id' : i+1 }})

    def test_filter(self):
        """
        Method used to test the search by filter over Item objects.
        """
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { "filter": {"field": "filename", "value": "test_1"}
                 }
	}
        results = self.sm.search(data)
        self.assertEquals(results['count'], 1)


    def test_query(self):
        """
        Method used to test the search by query over Item objects.
        """
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { "query": {"text": "test", "fields": ["filename", "description"]}
                 }
	}
        results = self.sm.search(data)
        self.assertEquals(results['count'], 100)

    def test_filtered_query(self):
        """
        Method used to test the search by filtered query over Item objects.
        This search uses both filter and query parameters for retrieving objects.
        """
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { 
                     "filter": {"field": "filename", "value": "test_1"},
                     "query" : {"text": "test", "fields": ["filename", "description"]}
                 }
	}
        results = self.sm.search(data)
        self.assertEquals(results['count'], 1)

