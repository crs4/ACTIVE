from __future__ import absolute_import
import json
import requests
from celery import shared_task
from celery.signals import task_postrun

@shared_task
def callback(ret):
	return ret
	
@task_postrun.connect
def on_task_postrun(signal = None, sender = None, task_id = None, task = None, 
		args = None, kwargs = None, retval = None, state = None):
	if task.name == 'jprocessor.apps.commons.tasks.callback':
		payload = {"task_id":task_id, "task_name":task.name, "state":state, "retval":retval}
		#requests.post("http://156.148.132.83:8000", data = json.dumps(payload))
		print(json.dumps(payload))

