
from core.items.models import Item
from core.tags.models import Tag, Entity
from django.contrib.auth.models import User

from core.tags.views import TagList, TagDetail

from django.test import TestCase
from django.test import Client

import json




def create_entity():     
    entity = Entity.objects.create(category = 'test_category')
    return entity

def create_own_item(user):     
    
    item = Item.user_objects.by_user(user).create(filename = 'test', owner = user)    
    return item
    

def create_own_tag(user):
    entity = create_entity()     
    item = create_item(user)
    tag = Tag.user_objects.by_user(user).create(item=item, entity=entity, type='test_type')  
    return tag
    


def create_item(user):     
    
    item = Item.objects.create(filename = 'test', owner = user)    
    return item
    

def create_tag(user):
    entity = create_entity()     
    item = create_item(user)
    tag = Tag.objects.create(item=item, entity=entity, type='test_type')  
    return tag


class EntityTests(TestCase):

    def test_create(self):
        """
        Test used to create and save a fake entity.
        """        
        entity = create_entity()
        self.assertTrue(isinstance(entity, Entity))
        self.assertEqual(1,Entity.objects.count())
        
    def test_get(self):
        """
        Test used to get a fake entity.
        """   
        entity = create_entity()
        entity_retrieved = Entity.objects.filter(pk=entity.pk)        
        self.assertEqual(entity, entity_retrieved[0])
        
    def test_update(self):
        """
        Test used to update fake entity.
        """   
        entity = create_entity()
        entity.category = 'test_updated'
        entity.save()
        entity_retrieved = Entity.objects.filter(pk=entity.pk)     
        self.assertEqual(entity.category, entity_retrieved[0].category)

    def test_delete(self):
        """
        Test used to delete a fake entity.
        """   
        entity = create_entity()
        entity.delete()
        if Entity.objects.filter(pk=entity.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
            


class TagTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='123')
   
    def test_create(self):
        """
        Test used to create and save a fake tag using default Manager.
        """       
        user = User.objects.get(pk = 1)
        tag = create_tag(user)
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(1,Tag.objects.count())
        
    def test_get(self):
        """
        Test used to get a fake tag using default Manager.
        """   
        user = User.objects.get(pk = 1)
        tag = create_tag(user)
        tag_retrieved = Tag.objects.filter(pk=tag.pk)        
        self.assertEqual(tag, tag_retrieved[0])
        
    def test_update(self):
        """
        Test used to update a fake tag using default Manager.
        """       
        user = User.objects.get(pk = 1)    
        tag = create_tag(user)
        tag.type = 'type_updated'
        tag.save()
        tag_retrieved = Tag.objects.filter(pk=tag.pk)     
        self.assertEqual(tag.type, tag_retrieved[0].type)

    def test_delete(self):
        """
        Test used to delete a fake tag using default Manager.
        """   
        user = User.objects.get(pk = 1)
        tag = create_tag(user)
        tag.delete()
        if Tag.objects.filter(pk=tag.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
            
class TagOwnershipTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='123')
    
    def test_create(self):
        """
        Test used to create and save a fake tag using custom Manager.
        """       
        user = User.objects.get(pk = 1) 
        tag = create_own_tag(user)
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(1,Tag.user_objects.by_user(user).count())
        
    def test_get(self):
        """
        Test used to get a fake tag using custom Manager.
        """   
        user = User.objects.get(pk = 1)
        tag = create_own_tag(user)
        tag_retrieved = Tag.user_objects.by_user(user).filter(pk=tag.pk)        
        self.assertEqual(tag, tag_retrieved[0])
        
    def test_update(self):
        """
        Test used to update a fake tag using custom Manager.
        """   
        user = User.objects.get(pk = 1)
        tag = create_own_tag(user)
        tag.type = 'type_updated'
        tag.save()
        tag_retrieved = Tag.user_objects.by_user(user).filter(pk=tag.pk)     
        self.assertEqual(tag.type, tag_retrieved[0].type)

    def test_delete(self):
        """
        Test used to delete a fake tag using custom Manager.
        """   
        user = User.objects.get(pk = 1)
        tag = create_own_tag(user)
        tag.delete()
        if Tag.user_objects.by_user(user).filter(pk=tag.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
      
    #~ def test_tag_list_view(self):
        #~ tag = create_tag()
        #~ resp = self.client.get('/api/tags/')        
        #~ self.assertEqual(resp.status_code, 200)
        #~ self.assertIn(str(tag.id), resp.content)
        #~ 
    #~ def test_tag_post_view(self):
        #~ item = create_item()
        #~ entity = create_entity()
        #~ resp_post = self.client.post('/api/tags/',{'item': item.id, 'entity': entity.id, 'type': 'test_type'})
        #~ print json.loads(resp_post)
        #~ self.assertEqual(resp.status_code, 200)
        #~ self.assertIn(str(tag.id), resp_post.content)
#~ 

            
            
            
            
            
            
            
            
            
            
            
            
        

