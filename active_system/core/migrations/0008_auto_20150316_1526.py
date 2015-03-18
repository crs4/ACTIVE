# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150316_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='filesize',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='bitrate',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='duration',
            field=models.BigIntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='format',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='frame_height',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='frame_width',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
