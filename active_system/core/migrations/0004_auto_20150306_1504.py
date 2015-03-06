# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_audiovideoitem_imageitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AudioVideoItem',
            new_name='AudioItem',
        ),
    ]
