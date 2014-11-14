from django.test import TestCase
import datetime
from core.models import Person, Item, Occurrence

######## global functions ########################

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
        #occurrence.start_time   = datetime.timedelta(hours=1, minutes=30)
        #occurrence.length       = datetime.timedelta(milliseconds=600000)
        return occurrence

######## test units ##############################

"""
Test cases used to check the CRUD operations for Person objects
"""
class TestPerson(TestCase):
    """
    Method used to check if data is saved in the db
    """
    def test_createPerson(self):
        # create a new instance of Person
        person = create_new_person()

        # get the total amount of saved objects
        old_num = Person.objects.count()
        person.save()
        new_num = Person.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

    """
    Method used to check if data is retrieved correctly from the db
    """
    def test_findPerson(self):
        # save a new instance of Person
        person = create_new_person()
        person.save()

        # retrieve previously saved instance
        person2 = Person.objects.all()[0]

        # check objects ids
        self.assertEquals(person, person2)

    """
    Method used to check if data is updated correctely in the db
    """
    def test_editPerson(self):
        # save a new instance of Person
        person = create_new_person()
        person.save()

        # retrieve, edit and save previously instance
        person2 = Person.objects.filter(first_name="Billy").all()[0]
        person2.first_name = "Massimiliano"
        person2.save()

        # check if instance has been deleted
        self.assertEquals(Person.objects.all()[0].first_name, "Massimiliano")

    """
    Method used to check if data is removed correctly from the db
    """
    def test_deletePerson(self):
        # save a new instance of Person
        person = create_new_person()
        person.save()

        # retrieve and delete previously saved instance
        person2 = Person.objects.filter(first_name="Billy").all()[0]
        person2.delete()

        # check if instance has been deleted
        self.assertEquals(Person.objects.count(), 0)

"""
Test cases used to check the CRUD operations for Item objects
"""
class TestItem(TestCase):
    """
    Method used to check if data is saved in the db
    """
    def test_createItem(self):
        # create a new instance of Person
        item = create_new_item()

        # get the total amount of saved objects
        old_num = Item.objects.count()
        item.save()
        new_num = Item.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

    """
    Method used to check if data is retrieved correctly from the db
    """
    def test_findItem(self):
        # save a new instance of Person
        item = create_new_item()
        item.save()

        # retrieve previously saved instance
        item2 = Item.objects.all()[0]

        # check objects ids
        self.assertEquals(item, item2)

    """
    Method used to check if data is updated correctely in the db
    """
    def test_editItem(self):
        # save a new instance of Item
        item = create_new_item()
        item.save()

        # retrieve, edit and save previously instance
        item2 = Item.objects.filter(name="Video 1").all()[0]
        item2.name = "Video_01"
        item2.save()

        # check if instance has been edited
        self.assertEquals(Item.objects.all()[0].name, "Video_01")

    """
    Method used to check if data is removed correctly from the db
    """
    def test_deleteItem(self):
        # save a new instance of Item
        item = create_new_item()
        item.save()

        # retrieve and delete previously saved instance
        item2 = Item.objects.filter(name="Video 1").all()[0]
        item2.delete()

        # check if instance has been deleted
        self.assertEquals(Item.objects.count(), 0)

"""
Test cases used to check the CRUD operations for Occurrence objects
"""
class TestOccurrence(TestCase):
    """
    Method used to check if data is saved in the db
    """
    def test_createOccurrence(self):
        # create a new instance of Occurrence class
        occurrence = create_new_occurrence(create_new_person(), create_new_item())

        # get the total amount of saved objects
        old_num = Occurrence.objects.count()
        occurrence.save()
        new_num = Occurrence.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

    """
    Method used to check if data is retrieved correctly from the db
    """
    def test_findOccurrence(self):
        # save a new instance of Occurrence
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

        # retrieve previously saved instance
        occurrence2 = Occurrence.objects.all()[0]

        # check objects ids
        self.assertEquals(occurrence, occurrence2)

    """
    Method used to check if data is updated correctely in the db
    """
    def test_editOccurrence(self):
        # save a new instance of Occurrence
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

        # retrieve, edit and save previously instance
        occurrence2 = Occurrence.objects.filter(item__name="Video 1").all()[0]
        occurrence2.position_x = 100
        occurrence2.save()

        # check if instance has been edited
        self.assertEquals(Occurrence.objects.all()[0].position_x, 100)

    """
    Method used to check if data is removed correctly from the db
    """
    def test_deleteOccurrence(self):
        # save a new instance of Occurrence
        occurrence = create_new_occurrence(create_new_person(), create_new_item())
        occurrence.save()

        # retrieve and delete previously saved instance
        occurrence2 = Occurrence.objects.filter(person__first_name="Billy").all()[0]
        occurrence2.delete()

        # check if instance has been deleted
        self.assertEquals(Occurrence.objects.count(), 0)