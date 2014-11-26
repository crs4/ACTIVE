import os
import shutil

orig_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\VidTIMIT-Originale'
audio_training_set_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\VidTIMIT\Audio\Training set'
audio_test_set_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\VidTIMIT\Audio\Test set'
video_training_set_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\VidTIMIT\Video-1fps\Training set'
video_test_set_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\Dataset\VidTIMIT\Video-1fps\Test set'

training_item_nr_per_person = 6
video_fps = 25
used_fps = 1

# Delete files in output paths
for directory in os.listdir(audio_training_set_path):
    dir_complete_path = os.path.join(audio_training_set_path, directory)
    shutil.rmtree(dir_complete_path)
    
for directory in os.listdir(audio_test_set_path):
    dir_complete_path = os.path.join(audio_test_set_path, directory)
    shutil.rmtree(dir_complete_path)
    
for directory in os.listdir(video_training_set_path):
    dir_complete_path = os.path.join(video_training_set_path, directory)
    shutil.rmtree(dir_complete_path)
    
for directory in os.listdir(video_test_set_path):
    dir_complete_path = os.path.join(video_test_set_path, directory)
    shutil.rmtree(dir_complete_path)  
   
# Create training and test set for audio
print '\n### Creating training and test set for audio ###\n'
for directory in os.listdir(orig_path):
    
    print 'Creating training and test set for', directory
    training_audio_files_path = os.path.join(audio_training_set_path, directory)
    os.makedirs(training_audio_files_path)
    test_audio_files_path = os.path.join(audio_test_set_path, directory)
    os.makedirs(test_audio_files_path)
    
    dir_complete_path = os.path.join(orig_path, directory)
    person_dir = os.path.join(dir_complete_path, directory)
    all_audio_files_dir = os.path.join(person_dir, 'audio')
    counter = 1
    for audio_dir in os.listdir(all_audio_files_dir):
            
        audio_path = os.path.join(all_audio_files_dir, audio_dir)
        new_audio_path = os.path.join(training_audio_files_path, audio_dir)
        
        if(counter > training_item_nr_per_person):
            # Audio must be used in test set
            new_audio_path = os.path.join(test_audio_files_path, audio_dir)
        
        shutil.copy(audio_path, new_audio_path)
        
        counter = counter + 1
    
# Create training and test set for video
print '\n### Creating training and test set for video ###\n'
for directory in os.listdir(orig_path):
    
    print 'Creating training and test set for', directory
    training_video_files_path = os.path.join(video_training_set_path, directory)
    os.makedirs(training_video_files_path)
    test_video_files_path = os.path.join(video_test_set_path, directory)
    os.makedirs(test_video_files_path)
    
    dir_complete_path = os.path.join(orig_path, directory)
    person_dir = os.path.join(dir_complete_path, directory)
    all_video_files_dir = os.path.join(person_dir, 'video')
    counter = 1
    for video_dir in os.listdir(all_video_files_dir):
        
        if(video_dir[0:4] != 'head'): # Discard head rotation videos
            
            video_path = os.path.join(all_video_files_dir, video_dir)
            new_video_path = training_video_files_path
            
            if(counter > training_item_nr_per_person):
                # Video must be used in test set
                new_video_path = os.path.join(test_video_files_path, video_dir)
                os.makedirs(new_video_path)
                
            frame_counter = 0
            last_saved_frame = 0
            for frame in os.listdir(video_path):
				
				# Next frame to be saved
                next_frame = last_saved_frame + (video_fps/used_fps)
                
                if(frame_counter > next_frame):
				
					frame_path = os.path.join(video_path, frame)
					new_frame_name = video_dir + '-' + frame
					new_frame_path = os.path.join(new_video_path, new_frame_name)
					shutil.copy(frame_path, new_frame_path)
					last_saved_frame = frame_counter
                
                frame_counter = frame_counter + 1
                
            counter = counter + 1
    
    
    
