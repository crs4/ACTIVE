# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0002_auto_20150714_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='thumbnail',
            field=models.FileField(default=b'image.jpg', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
