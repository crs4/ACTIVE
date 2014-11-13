import os
import pickle
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_summarizer import FaceSummarizer

fs = FaceSummarizer()

#resource = r'C:\Active\RawVideos\videolina-3sec.mov'

#resource = r'C:\Active\RawVideos\FicTrackingTest1.mp4'

#resource = r'C:\Active\RawVideos\Videolina-mezzo_sec.mp4'

resource = r'C:\Active\RawVideos\FicMix2sec.mp4'

#fs.resource_name = r'FicTrackingTest1.mp4'

fs.getFrameList(resource)

fs.detectFacesInVideo()

#file_name = fs.resource_name + '.pickle'

#file_path = os.path.join(FACE_DETECTION_PATH, file_name)

#with open(file_path) as f:
	
	#fs.detected_faces = pickle.load(f) 

fs.trackFacesInVideo()

fs.recognizeFacesInVideo()

fs.saveTrackingSegments()
