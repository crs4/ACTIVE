from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from core.tags.models import Tag


@receiver(post_delete, sender=Tag)
def tag_post_delete(sender, **kwargs):
    print('Deleted: {}'.format(kwargs['instance'].__dict__))

