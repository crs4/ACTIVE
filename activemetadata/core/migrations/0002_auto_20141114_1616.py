# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='length',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='position_height',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='position_width',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='position_x',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='position_y',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='start_time',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
    ]
