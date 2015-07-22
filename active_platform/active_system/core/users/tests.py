from django.test import TestCase

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password

# Create your tests here.

def create_permission():
    permission = Permission()
    permission.name = 'Do stuff'
    permission.codename = 'Can do stuff'
    permission.content_type = {}
    return permission

def create_group():
    group = Group()
    group.name = 'GruppoTogo'
    #group.permissions.add([])
    return group

def create_user():
    user = User()
    user.first_name = 'Ciccio'
    user.last_name = 'Panda'
    user.username = 'ciccio'
    user.password = make_password('ciccio')
    #user.groups.add([])
    #user.user_permissions.add([])
    return user

class TestModelUser(TestCase):

    def test_create_user(self):
        user = create_user()
        user.save()
        self.assertEqual(User.objects.count(), 1)
        user.delete()
        
    def test_read_user(self):
        user = create_user()
        user.save()
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.id, 1)
        user.delete()

    def test_update_user(self):
        user = create_user()
        user.save()
        user.first_name = 'Lillo'
        user.save()
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.first_name, 'Lillo')
        user.delete()

    def test_delete_user(self):
        user = create_user()
        user.save()
        self.assertEqual(User.objects.count(), 1)
        user.delete()
        self.assertEqual(User.objects.count(), 0)

"""
class TestApiUser(TestCase):

    def test_create_user(self):
        response = self.client.post('/api/users/users/', {
            'first_name':'Ciccio', 
            'last_name':'Panda', 
            'username':'ciccio', 
            'password':'ciccio', 
            'groups':[], 
            'user_permissions':[]}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_read_user(self):
        response = self.client.get('/api/users/users/1/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

class TestModelGroup(TestCase):

    def test_create_group(self):
        group = create_group()
        group.save()
        self.asserEqual(Group.objects.count(), 1)
        group.delete()

    def test_read_group(self):
        group = create_group()
        group.save()
        group = Group.objects.get(pk=group.id)
        self.assertEqual(group.name, 'GruppoTogo')
        group.delete()

    def test_update_group(self):
        group = create_group()
        group.save()
        group.name = 'GruppoMenoTogo'
        group.save()
        group = Group.objects.get(pk=group.id)
        self.assertEqual(group.name, 'GruppoMenoTogo')
        group.delete()

    def test_delete_group(self):
        group = create_group()
        group.save()
        self.asserEqual(Group.objects.count(), 1)
        group.delete()
        self.asserEqual(Group.objects.count(), 0)
"""
