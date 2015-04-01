# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_item_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoitem',
            name='frame_rate',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
