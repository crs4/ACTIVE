# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0002_auto_20150922_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='event',
        ),
        migrations.AddField(
            model_name='action',
            name='events',
            field=models.ManyToManyField(to='plugins.Event'),
            preserve_default=True,
        ),
    ]
