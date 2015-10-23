# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created to the the REST API for the search module, in order to 
check if it is possible to manage the searches in the ACTIVE platform.
For authentication purposes it is necessary to create a User called "root".
"""

from core.items.models import Item
from core.items.serializers import ItemSerializer
from core.tags.models import Tag
from core.tags.person.models import Person
from core.tags.keywords.models import Keyword
from core.tags.dynamic_tags.models import DynamicTag
from search.es_manager import ESManager
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from time import sleep
import json
import os


class SearchManagerTest(TestCase):
    """
    Test suite used to check the REST API for searching Items.
    """

    def setUp(self):
        """
        Method used to setup the test database
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
        sleep(1)

    def tearDown(self):
        """
        Remove the objects previuosly indexed.
        """
        for i in range(11):
            if self.sm.exists({'doc_type' : 'items', 'params': { 'id' : i+1 }})['results']:
                self.sm.delete({'doc_type': 'items', 'params': { 'id' : i+1 }})

    def test_check(self):
        """
        Check Item object existance
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"doc_type": "items", 
                "params":{"id":1}
        }
        response = client.post('/api/search/items/exists', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	self.assertEqual(json.loads(response.content)['results'], True)

    def test_create(self):
        """
        Index a new Item
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        item = Item()
        item.type = 'image'
        item.filename = 'test_'
        item.mime_type = 'image/png'
        item.owner = User.objects.all()[0]
        item.save()
        data = {"doc_type" : "items",
                "params": ItemSerializer(item).data
        }
        response = client.post('/api/search/items/create', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['created'], True)

    def test_update(self):
        """
        Update an indexed Item
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        item = Item.objects.get(pk=1)
        item.description = 'edited image'
        item.save()
        data = {"doc_type" : "items",
                "params": ItemSerializer(item).data
        }
        response = client.put('/api/search/items/update', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Remove an Item from the index
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"doc_type": "items",
                "params"  : {"id": 1}
        }
        response = client.delete('/api/search/items/delete', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query(self):
        """
        Search Item by query
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { "query": {"text": "test_1", "fields": ["filename"]}}
        }
        response = client.post('/api/search/items', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['count'], 1)

    def test_filter(self):
        """
        Search Item by filter
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { "filter": {"field": "filename", "value": "test_3"}}
        }
        response = client.post('/api/search/items', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['count'], 1)

    def test_filtered_query(self):
        """
        Search Item by filtered query
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": { 
                     "filter": {"field": "filename", "value": "test_3"},
                     "query" : {"text" : "image", "fields": ["mime_type", "type"]}
                  }
        }
        response = client.post('/api/search/items', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['count'], 1)

    def test_filtered_query2(self):
        """
        Search Item by filtered query
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        data = { "doc_type": "items",
                 "size": 32,
                 "from": 0,
                 "query_params": {
                     "filter": {"field": "filename", "value": "test_3"},
                     "query" : {"text" : "video", "fields": ["mime_type", "type"]}
                  }
        }
        response = client.post('/api/search/items', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['count'], 0)


class SearchTagTest(TestCase):
    """
    Test suite used to check the REST API for searching Tags.
    """
    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create Item objects
        for i in range(10):
            item = Item()
            item.type = 'image'
            item.filename = 'test_' + str(i)
            item.description = 'test'
            item.mime_type = 'image/png'
            item.owner = user
            item.save()
        # create Person objects
        for i in range(10):
            person = Person()
            person.category   = 'person'
            person.first_name = 'John'
            person.last_name  = 'Doe' + str(i)
            person.save()
        # create Tag objects
        for i in range(10):
            tag = Tag()
            tag.item   = Item.objects.get(pk=i+1)
            tag.entity = Person.objects.get(pk=i+1)
            tag.type   = 'test'
            tag.save()

    def test_item_1(self):
        """
        Search a Tag by the associated Item object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/tags/item/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_item_2(self):
        """
        Search a Tag by an inexistant Item object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/tags/item/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_person_1(self):
        """
        Search a Tag by the associated Person object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/tags/person/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_person_2(self):
        """
        Search a Tag by an inexistant Person object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/tags/person/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class SearchDynamicTagTest(TestCase):
    """
    Test suite used to check the REST API for searching DynamicTags.
    """
    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create Item objects
        for i in range(10):
            item = Item()
            item.type = 'image'
            item.filename = 'test_' + str(i)
            item.description = 'test'
            item.mime_type = 'image/png'
            item.owner = user
            item.save()
        # create Person objects
        for i in range(10):
            person = Person()
            person.category   = 'person'
            person.first_name = 'John'
            person.last_name  = 'Doe' + str(i)
            person.save()
        # create Tag objects
        for i in range(10):
            tag = Tag()
            tag.item   = Item.objects.get(pk=i+1)
            tag.entity = Person.objects.get(pk=i+1)
            tag.type   = 'test'
            tag.save()
        # create DynamicTag objects
        for i in range(10):
            dtag = DynamicTag()
            dtag.tag      = Tag.objects.get(pk=i+1)
            dtag.start    = 0
            dtag.duration = 2000
            dtag.save()

    def test_item_1(self):
        """
        Search a DynamicTag by the associated Item object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/item/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_item_2(self):
        """
        Search a DynamicTag by an inexistant Item object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/item/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_person_1(self):
        """
        Search a DynamicTag by the associated Person object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/person/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_person_2(self):
        """
        Search a DynamicTag by an inexistant Person object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/person/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_tag_1(self):
        """
        Search a DynamicTag by the associated Tag object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/tag/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_tag_2(self):
        """
        Search a DynamicTag by an inexistant Tag object.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/dtags/tag/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    

class SearchKeywordsTest(TestCase):
    """
    Test suite used to check the REST API for searching Keywords.
    """
    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create Keyword objects
        for i in range(10):
            keyword = Keyword()
            keyword.category    = 'keyword'
            keyword.description = 'koala' + str(i)
            keyword.save()
        
    def test_1(self):
        """
        Search a Keyword by its description with exact matching.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/keyword/koala1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_1(self):
        """
        Search a Keyword by its description with exact matching.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/keyword/koala/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SearchPeopleTest(TestCase):
    """
    Test suite used to check the REST API for searching Person objects.
    """
    
    def setUp(self):
        """
        Method used to setup the test database
        """
        # create a new user
        user  = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        # create Person objects
        for i in range(10):
            person = Person()
            person.category   = 'person'
            person.first_name = 'John'
            person.last_name  = 'Doe' + str(i)
            person.save()

    def test_1(self):
        """
        Search a Person by first and last name with exact matching.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/person/John/Doe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_2(self):
        """
        Search an inexistant Person by first and last name with exact matching.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/person/Jane/Doe/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_3(self):
        """
        Search all Person objects by first and last name as prefix.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/people/John/Doe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_4(self):
        """
        Search all Person objects by first and last name as prefix.
        """
        user = User.objects.all()[0]
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/search/people/Jane/Doe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
