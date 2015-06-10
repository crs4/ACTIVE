# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_item_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Entity')),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('core.entity',),
        ),
    ]
