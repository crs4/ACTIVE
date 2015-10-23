# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module defines all tests for the internal API of Keyword objects.
"""

from core.tags.keywords.models import Keyword
from django.test import TestCase
from django.test import Client
import json

def create_keyword(description):     
    keyword = Keyword.objects.create(description = description)
    return keyword


class KeywordTests(TestCase):

    def test_create(self):
        """
        Test used to create and save a fake person.
        """        
        keyword = create_keyword("test")
        self.assertTrue(isinstance(keyword, Keyword))
        self.assertEqual(1,Keyword.objects.count())
        
    def test_get(self):
        """
        Test used to get a fake person.
        """   
        keyword = create_keyword("test")
        keyword_retrieved = Keyword.objects.filter(pk=keyword.pk)        
        self.assertEqual(keyword, keyword_retrieved[0])
        
    def test_update(self):
        """
        Test used to update fake person.
        """   
        keyword = create_keyword("test")
        keyword.description = 'test_update'
        keyword.save()
        keyword_retrieved = Keyword.objects.filter(pk=keyword.pk)     
        self.assertEqual(keyword.description, keyword_retrieved[0].description)

    def test_delete(self):
        """
        Test used to delete a fake person.
        """   
        keyword = create_keyword("test")
        keyword.delete()
        if Keyword.objects.filter(pk=keyword.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            

