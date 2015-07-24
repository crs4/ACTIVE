"""
Module used to test the internal API for the video item module.
It is possibile to check if it is possible to create, update, retrieve and
delete VideoItem objects.
Moreover it is possible to check if the custom object manager works correctely.
"""

from core.items.video.models import VideoItem
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User


def create_item(user_id=1):        
    """
    Method used to create and return a simple VideoItem object.
    """     
    item = VideoItem()
    item.filename = "sample.mp4"
    item.owner = User.objects.get(pk=user_id)
    item.save()
    return item



class VideoItemTests(TestCase):
    """
    Test suite used to check if VideoItem objects are corretely stored in the database.
    """
    def setUp(self):
        """
        Method used to init the test database.
        It creates a new User with id 1.
        """
        user = User.objects.create_user(username="prostomia", password="1234")

    def test_create(self):
        """
        Test used to create and save a simple VideoItem object.
        """
        create_item()
        self.assertTrue(1, VideoItem.objects.count())
        
    def test_get(self):
        """
        Test used to create and retrieve a simple VideoItem object.
        """
        item = create_item()
        item_retrieved = VideoItem.objects.filter(pk=item.pk)[0]        
        self.assertEqual(item.id, item_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic VideoItem object.
        """
        item = create_item()

        item.filename = 'sample2.mp4'
        item.save()

        item_retrieved = VideoItem.objects.filter(pk=item.pk)[0]
        self.assertEqual(item.filename, item_retrieved.filename)

    def test_delete(self):
        """
        Test used to create and retrieve a simple VideoItem object.
        """
        item = create_item()
        item.delete()
        self.assertEqual(0, VideoItem.objects.count())
        

class VideoItemOwnershipTests(TestCase):
    """
    Test suite used to check if the custom object manager is able to detect
    correctely the VideoItem object ownership. So different VideoItem objects are created and
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
        Test used to create and save a simple VideoItem object.
        """
        create_item()
        self.assertTrue(1, VideoItem.user_objects.by_user(1).count())
        
    def test_get(self):
        """
        Test used to create and retrieve a simple VideoItem object.
        """
        item = create_item()
        item_retrieved = VideoItem.user_objects.by_user(1).filter(pk=item.pk)[0]        
        self.assertEqual(item.id, item_retrieved.id)
        
    def test_update(self):
        """
        Test used to update the fields of a generic VideoItem object.
        """
        item = create_item()

        item.filename = 'sample2.mp4'
        item.save()

        item_retrieved = VideoItem.user_objects.by_user(1).filter(pk=item.pk)[0]
        self.assertEqual(item.filename, item_retrieved.filename)

    def test_delete(self):
        """
        Test used to create and retrieve a simple VideoItem object.
        """
        item = create_item()
        item.delete()
        self.assertEqual(0, VideoItem.user_objects.by_user(1).count())

    def test_ownership_get(self):
        """
        Test used to create and retrieve a simple VideoItem object by user id.
        """
        item = create_item(user_id=1)
        self.assertEqual(1, VideoItem.user_objects.by_user(1).count())

    def test_ownership_get2(self):
        """
        Test used to create and retrieve many VideoItem objects by user id.
        """
        for i in range(10):
            create_item(user_id=1)
        self.assertEqual(10, VideoItem.user_objects.by_user(1).count())
    
    def test_ownership_get3(self):
        """
        Test used to create and retrieve VideoItem objects from different users.
        """
        for i in range(5):
            create_item(user_id=1)
        for i in range(3):
            create_item(user_id=2)
        
        self.assertEqual(5, VideoItem.user_objects.by_user(1).count())
        self.assertEqual(3, VideoItem.user_objects.by_user(2).count())
   
    def test_ownership_get4(self):
        """
        Test used to check if a user is able to access to other user VideoItem objects.
        """
        for i in range(10):
            create_item(user_id=1)
        
        self.assertEqual(0, VideoItem.user_objects.by_user(2).count())
        self.assertEqual(0, VideoItem.user_objects.by_user(2).filter(pk=3).count())
        
