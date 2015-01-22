# This module contains the Celery application instance for this project. 
# We take configuration from settings module and use autodiscover_tasks to 
# find task modules inside all packages listed in the DJANGO_APPS variable.

from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobprocessor.settings')

app = Celery('jobprocessor')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

