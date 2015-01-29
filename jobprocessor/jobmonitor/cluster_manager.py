from abc import ABCMeta, abstractmethod
from jobprocessor.celery import app

class ClusterManager:
	__metaclass__ = ABCMeta

	@abstractmethod	
	def start(self):
		pass

	@abstractmethod	
	def stop(self):
		pass

	@abstractmethod	
	def restart(self):
		pass

class CeleryManager(ClusterManager):

	def start(self):# TO DO
		print("... What the fuck!!!")

	def stop(self):
		app.control.broadcast("shutdown")

	def restart(self):
		app.control.broadcast("pool_restart", arguments = {'reload': True})

