# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_item_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audioitem',
            name='format',
        ),
        migrations.RemoveField(
            model_name='imageitem',
            name='format',
        ),
        migrations.RemoveField(
            model_name='videoitem',
            name='format',
        ),
    ]
