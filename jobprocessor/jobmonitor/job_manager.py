import time
#from time import sleep
from collections import OrderedDict
from multiprocessing.dummy import Pool

"""
Ad ogni utenete is associata una istanza di JobManager.
"""
class JobManager:
	def __init__(self, max_jobs=5):
		# i job vengono memorizzati all'interno di dizionari
		# per semplificare la ricerca basata su id
		self.__queuedJobs    = OrderedDict()
		self.__runningJobs   = OrderedDict()
		self.__failedJobs    = {}
		self.__completedJobs = {}
		self.__max_jobs = max_jobs
		self.__flag = False
		self.__pool = Pool(self.__max_jobs + 1)


	def addJob(self, job):
		# aggiunge il job alla coda di attesa
		self.__queuedJobs[job.id] = job

	def abortJob(self, job_id):
		# prima cerca nella lista dei processi in coda
		# e poi in quella dei processi in esecuzione
		if(self.__queuedJobs[job_id]):
			del self.__queuedJob[job_id]
		elif(self.__runningJobs[job_id]):
			# TODO interrompere il job...
			del self.__runningJobs[job_id]

	def cleanJobs(self):
		# rimuove tutti i job falliti o completati
		self.__failedJobs.clear()
		self.__completedJobs.clear()

        # avvia la gestione automatica della coda di job
	def start(self):
		self.__flag = True
		self.__pool.apply_async(self.__manage)


	# interrompe la gestione automatica della coda
	def stop(self):
		self.__flag = False

	def getAllJobs(self):
		# restituisce un dizionario indicando lo stato di ogni job
		return {"FAILED"   : self.__failedJobs.values(),
			"COMPLETED": self.__completedJobs.values(),
			"RUNNING"  : self.__runningJobs.values(),
			"QUEUED"   : self.__queuedJobs.values()}

	def getJobs(self, status):
		# status assume uno dei sequenti valori ["FAILED", "COMPLETED", "RUNNING", "QUEUED"]
		return self.getAllJobs[status]

	def getJob(self, job_id):
		# cerca in ogni lista il job con l'id specificato
		# se non lo trova restituisce None] 
		job_id = str(job_id)#cast inaspettato: dovrebbe essere una stringa.
		if(job_id in self.__queuedJobs):
			return self.__queuedJobs[job_id]
		elif(job_id in self.__runningJobs):
			return self.__runningJobs[job_id]
		elif(job_id in self.__completedJobs):
			return self.__completedJobs[job_id]
		elif(job_id in self.__failedJobs):
			return self.__failedJobs[job_id]
		else:
			return None

	def __manage(self):
		"""
		funzione utilizzata per gestire in modo automatico la coda di esecuzione dei job
		l'esecuzione avviene in modo costante e puo' essere interrotta tramite un flag booleano
		Si prende un job per volta dalla coda di esecuzione dei job
		Se il job non e' terminato lo reinserisce in fondo alla coda
		Determina in quale coda deve essere aggiunto il job sulla base dello stato di terminazione
		Prende un job in coda e lo mette in esecuzione (se presente)
		TODO: rifare la documentazione		
		"""
		while True:
			# check if job execution has to be ended
			if(not self.__flag):
				break
			
			# if there are enough resources execute some queued jobs (if any)
			while(len(self.__runningJobs) < self.__max_jobs and len(self.__queuedJobs) > 0):
				# get the job object from the returned couple
				job = self.__queuedJobs.popitem(last=False)[1]
				# run a job asynchronously
				job.start_time = int(round(time.time() * 1000))
				self.__runningJobs[job.id] = job
				job.result = self.__pool.apply_async(job.executor, job.args)			
			
			# check the status of the first running job
			if(len(self.__runningJobs) > 0):
				# get the job object from the returned couple
				job = self.__runningJobs.popitem(last=False)[1]
				# if result not ready move the job to the end
				if(not job.result.ready()):
					self.__runningJobs[job.id] = job
				# if job is finished move it in the right list
				else:
					job.end_time = int(round(time.time() * 1000))
					d = self.__failedJobs if job.error_info else self.__completedJobs
					d[job.id] = job

			time.sleep(0.1)
			
