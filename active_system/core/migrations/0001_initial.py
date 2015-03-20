# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('filename', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('filesize', models.IntegerField(default=0, null=True)),
                ('visibility', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
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
        migrations.CreateModel(
            name='AudioItem',
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
            name='Plugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('path', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('active_version', models.CharField(max_length=10)),
                ('plugin_version', models.CharField(max_length=10)),
                ('job_main', models.CharField(max_length=100)),
                ('url_info', models.CharField(max_length=300)),
                ('authors', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Item')),
                ('bitrate', models.IntegerField()),
                ('frame_width', models.IntegerField()),
                ('frame_height', models.IntegerField()),
                ('duration', models.BigIntegerField()),
                ('format', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('core.item',),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_abs', models.CharField(max_length=300)),
                ('event', models.ForeignKey(to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
