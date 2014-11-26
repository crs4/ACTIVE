"""
This files is used to check all functions defined for Item class.
Specifically it is used to test manipulation functionalities.
"""

from core.models import Item
from django.test import TestCase


"""
Global method used to create a new (static) instance of class Item
"""
def create_new_item():
        item = Item()
        item.name       = "Video 1"
        item.path       = "/home/user/documentario.mpeg"
        item.metadata   = "MPEG 2 Video ..."
        return item



"""
Test cases used to check the the creation of an Item object
"""
class TestItemCreate(TestCase):
    """
    Function used to check if data is saved in the database
    """
    def test_createItem(self):
        # get the total amount of saved objects
        old_num = Item.objects.count()
        # create a new instance of Person
        item = create_new_item()
        item.save()
        # get the new amount of saved objects
        new_num = Item.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

"""
Test case used to check the search of an Item object
"""
class TestItemRead(TestCase):
    """
    Function used to create and save a new Item object in the database
    """
    def setUp(self):
        item = create_new_item()
        item.save()

    """
    Method used to check if data is retrieved correctly from the database
    """
    def test_readItem(self):
        # retrieve previously saved instance
        count = Item.objects.count()

        # check objects amounts
        self.assertEquals(count, 1)

"""
Test case used to check if data is updated correctely
"""
class TestItemUpdate(TestCase):
    """
    Function used to create and save a new Item object in the database
    """
    def setUp(self):
        item = create_new_item()
        item.save()

    """
    Function used to check if data is updated correctely in the db
    """
    def test_editItem(self):
        # retrieve, edit and save previously instance
        item = Item.objects.all()[0]
        item.name = "Video_01"
        item.save()

        # check if instance has been edited
        self.assertEquals(Item.objects.all()[0].name, "Video_01")

"""
Test case used to check if Item objects are correctely remove from the database
"""
class TestItemDelete(TestCase):
    """
    Function used to create and save a new Item object in the database
    """
    def setUp(self):
        item = create_new_item()
        item.save()

    """
    Method used to check if data is removed correctly from the db
    """
    def test_deleteItem(self):
        # retrieve and delete previously saved instance
        item = Item.objects.all()[0]
        item.delete()

        # check if instance has been deleted
        self.assertEquals(Item.objects.count(), 0)