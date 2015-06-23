# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='description',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
