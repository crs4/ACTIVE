from django.test import TestCase
from celery import group, chain
from tasks import increase_task, multiply_task

class SimpleTest(TestCase):
	def test_1(self):
		print "Incrementa 30 numeri interi individualmente"
		res = group(increase_task.s(i) for i in xrange(30)).delay()
		res.get()

	def task_2(self):
		print "Incrementa e raddoppia 20 numeri interi a gruppi di 2"
		res = (increase_task.s() | multiply.s()).chunks(zip(xrange(20)), 10).group().delay()
		res.get()
