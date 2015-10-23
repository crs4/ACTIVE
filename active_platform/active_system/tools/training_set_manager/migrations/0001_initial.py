# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('last_update', models.DateTimeField()),
                ('entity', models.ForeignKey(to='tags.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thumbnail', models.FileField(default=b'image.jpg', upload_to=b'')),
                ('features', models.FileField(upload_to=b'')),
                ('trusted', models.BooleanField()),
                ('type', models.CharField(max_length=50)),
                ('entity_model', models.ForeignKey(blank=True, to='training_set_manager.EntityModel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
