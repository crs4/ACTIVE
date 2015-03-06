from django.test import TestCase
from xmp import xmp_extractor, xmp_embedder

class XMPEmbeddTest(TestCase):
	"""
	Test utilizzato per verificare la corretta inclusione dei
	metadati xmp sui file multimediali considerati.
	"""

	def test_embedding(self):
		filename = "/var/spool/active/data/image.jpg"
		metadata = {}
		metadata["1"] = {}
		metadata["1"]["prefix"] = "prova"
		metadata["1"]["fields"] = {}
		metadata["1"]["fields"]["nome"] = {"is_array":"not_array", "xpath":[], "type":"str",  "value":["TestImage"]}
		metadata["1"]["fields"]["data_creazione"] = {"is_array":"not_array", "xpath":[], "type":"date", "value":["2014-12-03 10:03:19"]}
		metadata["1"]["fields"]["estensione"] = {"is_array":"not_array", "xpath":[], "type":"str",  "value":["png"]}
		result = xmp_embedder.metadata_synch(1, filename, metadata)
		self.assertEqual(result, True)


class XMPExtractTest(TestCase):
	"""
	Test utilizzato per verificare il corretto funzionamento 
	della funzione di estrazione dei metadati da un file multimediale.
	"""
	def test_extraction1(self):
		filename = "/var/spool/active/data/image.jpg"
		metadata = xmp_extractor.extract(filename)
		self.assertEqual(metadata, {})

	def test_extraction2(self):
		filename = "/var/spool/active/data/image.jpg"
		metadata = xmp_extractor.extract(filename)
		self.assertNotEqual(metadata, {})

	def test_extraction3(self):
		filename = "/var/spool/active/data/image.jpg"
		metadata = xmp_extractor.extract(filename)
		self.assertEqual(metadata["1"][2][1], "TestImage")


