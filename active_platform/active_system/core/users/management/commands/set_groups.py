# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module define a custom command used to populate the database with a set of
groups and permissions that can be used to simplify the user management.
"""

from core.users.models import User, Group, Permission, ContentType
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Setup the Group objects and related Permission'

    def handle(self, *args, **options):
        # create and configure the Admin/Contributor/EndUser group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        contr_group, created = Group.objects.get_or_create(name='Contributor')
        user_group, created = Group.objects.get_or_create(name='End User')
        
        # delete all associated permissions
        admin_group.permissions.clear()
        contr_group.permissions.clear()
        user_group.permissions.clear()

        # add all permissions to each group
        for p in Permission.objects.all():
            admin_group.permissions.add(p)

        # remove permissions from some groups
        contr_group.permissions.add(Permission.objects.get(codename='add_item'))
        contr_group.permissions.add(Permission.objects.get(codename='change_item'))
        contr_group.permissions.add(Permission.objects.get(codename='add_audioitem'))
        contr_group.permissions.add(Permission.objects.get(codename='change_audioitem'))
        contr_group.permissions.add(Permission.objects.get(codename='add_imageitem'))
        contr_group.permissions.add(Permission.objects.get(codename='change_imageitem'))
        contr_group.permissions.add(Permission.objects.get(codename='add_videoitem'))
        contr_group.permissions.add(Permission.objects.get(codename='change_videoitem'))
        contr_group.permissions.add(Permission.objects.get(codename='add_tag'))
        contr_group.permissions.add(Permission.objects.get(codename='change_tag'))
        contr_group.permissions.add(Permission.objects.get(codename='delete_tag'))
        contr_group.permissions.add(Permission.objects.get(codename='add_dynamictag'))
        contr_group.permissions.add(Permission.objects.get(codename='change_dynamictag'))
        contr_group.permissions.add(Permission.objects.get(codename='delete_dynamictag'))
        contr_group.permissions.add(Permission.objects.get(codename='add_entity'))
        contr_group.permissions.add(Permission.objects.get(codename='change_entity'))
        contr_group.permissions.add(Permission.objects.get(codename='add_person'))
        contr_group.permissions.add(Permission.objects.get(codename='change_person'))
        contr_group.permissions.add(Permission.objects.get(codename='add_event'))
        contr_group.permissions.add(Permission.objects.get(codename='add_script'))
        contr_group.permissions.add(Permission.objects.get(codename='change_script'))
        contr_group.permissions.add(Permission.objects.get(codename='delete_script'))
        contr_group.permissions.add(Permission.objects.get(codename='add_entitymodel'))
        contr_group.permissions.add(Permission.objects.get(codename='change_entitymodel'))
        contr_group.permissions.add(Permission.objects.get(codename='delete_entitymodel'))
        contr_group.permissions.add(Permission.objects.get(codename='add_instance'))
        contr_group.permissions.add(Permission.objects.get(codename='change_instance'))
        contr_group.permissions.add(Permission.objects.get(codename='delete_instance'))
        contr_group.permissions.add(Permission.objects.get(codename='add_keyword'))

        # save the groups
        admin_group.save()
        contr_group.save()
        user_group.save()
