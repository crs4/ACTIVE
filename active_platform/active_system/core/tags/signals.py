# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from core.tags.models import Tag


@receiver(post_delete, sender=Tag)
def tag_post_delete(sender, **kwargs):
    print('Deleted: {}'.format(kwargs['instance'].__dict__))

