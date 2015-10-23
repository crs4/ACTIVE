# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '__first__'),
        ('items', '0002_item_owner'),
        ('training_set_manager', '0007_auto_20150717_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='dtag',
            field=models.ForeignKey(default=1, to='tags.DynamicTag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instance',
            name='item',
            field=models.ForeignKey(default=1, to='items.Item'),
            preserve_default=False,
        ),
    ]
