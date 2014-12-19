import numpy
import os
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_summarizer import FaceSummarizer
from tools.Utils import * 


man_ann_path = r'C:\Active\Face summarization\Annotations\fic.02'

#resource_path = r''

#fs = FaceSummarizer()

#fs.analizeVideo(resource_path)

## Get name of resource
#res_name = os.path.basename(resource_path) 
res_name = 'fic.02.mpg'

## Directory for this video     
video_path = os.path.join(FACE_SUMMARIZATION_PATH, res_name)

## Directory with simple annotations
simple_ann_path = os.path.join(video_path, FACE_SIMPLE_ANNOTATION_DIR)

# Get tags by analyzing folder with annotation files

people_precision_dict = {}
people_recall_dict = {}
tags = []
for ann_file in os.listdir(man_ann_path):
    
    tag = os.path.splitext(ann_file) [0]
    tags.append(tag)
    
    people_precision_dict[tag] = 0
    people_recall_dict[tag] = 0   


### Calculate recall ###

video_tot_rec = 0
video_tot_duration = 0

# Iterate through manual annotations
for ann_file in os.listdir(man_ann_path):
    
    ann_path = os.path.join(man_ann_path, ann_file)
    
    man_dict = load_YAML_file(ann_path)
    
    tot_duration = man_dict[TOT_SEGMENT_DURATION_KEY]
    
    video_tot_duration = video_tot_duration + tot_duration
    
    man_tag = man_dict[ANN_TAG_KEY]
    
    man_segments = man_dict[SEGMENTS_KEY]
    
    rec = 0.0 # Correctly recognized video (in milliseconds)
    
    auto_ann_file = os.path.join(simple_ann_path, ann_file)
        
    if(not(os.path.exists(auto_ann_file))):
        
        print(auto_ann_file)
        error_str = ('Warning! Automatic annotation for ' + 
        ann_file + ' does not exist')
         
        print error_str
        continue
    
    auto_dict = load_YAML_file(auto_ann_file)
    
    auto_tag = auto_dict[ANN_TAG_KEY]
    
    if(man_tag != auto_tag):
        
        print 'Warning! Tags are different!'
        
        break
    
    for man_segment in man_segments:
        
        man_start = man_segment[SEGMENT_START_KEY]
        
        man_duration = man_segment[SEGMENT_DURATION_KEY]
        
        man_end = man_start + man_duration
        
        # Check if there is a segment in automatic annotations 
        # that corresponds to this segment 
            
        auto_segments = auto_dict[SEGMENTS_KEY]
        
        for auto_segment in auto_segments:
            
            auto_start = auto_segment[SEGMENT_START_KEY]
            
            auto_duration = auto_segment[SEGMENT_DURATION_KEY]
            
            auto_end = auto_start + auto_duration
            
            # Real segment is smaller than automatic segment
            if((man_start >= auto_start) and (man_end <= auto_end)):
                
                # Whole real segment is correctly recognized
                rec = rec + man_duration
            
            # Real segment is bigger than automatic segment
            elif((man_start <= auto_start) and (man_end >= auto_end)):
            
                # Whole automatic segment is correctly recognized
                rec = rec + auto_duration
            
            # Real segment starts before automatic segment
            elif((man_start <= auto_start) and (man_end >= auto_start)):
                
                # Both automatic and real segments are 
                # partially correctly recognized
                rec = rec + (man_end - auto_start)
            
            # Real segment starts after automatic segment
            elif((man_start <= auto_end) and (man_end >= auto_end)):
                
                # Both automatic and real segments are 
                # partially correctly recognized
                rec = rec + (auto_end - man_start)   
    
    recall = rec / tot_duration     
                
    people_recall_dict[man_tag] = rec / tot_duration
    
    video_tot_rec = video_tot_rec + rec
    
tot_recall = video_tot_rec / video_tot_duration    

### Calculate precision ###

video_tot_rec = 0
video_tot_duration = 0

# Iterate through automatic annotations
for ann_file in os.listdir(simple_ann_path):
    
    ann_path = os.path.join(simple_ann_path, ann_file)
    
    auto_dict = load_YAML_file(ann_path)
    
    auto_tag = auto_dict[ANN_TAG_KEY]
    
    auto_segments = auto_dict[SEGMENTS_KEY]
    
    rec = 0.0 # Correctly recognized video (in milliseconds)
    
    man_ann_file = os.path.join(man_ann_path, ann_file)
        
    man_dict = load_YAML_file(man_ann_file)
    
    man_tag = man_dict[ANN_TAG_KEY]
    
    if(man_tag != auto_tag):
        
        print 'Warning! Tags are different!'
        
        break
    
    for auto_segment in auto_segments:
        
        auto_start = auto_segment[SEGMENT_START_KEY]
        
        auto_duration = auto_segment[SEGMENT_DURATION_KEY]
        
        auto_end = auto_start + auto_duration
        
        # In manual annotation, we consider as start previous second
        # and as end subsequent second
        
        auto_start = math.ceil(auto_start / 1000.0) * 1000
        
        auto_end = math.floor(auto_end / 1000.0) * 1000
        
        auto_duration = auto_end - auto_start
        
        if(auto_duration < 0):
            
            print(auto_start)
            print(auto_end)
            print(auto_segment)
            print(auto_tag)
            
            print 'Warning! Duration is less than zero'
        
        # Check if there is a segment in manual annotations 
        # that corresponds to this segment 
            
        man_segments = man_dict[SEGMENTS_KEY]
        
        for man_segment in man_segments:
            
            man_start = man_segment[SEGMENT_START_KEY]
            
            man_duration = man_segment[SEGMENT_DURATION_KEY]
            
            man_end = man_start + man_duration  
            
            # Real segment is smaller than automatic segment
            if((man_start >= auto_start) and (man_end <= auto_end)):
                
                # Whole real segment is correctly recognized
                rec = rec + man_duration
            
            # Real segment is bigger than automatic segment
            elif((man_start <= auto_start) and (man_end >= auto_end)):
            
                # Whole automatic segment is correctly recognized
                rec = rec + auto_duration
            
            # Real segment starts before automatic segment
            elif((man_start <= auto_start) and (man_end >= auto_start)):
                
                # Both automatic and real segments are 
                # partially correctly recognized
                rec = rec + (man_end - auto_start)
            
            # Real segment starts after automatic segment
            elif((man_start <= auto_end) and (man_end >= auto_end)):
                
                # Both automatic and real segments are 
                # partially correctly recognized
                rec = rec + (auto_end - man_start)
                
    tot_duration = auto_dict[TOT_SEGMENT_DURATION_KEY]
    
    precision = rec / tot_duration      
                
    people_precision_dict[auto_tag] = rec / tot_duration
    
    video_tot_rec = video_tot_rec + rec
    
    video_tot_duration = video_tot_duration + tot_duration
    
tot_precision = video_tot_rec / video_tot_duration 

tot_f1 = 2 * (tot_precision * tot_recall) / (tot_precision + tot_recall)
    
# Calculate statistics for each person
people_precision_list = []
people_recall_list = []
people_f1_list = []

for tag in tags:

    person_precision = people_precision_dict[tag]
    people_precision_list.append(person_precision)
    
    person_recall = people_recall_dict[tag]
    people_recall_list.append(person_recall)

    person_f1 = 0;
    if((person_precision != 0) and (person_recall != 0)):
        person_f1 = 2 * (person_precision * person_recall) / (person_precision + person_recall)
    people_f1_list.append(person_f1)   
    

mean_precision = float(numpy.mean(people_precision_list))
std_precision = float(numpy.std(people_precision_list))

mean_recall = float(numpy.mean(people_recall_list))
std_recall = float(numpy.std(people_recall_list))

mean_f1 = float(numpy.mean(people_f1_list))
std_f1 = float(numpy.std(people_f1_list))

print("\n ### RESULTS ###\n")

print('Tot precision: ' + str(tot_precision))
print('Tot recall: ' + str(tot_recall))
print('Tot f1: ' + str(tot_f1))

print('Mean of precision: ' + str(mean_precision))
print('Standard deviation of precision: ' + str(std_precision))
print('Mean of recall: ' + str(mean_recall))
print('Standard deviation of recall: ' + str(std_recall))
print('Mean of f1: ' + str(mean_f1))
print('Standard deviation of f1: ' + str(std_f1))
