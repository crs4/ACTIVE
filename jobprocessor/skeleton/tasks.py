from __future__ import absolute_import
from jobprocessor.celery import app


### private wrapper functions necessary to define tasks through celery
# TO DO:Estendere valutazione distribuita degli skeleton, non solo sequenziali
@app.task
def eval_distributed(skeleton, values):
	return skeleton.execute(values)

