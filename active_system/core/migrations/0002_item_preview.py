# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.items.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='preview',
            field=models.FileField(null=True, upload_to=core.items.models.compute_upload_path),
            preserve_default=True,
        ),
    ]
