import cachecore as cache
from jprocessor.tools.face_extraction.lib_face_extraction.FaceModelsLBP import FaceModelsLBP

class CacheManager(object):
	
	def __init__(self):
		self.c = cache.FileSystemCache(cache_dir = '/home/federico/workspace-python/cache')
		
	def getCachedModels(self, keyName):
		print("getCachedModels: consume model from cache")
		return self.c.get(keyName)

	def checkCachedModels(self):
		print("FaceModels: read model from disk")
		
		data = self.c.get('faceModels')
		
		if data is None:
			face_models = FaceModelsLBP()
			face_recognizer = face_models.model
			histograms = face_recognizer.getMatVector("histograms")
			labels = face_recognizer.getMat("labels")
			tags = face_models.get_tags()
			
			fm_dict = {}
			fm_dict["histograms"] = histograms
			fm_dict["labels"] = labels	
			fm_dict["tags"] = tags
			
			self.c.set('faceModels', fm_dict)
