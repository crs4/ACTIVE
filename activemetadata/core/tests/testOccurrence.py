"""
This file contains all functions needed to check the correct behavior of the functionalities developed
for Occurrence class. Specifically it contains test cases needed to check data manipulations functons.
"""

from core.models import Person, Item, Occurrence
from django.test import TestCase
import datetime

"""
Global method used to create a new instance of class Person
"""
def create_new_person():
        person = Person()
        person.first_name   = "Billy"
        person.last_name    = "Ballo"
        person.birth_date   = datetime.date.today()
        person.gender       = 'M'
        person.description  = ""
        return person

"""
Global method used to create a new instance of class Item
"""
def create_new_item():
        item = Item()
        item.name       = "Video 1"
        item.path       = "/home/user/documentario.mpeg"
        item.metadata   = "MPEG 2 Video ..."
        return item

"""
Global method used to create a new instance of class Occurence
"""
def create_new_occurrence(person, item):
        occurrence = Occurrence()
        person.save()
        item.save()
        occurrence.person       = person
        occurrence.item         = item
        # set where person has been detected
        occurrence.position_x   = 50
        occurrence.position_y   = 100
        occurrence.position_height = 60
        occurrence.position_width  = 90
        # set when person has been detected
        occurrence.start_time   = 3600000
        occurrence.length       = 1000
        return occurrence


"""
Test cases used to check the creation of Occurrence objects
"""
class TestOccurrenceCreate(TestCase):
    """
    Method used to check if data is saved in the db
    """
    def test_createOccurrence(self):
        # get the total amount of saved objects
        old_num = Occurrence.objects.count()
        # create a new instance of Occurrence class
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()
        # get the new total amount of objects
        new_num = Occurrence.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

"""
Test case used to check the search of Occurrence object in a database.
"""
class TestOccurrenceRead(TestCase):
    """
    Function used to create a new instance of occurrence
    """
    def setUp(self):
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

    """
    Method used to check if data is retrieved correctly
    """
    def test_readOccurrence(self):
        # retrieve previously saved instance
        count = Occurrence.objects.count()

        # check objects amount
        self.assertEquals(count, 1)

"""
Test case used to check if data is update correctely in the database
"""
class TestItemUpdate(TestCase):
    """
    Function used to create a new instance of occurrence
    """
    def setUp(self):
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

    """
    Method used to check if data is updated correctely
    """
    def test_editOccurrence(self):
        # retrieve, edit and save previously instance
        occurrence = Occurrence.objects.all()[0]
        occurrence.position_x = 100
        occurrence.save()

        # check if instance has been edited correctely
        self.assertEquals(Occurrence.objects.all()[0].position_x, 100)

"""
Test case used to check if Occurrence data has been deleted from the database
"""
class TestItemDelete(TestCase):
    """
    Function used to create a new instance of occurrence
    """
    def setUp(self):
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

    """
    Method used to check if data is removed correctly
    """
    def test_deleteOccurrence(self):
        # retrieve and delete previously saved instance
        occurrence = Occurrence.objects.all()[0]
        occurrence.delete()

        # check if instance has been deleted
        self.assertEquals(Occurrence.objects.count(), 0)