# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_script_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plugin',
            name='job_name',
        ),
        migrations.AddField(
            model_name='script',
            name='job_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
