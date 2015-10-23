# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from core.items.models import Item
from core.tags.models import Tag, Entity
from core.tags.dynamic_tags.models import DynamicTag
from django.contrib.auth.models import User
from django.test import TestCase
import json


class DynamicTagTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='123')
        item = Item.objects.create(filename='test', owner=user)
        entity = Entity.objects.create(category = 'test_category')
        tag = Tag.objects.create(item=item, entity=entity, type='test')
        dtag = DynamicTag.objects.create(tag=tag, start=0, duration=0)

    def test_create(self):
        """
        Test used to create and save a DynamicTag object.
        """
        tag = Tag.objects.all()[0]
        dtag = DynamicTag.objects.create(tag=tag, start=0, duration=0)
        # check if the dtag has been created
        num = DynamicTag.objects.count()
        self.assertEqual(2, num)
    
    def test_get(self):
        """
        Test used to retrieve a DynamicTag object.
        """
        dtag = DynamicTag.objects.get(pk=1)
        self.assertTrue(True)
    
    def test_update(self):
        """
        Test used to update a DynamicTag object.
        """       
        dtag = DynamicTag.objects.get(pk=1)
        dtag.start = 1000
        dtag.save()
        # check if the dtag has been updated
        dtag = DynamicTag.objects.get(pk=1)     
        self.assertEqual(1000, dtag.start)
    
    def test_delete(self):
        """
        Test used to delete a DynamicTag object.
        """
        dtag = DynamicTag.objects.get(pk=1)
        dtag.delete()
        #check if the dtag has been deleted
        num = DynamicTag.objects.count()
        self.assertEqual(0, num)
