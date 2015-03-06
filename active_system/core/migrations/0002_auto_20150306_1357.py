# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='path',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='', max_length=300, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='file',
            field=models.FileField(default=None, upload_to=b''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='filesize',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
