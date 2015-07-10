# reference to the main celery instance
from __future__ import absolute_import
from job_processor.celery import app


"""
This module is used to define a generic evaluator function for sequential skeletons.
This function is a Celery task that will be instantiated and executed remotely 
in some cluster node.
Actually distributed evaluation is available only for sequential skeletons.
"""

# wrapper function necessary to execute tasks through celery
@app.task
def eval_distributed(skeleton, values):
	"""
	@param skeleton: Sequential skeleton contining the function to compute in a distributed way with provided arguments.
	@type skeleton: Seq
	@param values: Input data for the computation.
	@type values: List of objects
	@return: The result of Seq skeleton evaluation.
	@rtype: Object
	"""
	return skeleton.execute(values)
