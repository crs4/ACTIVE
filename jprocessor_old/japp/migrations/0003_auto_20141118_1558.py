# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('japp', '0002_auto_20141117_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='duration',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='resource',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
