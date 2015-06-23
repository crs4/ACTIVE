from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class ACTIVEUser(models.Model):
    """
    Class created only for migration purposes.
    """
    role = models.CharField(max_length = 300)
