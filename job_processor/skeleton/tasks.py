"""
This module is used to define a generic evaluator function for sequential skeletons.
This function is a Celery task that will be instantiated and executed remotely 
in some cluster node.
Actually distributed evaluation is available only for sequential skeletons.
"""

from __future__ import absolute_import
from job_processor.celery import app

# wrapper function necessary to execute tasks through Celery
@app.task
def eval_distributed(skeleton, *args):
	"""
	@param skeleton: Sequential skeleton contining the function to compute in a distributed way with provided arguments.
	@type skeleton: Seq
	@param args: Input data for the computation.
	@type args: Tuple of objects
	@return: The result of Seq skeleton evaluation.
	@rtype: Object
	"""
	return apply(skeleton.execute, args)
