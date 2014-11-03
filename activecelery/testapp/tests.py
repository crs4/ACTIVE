"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from testapp.tasks import *


class TaskTest(TestCase):
		
	def test_video(self):
		video_action_task.delay()
        
	def test_image(self):
		image_action_task.delay()
        
	def test_sound(self):
		sound_action_task.delay()
		
	def test_chunk_check_prime(self):
		x = 80
		job = check_prime.chunks(zip(range(2, x+1)), 10)
		job.apply_async()

		
