# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0008_auto_20150928_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='dtag',
            field=models.ForeignKey(blank=True, to='tags.DynamicTag', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='item',
            field=models.ForeignKey(blank=True, to='items.Item', null=True),
            preserve_default=True,
        ),
    ]
