# This module contains the Celery application instance for this project. 
# We take configuration from settings module and use autodiscover_tasks to 
# find task modules inside all packages listed in APPS.

from __future__ import absolute_import
from celery import Celery
from jprocessor.settings import APPS

app = Celery('jprocessor')
app.config_from_object('jprocessor.settings')
app.autodiscover_tasks(lambda: APPS)

