from __future__ import absolute_import
from celery import shared_task, chain
from celery.signals import task_postrun
from xmp import xmp_extractor
from xmp import xmp_embedder
import json
import requests

"""
One-shot tasks.
All following tasks are executed in order to complete a process.
Each task corresponds to a step of a complex computation that could be parallelized.
"""

@shared_task
def callback(ret):
	"""
	Callback task used to synchronize workflow execution.
	This task simply return the computation result. In case of asynchronous computation
	the task id of last computed/istantiated task is returned.
	"""
	return ret
	
@task_postrun.connect
def on_task_postrun(signal = None, sender = None, task_id = None, task = None, 
		args = None, kwargs = None, retval = None, state = None):
	"""
	This function is a side-effect that is called/executed each time a task is
	completed. Inside this function it is possibile to personalize the execution
	based on the executed task name
	"""
	if task.name == 'xmp.tasks.callback':
		payload = {"task_id":task_id, "task_name":task.name, "state":state, "retval":retval}
		#requests.post("http://156.148.132.83:8000", data = json.dumps(payload))
		print(json.dumps(payload))



###### migliorare i nomi dei task e dei workflow in modo da evitare la presenza di ripetizioni o incomprensioni

@shared_task
def extract_xmp(file_path):
	"""
	Task used to call a function capable to extract XMP metadata from a file.

	param: file_path: Absolute file path that refers to the considered file.
	type: file_path: str
	"""
	return xmp_extractor.extract(file_path)
    
@shared_task
def embed_xmp(component_id, component_path, changes):
	"""
	Task used to call a function capable to embed XMP metadata inside a file.

	param: component_id: Identifier of the item that will be modified
	type: component_id: int
	param: component_path: Absolut path of the item that will be modified
	type: component_path: str
	param: changes: Dictionary containing XMP metadata to write in the correct format
	type: chaanges: dict
	"""
	return xmp_embedder.metadata_synch(component_id, component_path, changes)


"""
Workflows - pipes and chunks.
Following tasks has been created in order to define/organize parallel computations.
Celery primitives could be used to define where and how parallelism occurs.
"""

@shared_task
def task_extract_xmp(resource_path):
	"""
	This task describe how to configure the parallel execution for
	XMP metadata extraction from a specific multimedia file.
	A callback task is used to provide a side-effect mechanism.

	:param resource_path: Absolute path for the multimedia file that will be considered.
	:type resource_path: str
	"""
	job = (extract_xmp.s(resource_path) | callback.s())
	return job.apply_async()

@shared_task
def task_embed_xmp(component_id, component_path, changes):
	"""
	This task describe how to configure the parallel execution for
	XMP metadata embedding from a specific multimedia file.
	A callback task is used to provide a side-effect mechanism.

	:param component_id: Id of the multimedia file to consider
	:type component_id: int
	:param component_path: Aboslute path for the file that will be modified
	:type component_path: str
	:param changes: Dictionary containing XMP metadata that will be applied to the file
	:type changes: dict
	"""
	job = (embed_xmp.s(component_id, component_path, changes) | callback.s())
	return job.apply_async()
