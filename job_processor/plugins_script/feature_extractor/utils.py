from django.conf import settings
import requests
import subprocess
import time

def extract_video_data(func_in, func_out):
	
	res = subprocess.check_output("/usr/bin/exiftool " + settings.MEDIA_ROOT + func_out['file'], shell=True)
	
	item_info = {} 
	for row in res.split('\n')[:-1]:
     		temp = row.split(':')
     		key = temp[0].strip().strip()
     		value = ' '.join(temp[1:]).strip().strip()
     		item_info[key] = value
	
	l = item_info['Duration'].split(' ') 

    	r = requests.put(settings.ACTIVE_CORE_ENDPOINT + 'api/items/'+str(func_out['id'])+"/", { 'frame_width' : item_info['Image Width'], 
                                                                            'frame_height' : item_info['Image Height'],
									    'duration': int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]),  
									    'format': item_info['File Type'],
									    'frame_rate': item_info['Video Frame Rate'],
									    'filesize': item_info['File Size']
															})





def extract_image_data(func_in, func_out):
	
	res = subprocess.check_output("/usr/bin/exiftool " + settings.MEDIA_ROOT + func_out['file'], shell=True)
	
	item_info = {} 
	for row in res.split('\n')[:-1]:
     		temp = row.split(':')
     		key = temp[0].strip().strip()
     		value = ' '.join(temp[1:]).strip().strip()
     		item_info[key] = value
	
	

    	r = requests.put(settings.ACTIVE_CORE_ENDPOINT + 'api/items/'+str(func_out['id'])+"/", { 'frame_width' : item_info['Image Width'], 
                                                                            'frame_height' : item_info['Image Height'],
									    'format': item_info['File Type'],
									    'filesize': item_info['File Size']})
				


def extract_audio_data(func_in, func_out):
	
	res = subprocess.check_output("/usr/bin/exiftool " + settings.MEDIA_ROOT + func_out['file'], shell=True)
	
	item_info = {} 
	for row in res.split('\n')[:-1]:
     		temp = row.split(':')
     		key = temp[0].strip().strip()
     		value = ' '.join(temp[1:]).strip().strip()
     		item_info[key] = value
	
	if(item_info['Duration'].endswith('s')):
		item_info['Duration'] = int(float(item_info['Duration'].strip('s')))			
	else:
		l = item_info['Duration'].split(' ') 
		item_info['Duration'] = int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    	r = requests.put(settings.ACTIVE_CORE_ENDPOINT + 'api/items/'+str(func_out['id'])+"/", { 
									    'duration': item_info['Duration'],  
									    'format': item_info['File Type'],
									    'sample_rate': item_info['Sample Rate'],
									    'num_channels': item_info['Num Channels'],
									    'bits_per_sample': item_info['Bits Per Sample'],
								            'filesize': item_info['File Size']
															})


	
def perform():
	pass


if __name__ == '__main__':
	extract_data()
