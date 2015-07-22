"""
Module used to test the internal API for the image item module.
It is possibile to check if it is possible to create, update, retrieve and
delete ImageItem objects.
Moreover it is possible to check if the custom object manager works correctely.
"""

from core.items.image.models import ImageItem
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User


def create_item(user_id=1):        
    """
    Method used to create and return a simple ImageItem object.
    """     
    item = ImageItem()
    item.filename = "sample.mp4"
    item.owner = User.objects.get(pk=user_id)
    item.save()
    return item



class ImageItemTests(TestCase):
    """
    Test suite used to check if ImageItem objects are corretely stored in the database.
    """
    def setUp(self):
        """
        Method used to init the test database.
        It creates a new User with id 1.
        """
        user = User.objects.create_user(username="prostomia", password="1234")

    def test_create(self):
        """
        Test used to create and save a simple ImageItem object.
        """
        create_item()
        self.assertTrue(1, ImageItem.objects.count())
        
    def test_get(self):
        """
        Test used to create and retrieve a simple ImageItem object.
        """
        item = create_item()
        item_retrieved = ImageItem.objects.filter(pk=item.pk)[0]        
        self.assertEqual(item.id, item_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic ImageItem object.
        """
        item = create_item()

        item.filename = 'sample2.mp4'
        item.save()

        item_retrieved = ImageItem.objects.filter(pk=item.pk)[0]
        self.assertEqual(item.filename, item_retrieved.filename)

    def test_delete(self):
        """
        Test used to create and retrieve a simple ImageItem object.
        """
        item = create_item()
        item.delete()
        self.assertEqual(0, ImageItem.objects.count())
        

class ImageItemOwnershipTests(TestCase):
    """
    Test suite used to check if the custom object manager is able to detect
    correctely the ImageItem object ownership. So different ImageItem objects are created and
    then retrieved based on User objects.
    """

    def setUp(self):
        """
        Method used to init the test database.
        It creates two User object with id 1 and 2.
        """
        user1 = User.objects.create_user(username="prostomia", password="1234")
        user2 = User.objects.create_user(username="antani",    password="4321")
    

    def test_create(self):
        """
        Test used to create and save a simple ImageItem object.
        """
        create_item()
        self.assertTrue(1, ImageItem.user_objects.by_user(1).count())
        
    def test_get(self):
        """
        Test used to create and retrieve a simple ImageItem object.
        """
        item = create_item()
        item_retrieved = ImageItem.user_objects.by_user(1).filter(pk=item.pk)[0]        
        self.assertEqual(item.id, item_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic ImageItem object.
        """
        item = create_item()

        item.filename = 'sample2.mp4'
        item.save()

        item_retrieved = ImageItem.user_objects.by_user(1).filter(pk=item.pk)[0]
        self.assertEqual(item.filename, item_retrieved.filename)

    def test_delete(self):
        """
        Test used to create and retrieve a simple ImageItem object.
        """
        item = create_item()
        item.delete()
        self.assertEqual(0, ImageItem.user_objects.by_user(1).count())

    def test_ownership_get(self):
        """
        Test used to create and retrieve a simple ImageItem object by user id.
        """
        item = create_item(user_id=1)
        self.assertEqual(1, ImageItem.user_objects.by_user(1).count())

    def test_ownership_get2(self):
        """
        Test used to create and retrieve many ImageItem objects by user id.
        """
        for i in range(10):
            create_item(user_id=1)
        self.assertEqual(10, ImageItem.user_objects.by_user(1).count())
    
    def test_ownership_get3(self):
        """
        Test used to create and retrieve ImageItem objects from different users.
        """
        for i in range(5):
            create_item(user_id=1)
        for i in range(3):
            create_item(user_id=2)
        
        self.assertEqual(5, ImageItem.user_objects.by_user(1).count())
        self.assertEqual(3, ImageItem.user_objects.by_user(2).count())
   
    def test_ownership_get4(self):
        """
        Test used to check if a user is able to access to other user ImageItem objects.
        """
        for i in range(10):
            create_item(user_id=1)
        
        self.assertEqual(0, ImageItem.user_objects.by_user(2).count())
        self.assertEqual(0, ImageItem.user_objects.by_user(2).filter(pk=3).count())
        
