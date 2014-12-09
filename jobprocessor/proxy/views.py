"""
All'interno di questo modulo sono state riportate tutte le 
funzioni che vengono invocate dal proxi attraverso l'API REST fornita dal
Job Processor.
Dato che il Job Processor nella versione corrente utilizza RabbitMQ e Celery per
gestire ed eseguire i task mentre utilizza l'API REST di Flower per avviare alcune 
funzionalita' di base del sistema, il job processor sviluppato non a' altro che un
proxy ad alcune delle operazioni messe a disposizione da flower, con la differenza
che e' possibile personalizzare il funzionamento di quest'ultimo.
"""

from django.shortcuts import render
from django.http import HttpResponse, QueryDict
import requests # da non confondere con il parametro request delle viste!
import json
import time


################## Funzioni che interrogano direttamente le API REST di Flower
FLOWER_ENDPOINT = 'http://localhost:5555/'	# TODO spostare nei parametri di configurazione

def start_async_task(name, params):
	""" Avvia un task asincrono attraverso l'API di Flower """
	# ottiene l'id del task iniziale che e' stato avviato
	url = FLOWER_ENDPOINT + 'api/task/send-task/' + name
	payload = json.dumps({'kwargs' : params})
	response = requests.post(url, data=payload)
	return response.content

def stop_async_task(task_id):
	""" Interrompe un task asincrono tramite l'API di Flower """
	url = FLOWER_ENDPOINT + "api/task/revoke/" + task_id
	response = requests.post(url, params={"terminate" : True})
	return response

def result_async_task(task_id):
	""" Ottiene il risultato di un task asincrono tramite l'API di Flower """
	# ottiene l'id del task che calcola i risultati
	url = FLOWER_ENDPOINT + 'api/task/info/' + task_id
	response = requests.get(url)
	task_id = json.loads(response.text)['result'][15:-2]
	
	# aspetta che la computazione sia terminata (deadlock possibile?)
	result = None
	while True:
		# effettua la chiamata all'API di Flower
		url = FLOWER_ENDPOINT + 'api/task/info/' + task_id
		response = requests.get(url)
		result = json.loads(response.text)['result']
		if result is not None :
			result = result[1:-1]	# rimuove gli apici che racchiudono il risultato (stringa)
			break
		time.sleep(1)
	return json.dumps(result)



############### Viste che vengono utilizzate per fornire l'API REST delle funzioni precedenti 
def view_start_task(request):
	""" Vista utilizzata per avviare l'esecuzione asincrona di un task """
	task_name = request.GET.get('name', '0')
	task_params = request.GET.dict()
	if task_name != '0' :
		del task_params['name']
	response = start_async_task(task_name, task_params)
	return HttpResponse(response)

def view_stop_task(request):
	""" Vista utilizzata per interrompere l'esecuzione di un task """
	task_id = request.GET.get('id', '0')
	response = stop_async_task(task_id)
	return HttpResponse(response)

def view_result_task(request):
	"""
	Vista utilizzata per ottenere il risultato di una computazione asincrona (generata un'attesa bloccante).
	NB: utilizzare le callback associata a ciascun task per gestire i risultati delle computazioni.
	"""
	task_id = request.GET.get('id', '0')
	response = result_async_task(task_id)
	return HttpResponse(response)

