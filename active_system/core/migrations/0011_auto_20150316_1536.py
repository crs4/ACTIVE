# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150316_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoitem',
            name='bitrate',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
    ]
