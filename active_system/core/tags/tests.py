
from core.items.models import Item
from core.tags.models import Tag, Entity

from core.tags.views import TagList, TagDetail

from django.test import TestCase
from django.test import Client

import json



def create_entity():     
    entity = Entity.objects.create(category = 'test_category')
    entity.save()
    return entity
    

def create_item():     
    item = Item.objects.create(filename = 'test')
    item.save()
    return item
    

def create_tag():     
    item = create_item()
    entity = create_entity()    
    tag = Tag.objects.create(item=item, entity=entity, type='test_type')
    tag.save()
    return tag



class EntityTests(TestCase):

    def test_create(self):
        """
        Test used to create and save a fake item.
        """        
        entity = create_entity()
        self.assertTrue(isinstance(entity, Entity))
        self.assertEqual(1,Entity.objects.count())
        
    def test_get(self):
        entity = create_entity()
        entity_retrieved = Entity.objects.filter(pk=entity.pk)        
        self.assertEqual(entity, entity_retrieved[0])
        
    def test_update(self):
        entity = create_entity()
        entity.category = 'test_updated'
        entity.save()
        entity_retrieved = Entity.objects.filter(pk=entity.pk)     
        self.assertEqual(entity.category, entity_retrieved[0].category)

    def test_delete(self):
        entity = create_entity()
        entity.delete()
        if Entity.objects.filter(pk=entity.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
            


class TagTests(TestCase):

    def test_create(self):
        """
        Test used to create and save a fake item.
        """        
        tag = create_tag()
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(1,Tag.objects.count())
        
    def test_get(self):
        tag = create_tag()
        tag_retrieved = Tag.objects.filter(pk=tag.pk)        
        self.assertEqual(tag, tag_retrieved[0])
        
    def test_update(self):
        tag = create_tag()
        tag.type = 'type_updated'
        tag.save()
        tag_retrieved = Tag.objects.filter(pk=tag.pk)     
        self.assertEqual(tag.type, tag_retrieved[0].type)

    def test_delete(self):
        tag = create_tag()
        tag.delete()
        if Tag.objects.filter(pk=tag.pk):
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            
    def test_tag_list_view(self):
        tag = create_tag()
        resp = self.client.get('/api/tags/')        
        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(tag.id), resp.content)
        
    def _test_tag_post_view(self):
        item = create_item()
        entity = create_entity()
        resp_post = self.client.post('/api/tags/',{'item': item.id, 'entity': entity.id, 'type': 'test_type'})
        print json.loads(resp_post)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(tag.id), resp_post.content)


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            #~ 
            #~ 
        #~ 
  #~ w = self.create_item()
            #~ url = reverse("whatever.views.whatever")
            #~ resp = self.client.get(url)
            #~ self.assertEqual(resp.status_code, 200)
            #~ self.assertIn(w.title, resp.content)
       #~ 
#~ 
#~ 
        #~ 

        

