# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('japp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='title',
        ),
        migrations.AddField(
            model_name='job',
            name='data',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='resource',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
    ]
