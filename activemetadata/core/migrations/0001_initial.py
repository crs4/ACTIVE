# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
                ('metadata', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_x', models.PositiveIntegerField()),
                ('position_y', models.PositiveIntegerField()),
                ('position_width', models.PositiveIntegerField()),
                ('position_height', models.PositiveIntegerField()),
                ('start_time', models.TimeField(verbose_name=b'Occurrence start')),
                ('length', models.TimeField(verbose_name=b'Occurence duration')),
                ('item', models.ForeignKey(to='core.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=3, choices=[('M', 'Male'), ('F', 'Female')])),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='person',
            field=models.ForeignKey(to='core.Person'),
            preserve_default=True,
        ),
    ]
