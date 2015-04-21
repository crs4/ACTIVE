from django.conf import settings
import requests
import subprocess
import time
import os

def get_exif_metadata(item_path):
	"""
	Function used to extract the metadata associated to a given digital item.
	This is a wrapper for the Exiftool shell command and it will provide all metadata
	extracted by this command.
	:param item_path: Item absolute path that will be considered for metadata extraction.
	:returns: A dictionary containing all extracted item metadata.
	:rtype: dictionary
	"""
	
	res = subprocess.check_output('/usr/bin/exiftool "' + item_path + '"' , shell=True)

	item_info = {}
        for row in res.split('\n')[:-1]:
                temp = row.split(':')
                key = temp[0].strip().strip()
                value = ':'.join(temp[1:]).strip().strip()
                item_info[key] = value
	
	return item_info


def convert_duration(item_info):
	"""
	Function used to convert the duration field extracted from the metadata
	to seconds (integer value).
	:param item_info: Dictionary that will be updated, editing the Duration field.
	:returns: Updated item metadata dictionary
	:rtype: dictionary
	"""
	# when the duration is low it is represented as seconds
	if(item_info['Duration'].endswith('s')):
                item_info['Duration'] = int(float(item_info['Duration'].strip('s')))



	# when duration is high it is represented in the format H:MM:SS 
        else:
		item_info['Duration'] = item_info['Duration'].strip('(approx)')
                l = item_info['Duration'].split(':')
                item_info['Duration'] = int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


	# make a check for the number of channels
	#if 'Num Channels' not in item_info:
	#	item_info['Num Channels'] = 1

	return item_info


def extract_video_data(func_in, func_out):
	"""
	This function is used to extract relevant metadata from a video item
	and then save this data on the active core.
	:param func_in: Input parameters of the function that generate this function call
	:param func_out: Output parameters of the function that generate this function call
	"""
	file_path = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])

	item_info = get_exif_metadata(file_path)
	convert_duration(item_info)

	server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
	keys = [('mime_type', 'MIME Type'),
		('frame_width', 'Image Width'),
		('frame_height', 'Image Height'),
		('duration', 'Duration'),
		('format', 'File Type'),
		('frame_rate', 'Video Frame Rate'),
		('filesize', 'File Size')]

	res_dict = {}
	for k in keys:
		if k[1] in item_info:
			res_dict[k[0]] = item_info[k[1]]
	r = requests.put(server_url, res_dict)
	"""
    	r = requests.put(server_url,   {'mime_type' : item_info['MIME Type'],
					'frame_width' : item_info['Image Width'],
                                      	'frame_height' : item_info['Image Height'],
					'duration' : item_info['Duration'],
					'format': item_info['File Type'],
					'frame_rate': item_info['Video Frame Rate'],
					'filesize': item_info['File Size']})
	"""

def extract_image_data(func_in, func_out):
	"""
        This function is used to extract relevant metadata from a image item
        and then save this data on the active core.
        :param func_in: Input parameters of the function that generate this function call
        :param func_out: Output parameters of the function that generate this function call
        """
	file_path = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])

	item_info = get_exif_metadata(file_path)

	server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
    	r = requests.put(server_url,  { 'mime_type' : item_info['MIME Type'],
					'frame_width' : item_info['Image Width'],
					'frame_height' : item_info['Image Height'],
					'format': item_info['File Type'],
					'filesize': item_info['File Size']})


def extract_audio_data(func_in, func_out):
	"""
        This function is used to extract relevant metadata from a video item
        and then save this data on the active core.
        :param func_in: Input parameters of the function that generate this function call
        :param func_out: Output parameters of the function that generate this function call
	"""
	file_path = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])

        item_info = get_exif_metadata(file_path)
        convert_duration(item_info)

        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
    	r = requests.put(server_url, {	'mime_type' : item_info['MIME Type'],
					'duration': item_info['Duration'],  
					'format': item_info['File Type'],
					'sample_rate': item_info['Sample Rate'],
					'num_channels': item_info['Num Channels'],
					'bits_per_sample': item_info['Bits Per Sample'],
					'filesize': item_info['File Size'] })
