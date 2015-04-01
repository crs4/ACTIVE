from django.test import TestCase
from django.contrib.auth.models import User,UserManager
from core.users.models import ActiveUser

# This file has been created in order to detect if all
# provided functionalities work properly.


def create_user(username, passwd=None, fst_name='', lst_name='', email='', role='EndUser'):
	# create a standard Django user
	user = User.objects.create_user(username, password=passwd, first_name=fst_name, last_name=lst_name, email=email)
	# create a platform user
        active_user = ActiveUser()
        active_user.user = user
        active_user.role = role
        active_user.save()
	return active_user

class BasicUserTests(TestCase):
	def test_create(self):
		""" Test used to create and save a fake platform user. """
		create_user("user", "user", role='Contributor')
		self.assertEqual(1, ActiveUser.objects.count())

	def test_get(self):
		""" Test used to retrieve a user previously saved. """
                temp = create_user("user1", "user1", role='Contributor')
		temp = create_user("user2", "user2", role='EndUser')
		user =  ActiveUser.objects.get(pk=temp.id) 
                self.assertEqual('EndUser', user.role)

	def test_update(self):
		""" Test used to edit some user attributes. """
                user = create_user("user1", "user1", role='Contributor')
                user.role = "EndUser"
		user.save()
		user =  ActiveUser.objects.get(pk=user.id)
                self.assertEqual('EndUser', user.role)

	def test_delete(self):
		""" Test used to delete an existing user. """
		user1 = create_user("user1", "user1", role='Contributor')
                user2 = create_user("user2", "user2", role='EndUser')
		user1.delete()
		self.assertEqual(1, ActiveUser.objects.count())

	def test_list(self):
		""" Test used to retrieve all stored users. """
                temp = create_user("user1", "user1", role='Contributor')
                temp = create_user("user2", "user2", role='EndUser')
                self.assertEqual(2, ActiveUser.objects.count())



# TODO inserire dei test piu' avanzati sulle funzionalita' ad esempio:
# - fare delle chiamate all'API del sistema
# - invocare le viste definiti per gli utenti
# - verificare la presenza dei permessi

