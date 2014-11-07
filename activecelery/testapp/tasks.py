from __future__ import absolute_import

from celery import shared_task
	
@shared_task
def video_action_task():
	return 'video action task'
	
@shared_task
def image_action_task():
	return 'image action task'
	
@shared_task
def sound_action_task():
	return 'sound action task'
	
@shared_task
def check_prime(num):
	return all(num % i for i in xrange(2, num))																				

