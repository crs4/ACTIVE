from core.items.models import Item
from django.core.files import File
from django.test import TestCase



def create_item(filename):        
    
    item = None
    #~ with open('/var/spool/active/data/tests/file.png', 'r') as f:      
        #~ item = Item.objects.create(filename = filename, file = File(f))
        #~ item = Item()
        #~ item.filename = "lillo"
        #~ item.save()
        #~ 
    #~ f.close()        
        
    item = Item()
    item.filename = "lillo"
    item.save()
    return item



class ItemTests(TestCase):

    def test_create(self):
        """
        Test used to create and save a fake item.
        """
        
        item = create_item('test')
        self.assertTrue(isinstance(item, Item))
        
    def test_get(self):
        item = create_item('test')        
        item_retrieved = Item.objects.filter(pk=item.pk)        
        self.assertEqual(item, item_retrieved[0])
        
    def test_update(self):
        item = create_item('test')
        item.filename = 'test_updated'
        item.save()
        item_retrieved = Item.objects.filter(pk=item.pk)     
        self.assertEqual(item.filename, item_retrieved[0].filename)
        
    #~ def test_delete(self):
        #~ item = create_item('test')
        #~ item.delete()
        #~ self.assertIsNone(Item.objects.filter(pk=item.pk))
        
 
        #~ def test_item_list_view(self):
            #~ w = self.create_item()
            #~ url = reverse("whatever.views.whatever")
            #~ resp = self.client.get(url)
            #~ self.assertEqual(resp.status_code, 200)
            #~ self.assertIn(w.title, resp.content)



        

        
