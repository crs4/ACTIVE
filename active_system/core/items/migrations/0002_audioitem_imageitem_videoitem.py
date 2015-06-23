# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('sample_rate', models.IntegerField(null=True, blank=True)),
                ('bits_per_sample', models.IntegerField(null=True, blank=True)),
                ('num_channels', models.IntegerField(null=True, blank=True)),
                ('duration', models.BigIntegerField(null=True, blank=True)),
                ('format', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
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
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('frame_rate', models.FloatField(null=True, blank=True)),
                ('frame_width', models.IntegerField(null=True, blank=True)),
                ('frame_height', models.IntegerField(null=True, blank=True)),
                ('duration', models.BigIntegerField(null=True, blank=True)),
                ('format', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
    ]
