import yaml
import os
import pickle
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_summarizer import FaceSummarizer


frames_already_saved = False

fs = FaceSummarizer()

resource = r'C:\Active\Mercurial\jprocessor\Video\YouTubeMix.mp4'

if(frames_already_saved):
	
	#fs.resource_name = r'Videolina-2sec.mov'
	
	#fs.resource_name = r'FicMixSegment3'
	
	fs.resource_name = r'FicMixTest1'
	
	fps = 25.0
	
	fs.fps = fps
	
	#frames_path = r'C:\Users\Maurizio\Documents\Face summarization\Videolina-2sec.mov\Frames'
	
	#frames_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Frames'
	
	#frames_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Face tracking\Segments\3'
	
	frames_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixTest1\Frames'
	
	frame_list = []
	
	counter = 0
	
	for frame in os.listdir(frames_path):
		
		complete_path = os.path.join(frames_path, frame)
		
		frame_dict = {}
                    
		frame_dict[FRAME_PATH_KEY] = complete_path
		
		elapsed_s = counter / fps
		
		frame_dict[ELAPSED_VIDEO_TIME_KEY] = elapsed_s
		
		frame_list.append(frame_dict) 
		
		counter = counter + 1
		
	fs.frame_list = frame_list
	
	fs.video_frames = float(counter)
	
else:

	fs.getFrameList(resource)

#file_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Face detection\FicMix.YAML'

#file_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixSegment3\Face detection\FicMixSegment3.YAML'

#file_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixTest1\Frames'

#file_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixTest1\Face detection\FicMixTest1.YAML'

#with open(file_path) as f:
	
#	fs.detected_faces = yaml.load(f) 
	
fs.detectFacesInVideo()		
	
fs.calcHistDiff()

fs.trackFacesInVideo()

fs.saveTrackingSegments()

fs.recognizeFacesInVideo()

fs.saveRecPeople()

fs.showRecPeople()

fs.savePeopleFiles()
