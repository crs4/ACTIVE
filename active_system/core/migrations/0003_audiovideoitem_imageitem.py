# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150306_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioVideoItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('bitrate', models.IntegerField()),
                ('duration', models.BigIntegerField()),
                ('format', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('core.item',),
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('frame_width', models.IntegerField()),
                ('frame_height', models.IntegerField()),
                ('format', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('core.item',),
        ),
    ]
