# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20150318_0857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videoitem',
            old_name='bitrate',
            new_name='frame_rate',
        ),
        migrations.AlterField(
            model_name='item',
            name='filesize',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
    ]
