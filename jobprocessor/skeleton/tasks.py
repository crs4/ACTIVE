from __future__ import absolute_import
from jobprocessor.celery import app

"""
This module is used to define a generic evaluator function for sequential skeletons.
This function is a Clelery task that will be instantiated and executed remotely 
in some cluster node.
Actually distributed evaluation is available only for sequential skeletons.
"""
# wrapper function necessary to execute tasks through celery
# TO DO:Estendere valutazione distribuita degli skeleton, non solo sequenziali?
@app.task(max_retries = 3, default_retry_delay = 60)
def eval_distributed(skeleton, values):
	"""
	:param skeleton: Sequential skeleton contining the function to compute
			in a distributed way with provided arguments.
	:parms values: Input data for the computation.
	"""
	try:
		return skeleton.execute(values)
	except Exception as ex:
		raise eval_distributed.retry(ex=ex, countdown=5)
