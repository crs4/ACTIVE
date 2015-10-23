# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.items.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, blank=True)),
                ('mime_type', models.CharField(max_length=100, blank=True)),
                ('filename', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('filesize', models.CharField(max_length=10, blank=True)),
                ('visibility', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=core.items.models.compute_upload_path, blank=True)),
                ('thumb', models.FileField(null=True, upload_to=core.items.models.compute_upload_path, blank=True)),
                ('preview', models.FileField(null=True, upload_to=core.items.models.compute_upload_path, blank=True)),
                ('state', models.CharField(default=b'STORED', max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('frame_width', models.IntegerField(null=True)),
                ('frame_height', models.IntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='AudioItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('sample_rate', models.IntegerField(null=True)),
                ('bits_per_sample', models.IntegerField(null=True)),
                ('num_channels', models.IntegerField(null=True)),
                ('duration', models.BigIntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='items.Item')),
                ('frame_rate', models.FloatField(null=True)),
                ('frame_width', models.IntegerField(null=True)),
                ('frame_height', models.IntegerField(null=True)),
                ('duration', models.BigIntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('items.item',),
        ),
    ]
