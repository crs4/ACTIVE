from django.db import models
from django.contrib.auth.models import User


class ActiveUser(models.Model):
	"""
	This model has beed defined in order to manage all
	different types of users.
	It extends the Django user model, adding some fields.
	"""
	
	user  = models.ForeignKey(User)
	role  = models.CharField(max_length=100, blank=False)

	def __repr__(self):
        	print 'User: ', self.username, " - ", self.role

	def get_username(self):
		"""
		Method used to obtain a string which identifies the user.
		@returns: Unique username for the user.
		"""
		return self.user.username

	def get_full_name(self):
		"""
		Wrapper method used to obtain the user's full name.
		@returns: The name of the user.
		"""
		return self.user.get_full_name()

	def get_role(self):
		"""
		Method used to return the platform user's role.
		@returns: Users's role.
		"""
		return self.role

	def set_full_name(self, first_name, last_name):
		"""
		Method used to edit the user full name.
		@param first_name: User's first name
		@param last_name: User's last name
		"""
		self.user.first_name = first_name
		self.user.last_name = last_name

	def set_role(self, role):
                """
                Method used to set the platform user's role.
		@param role: Role that will be applied to the user.
                """
                self.role = role

