from jprocessor.tools.face_extraction.lib_face_extraction.FaceModelsLBP import FaceModelsLBP

class CacheManager(object):
	
	def getCachedModels(self, keyName):
		
		print("getCachedModels: consume model from cache")
			
		return cache.get(keyName)
	
	
	def checkFaceModels(self):
		
		data = cache.get('faceModels')

		if data is None:
			
			print("checkFaceModels: consume model from disk")
			
			face_models = FaceModelsLBP()

			face_recognizer = face_models.model

			histograms = face_recognizer.getMatVector("histograms")
			
			labels = face_recognizer.getMat("labels")
			
			tags = face_models.get_tags()
				
			fm_dict = {}
			
			fm_dict["histograms"] = histograms

			fm_dict["labels"] = labels
			
			fm_dict["tags"] = tags
				
			cache.set('faceModels', fm_dict)
