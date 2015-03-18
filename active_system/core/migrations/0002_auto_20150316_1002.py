# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioitem',
            name='bitrate',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='audioitem',
            name='duration',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='audioitem',
            name='format',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='format',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='frame_height',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='frame_width',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='bitrate',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='duration',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='format',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='frame_height',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='frame_width',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
