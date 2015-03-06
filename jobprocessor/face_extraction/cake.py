from django.core.cache import cache
from face_extraction.libs.FaceModelsLBP import FaceModelsLBP

class CacheManager(object):
   
    def checkCachedModels(self, keyName):
        data = cache.get(keyName)

        if data is None:
            print("checkCachedModels:consume from disk")
            face_models = FaceModelsLBP()
            face_recognizer = face_models.model
            histograms = face_recognizer.getMatVector("histograms")       
            labels = face_recognizer.getMat("labels")
            tags = face_models.get_tags()              
            fm_dict = {}       
            fm_dict["histograms"] = histograms
            fm_dict["labels"] = labels
            fm_dict["tags"] = tags
            cache.set(keyName, fm_dict)
            return cache.get(keyName)
            
        print("checkCachedModels:consume from cache")
        return data
