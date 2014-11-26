"""
This file contains a set of function ancd classes used to test methods and functionalities provided
bu the data model. Specifically data manipulation functions for Person objects are tested.
"""

from core.models import Person
from django.test import TestCase
import datetime

"""
Global method used to create a new (static) instance of class Person
"""
def create_new_person():
        person = Person()
        person.first_name   = "Billy"
        person.last_name    = "Elliot"
        person.birth_date   = datetime.date.today()
        person.gender       = 'M'
        person.description  = "Dancer"
        return person


"""
Test cases used to check the creation of Person objects
"""
class TestPersonCreate(TestCase):
    """
    Function used to check if data is saved in the db
    """
    def test_create(self):
        # get the total amount of saved objects
        old_num = Person.objects.count()
        person = create_new_person()
        person.save()
        new_num = Person.objects.count()

        # check the number of objects
        self.assertEquals(new_num, old_num+1)

"""
Test cases used to check the search of Person objects
"""
class TestPersonRead(TestCase):
    """
    Function used to create and save a new Person instance in the database
    """
    def setUp(self):
        person = create_new_person()
        person.save()

    """
    Function used to retrieve saved instances
    """
    def test_find(self):
        # retrieve previously saved instance
        count = Person.objects.count()

        # check objects amounts
        self.assertEquals(count, 1)

"""
Test cases used to check the update of Person objects
"""
class TestPersonUpdate(TestCase):
    """
    Function used to create and save a new Person instance in the database
    """
    def setUp(self):
        person = create_new_person()
        person.save()

    """
    Function used to check if Person data has been updated correctely
    """
    def test_update(self):
        # retrieve, edit and save a Person instance
        person = Person.objects.all()[0]
        person.first_name = "Massimiliano"
        person.save()

        # check if instance is update
        self.assertEquals(Person.objects.all()[0].first_name, "Massimiliano")

"""
Test cases used to check the deletion of Person objects
"""
class TestPersonDelete(TestCase):
    """
    Function used to create and save a new Person instance in the database
    """
    def setUp(self):
        person = create_new_person()
        person.save()

    """
    Function used to check if data is removed correctly
    """
    def test_deletePerson(self):
        # retrieve and delete previously saved instance
        person = Person.objects.all()[0]
        person.delete()

        # check if instance has been deleted
        self.assertEquals(Person.objects.count(), 0)