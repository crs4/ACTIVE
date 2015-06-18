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
                ('state', models.CharField(default=b'', max_length=300, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
