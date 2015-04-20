from django.db import models
from core.tags.models import Entity

"""
Module used to define the data model for people entities.
"""

class Person(Entity):
	"""
	This class extends the Entity class in order to provide
	additional fields for a person.
	This class allow to extend the entities that could occur in
	a digital item.
	"""
	first_name = models.CharField(max_length=100)
	last_name= models.CharField(max_length=100)
	gender = models.CharField(max_length=100, blank=True)
	birth_date = models.DateField(null=True, blank=True)

	def save(self, *args, **kwargs):
		super(Person, self).save(*args, **kwargs)
		self.category = 'Person - ' + self.first_name + ' ' + self.last_name
		super(Person, self).save() 
		
