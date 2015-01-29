import uuid
import time

class Job:
	def __init__(self, func, args, name="job"):
		self.id = str(uuid.uuid4())
		self.args = args 
		self.executor = func #args['executor']
		self.result = None # wrapper del risultato asincrono della computazione
		self.percentage = None
		self.start_time = None
		self.end_time = None
		self.name = name #args['name']
		self.error_info = None

	def __unicode__(self):
		return self.id

	def __repr__(self):
		return self.id

	def __str__(self):
		return self.id

	def duration(self):
		if(self.end_time):
			return self.end_time - self.start_time
		return int(round(time.time()*1000)) - self.start_time

	def set_start_end(self):
		if(self.start_time):
			self.end_time = int(round(time.time()*1000))
		else: self.start_time = int(round(time.time()*1000))
		
