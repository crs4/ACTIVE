import yaml

import os

old_path = r'F:\Face summarization\6 fps - res originale - std mult 10 - conf 4\MONITOR072011.mp4\Simple annotations_old'

new_path = r'F:\Face summarization\6 fps - res originale - std mult 10 - conf 4\MONITOR072011.mp4\Simple annotations'

for file_name in os.listdir(old_path):
            
    old_file_path = os.path.join(old_path, file_name)
    
    with open(old_file_path) as f:
    
        old_person_dict = yaml.load(f)
        
        new_person_dict = {}
        
        new_person_dict['ann_tag'] = old_person_dict['ann_tag']
        
        old_segments = old_person_dict['segments']
        
        new_segments = []
        
        tot_duration = 0
        
        for old_segment in old_segments:
            
            old_duration = old_segment['segment_duration']
            
            start = old_segment['segment_start']
            
            new_duration = old_duration * 25.0 / 6.0
            
            new_segment = {}
            
            new_segment['segment_duration'] = new_duration
            
            new_segment['segment_start'] = start
            
            new_segments.append(new_segment)
            
            tot_duration = tot_duration + new_duration
            
        new_person_dict['segments'] = new_segments
        
        new_person_dict['tot_segments_duration'] = tot_duration
        
        new_file_path = os.path.join(new_path, file_name)
        
        with open(new_file_path, 'w') as stream:
            
            stream.write(yaml.dump(new_person_dict, default_flow_style = False))
         
