# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150316_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioitem',
            name='bitrate',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audioitem',
            name='duration',
            field=models.BigIntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audioitem',
            name='format',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='format',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='frame_height',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='frame_width',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
