# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tools.training_set_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0004_auto_20150714_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitymodel',
            name='name',
            field=models.CharField(default='Standard model', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entitymodel',
            name='last_update',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='thumbnail',
            field=models.FileField(null=True, upload_to=tools.training_set_manager.models.instances_upload_path, blank=True),
            preserve_default=True,
        ),
    ]
