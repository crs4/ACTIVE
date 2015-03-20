# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150318_1434'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='View',
            new_name='Action',
        ),
    ]
