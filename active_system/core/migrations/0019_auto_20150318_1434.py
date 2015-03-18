# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150318_0932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audioitem',
            old_name='bitrate',
            new_name='bits_per_sample',
        ),
        migrations.AddField(
            model_name='audioitem',
            name='num_channels',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audioitem',
            name='sample_rate',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
