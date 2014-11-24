# This module contains the Celery application instance for this project, 
# we take configuration from Django settings and use autodiscover_tasks to 
# find task modules inside all packages listed in INSTALLED_APPS.

from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jprocessor.settings')

app = Celery('jprocessor')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind = True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
