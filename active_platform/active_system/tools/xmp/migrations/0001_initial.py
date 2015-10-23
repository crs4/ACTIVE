# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_item_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='XMPMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.CharField(max_length=1000)),
                ('item', models.ForeignKey(to='items.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
