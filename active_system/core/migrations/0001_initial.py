# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core.items.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_abs', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActiveUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DynamicTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.BigIntegerField(blank=True)),
                ('duration', models.BigIntegerField(blank=True)),
                ('x_position', models.IntegerField(default=0)),
                ('y_position', models.IntegerField(default=0)),
                ('size_width', models.IntegerField(default=0)),
                ('size_height', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(default=b'N/A', max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('file', models.FileField(null=True, upload_to=core.items.models.compute_upload_path)),
                ('thumb', models.FileField(null=True, upload_to=core.items.models.compute_upload_path)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('frame_width', models.IntegerField(null=True)),
                ('frame_height', models.IntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('core.item',),
        ),
        migrations.CreateModel(
            name='AudioItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('sample_rate', models.IntegerField(null=True)),
                ('bits_per_sample', models.IntegerField(null=True)),
                ('num_channels', models.IntegerField(null=True)),
                ('duration', models.BigIntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('core.item',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Entity')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=('core.entity',),
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('active_version', models.CharField(max_length=10)),
                ('plugin_version', models.CharField(max_length=10)),
                ('url_info', models.CharField(max_length=300)),
                ('authors', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('details', models.CharField(max_length=300)),
                ('path', models.CharField(unique=True, max_length=100)),
                ('job_name', models.CharField(max_length=100)),
                ('item_type', models.CharField(default=b'', max_length=50)),
                ('events', models.ManyToManyField(to='core.Event')),
                ('plugin', models.ForeignKey(to='core.Plugin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, blank=True)),
                ('entity', models.ForeignKey(to='core.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('frame_rate', models.FloatField(null=True)),
                ('frame_width', models.IntegerField(null=True)),
                ('frame_height', models.IntegerField(null=True)),
                ('duration', models.BigIntegerField(null=True)),
                ('format', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=('core.item',),
        ),
        migrations.AddField(
            model_name='tag',
            name='item',
            field=models.ForeignKey(to='core.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dynamictag',
            name='tag',
            field=models.ForeignKey(to='core.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='event',
            field=models.ForeignKey(to='core.Event'),
            preserve_default=True,
        ),
    ]
