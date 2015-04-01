# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150319_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='thumb',
            field=models.FileField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
