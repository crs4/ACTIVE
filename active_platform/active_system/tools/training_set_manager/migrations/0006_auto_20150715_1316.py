# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_set_manager', '0005_auto_20150715_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitymodel',
            name='name',
            field=models.CharField(default=b'Generic Entity model', max_length=300),
            preserve_default=True,
        ),
    ]
