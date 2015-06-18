# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('frame_width', models.IntegerField(null=True, blank=True)),
                ('frame_height', models.IntegerField(null=True, blank=True)),
                ('format', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
    ]
