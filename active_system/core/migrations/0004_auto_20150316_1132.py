# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150316_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=100)),
                ('plugin', models.ForeignKey(to='core.Plugin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='description',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='events',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='path',
        ),
    ]
