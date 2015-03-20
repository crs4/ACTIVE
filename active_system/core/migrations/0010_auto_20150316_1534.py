# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150316_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoitem',
            name='bitrate',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
