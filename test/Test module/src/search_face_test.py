import os
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_summarizer import FaceSummarizer
from tools.Utils import * 

rec_file_path = r'C:\Active\Face summarization\Rev229\FPS_6_RES_ORIG_STDMULT_20_CONF_5\MONITOR072011.mpg\Face recognition\MONITOR072011.mpg.YAML'


def compare_segments(train_person_nr, train_segment_nr, query_person_nr, query_segment_nr):

    rec_faces = None
    
    # Try to load YAML file with recognition results
    if(os.path.exists(rec_file_path)):
        
        print 'Loading YAML file with recognition results'
        
        rec_faces = load_YAML_file(rec_file_path)
        
        if(rec_faces):
            
            print 'YAML file with recognition results loaded'
    
            fs = FaceSummarizer()
    
            train_person = rec_faces[train_person_nr]
            
            segments = train_person['segments']
            
            segment_dict = segments[train_segment_nr]
            
            train_model = fs.createFaceModel(segment_dict)
            
            train_hists = train_model.getMatVector("histograms")
            
            query_person = rec_faces[query_person_nr]
            
            segments = query_person['segments']
            
            segment_dict = segments[query_segment_nr]
            
            query_model = fs.createFaceModel(segment_dict)
            
            query_hists = query_model.getMatVector("histograms")
            
            for i in range(0,len(query_hists)):
    
                hist = query_hists[i][0]
                
                # Confidence value
                conf = sys.maxint
                
                print('query', i)
        
                # Iterate through LBP histograms in training model
                for t in range(0, len(train_hists)):
                    
                    print('train', t)
                    
                    train_hist = train_hists[t][0]
                
                    diff = cv2.compareHist(
                    hist, train_hist, cv.CV_COMP_CHISQR)
                    
                    print('diff', diff)
                    
                raw_input("Press Enter to continue...")
                    

compare_segments(6, 0, 6, 1)
