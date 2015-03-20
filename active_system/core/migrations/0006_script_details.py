# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150316_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='details',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
