# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password

def create_permission():
    permission = Permission()
    permission.name = 'Do stuff'
    permission.codename = 'Can do stuff'
    permission.content_type = {}
    return permission

def create_group():
    group = Group()
    group.name = 'GruppoTogo'
    return group

def create_user():
    user = User()
    user.first_name = 'Ciccio'
    user.last_name = 'Panda'
    user.username = 'ciccio'
    user.password = make_password('ciccio')
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
