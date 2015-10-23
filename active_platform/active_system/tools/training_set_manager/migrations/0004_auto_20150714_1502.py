# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tools.training_set_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0003_auto_20150714_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitymodel',
            name='model_file',
            field=models.FileField(null=True, upload_to=tools.training_set_manager.models.models_upload_path, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='features',
            field=models.FileField(null=True, upload_to=tools.training_set_manager.models.instances_upload_path, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='thumbnail',
            field=models.FileField(default=b'image.jpg', null=True, upload_to=tools.training_set_manager.models.instances_upload_path, blank=True),
            preserve_default=True,
        ),
    ]
