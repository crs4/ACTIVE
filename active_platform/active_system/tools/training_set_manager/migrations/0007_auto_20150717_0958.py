# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tools.training_set_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0006_auto_20150715_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='thumbnail',
            field=models.FileField(default=b'thumbnails/generic_file.jpeg', null=True, upload_to=tools.training_set_manager.models.instances_upload_path, blank=True),
            preserve_default=True,
        ),
    ]