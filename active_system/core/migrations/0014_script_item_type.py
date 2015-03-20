# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='item_type',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
