from django.test import TestCase
from face_extraction.pipe import *
		
class TestFunctional(TestCase):
	
	def test_face_extraction(self):
		resource_path = '/var/spool/active/data/videolina-10sec.mov'
		face_extraction(resource_path)
