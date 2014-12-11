from __future__ import absolute_import
from celery import shared_task, chain
from celery.signals import task_postrun
import time

"""
Questo file contiene i task di esempio dell'applicazione fittizia utilizzata per testare il corretto funzionamento
dei diversi moduli che costituiscono il JobProcessor e per fornire un esempio su come strutturare un'applicazione
che utilizza i task celery per effettuare le computazioni parallele.
Prima vengono definiti i singoli task logici da eseguire e successivamente vengono definiti i workflow, ossia come
sono organizzati questi task tra di loro.
NB: poiche' i task vengono invocati attraverso l'API RESt fornita da Flower e' consigliabile effettuare esplicitamente
il casting per ciascuno dei parametri di input che vengono passati ai task dalla pipeline (stringa per default)
"""


############### Funzioni corrispondenti ai task di base
@shared_task
def add(x, y):
	""" Task di esempio che effettua una somma """
	print("Somma dei valori %s %s" % (x, y))
	time.sleep(5)		# latenza che simula una computazione
	return x + y

@shared_task
def increase(z):
	""" Task di esempio che incrementa di uno la computazione """
	print("Incremento del valore %s" % z)
	time.sleep(5)		# latenza che simula una computazione
	return z + 1



############### Funzioni che definiscono come sono organizzati i task precedenti
@shared_task
def workflow_sync(x, y):
	""" Workflow di esempio che combina i task definiti in modo sequenziale """
	z = add(int(x), int(y))
	res = increase(int(z))
	return res
	
@shared_task
def workflow(x, y):
	""" Workflow di esempio che combina i task definiti in modo sequenziale e asincrono """
	wf = (add.s() | increase.s())	# costruisce la pipeline di task
	res = wf.delay(int(x), int(y))	# invoca l'esecuzione asincrona del workflow
	return res			# restitusce l'id del task che calcolera' il risultato complessivo
