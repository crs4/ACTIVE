from __future__ import absolute_import
from jobprocessor.celery import app
from time import sleep

def increase(x):
	sleep(6)
	return x + 1

def multiply(x):
	return x + 1

@app.task
def increase_task(x):
	return increase(x)

@app.task
def multiply_task(x):
	return multiply(x)

@app.task
def pipeline_task(x):
	return multiply(increase(x))
