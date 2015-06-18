# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.tags.person.models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
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
                ('tag', models.ForeignKey(to='tags.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tags.Entity')),
                ('description', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=('tags.entity',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tags.Entity')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('image', models.FileField(default=b'person/unknown_user.png', null=True, upload_to=core.tags.person.models.compute_upload_path, blank=True)),
            ],
            options={
            },
            bases=('tags.entity',),
        ),
    ]
