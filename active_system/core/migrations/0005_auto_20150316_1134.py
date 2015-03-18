# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150316_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='description',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='script',
            name='events',
            field=models.ManyToManyField(to='core.Event'),
            preserve_default=True,
        ),
    ]
