from django.conf import settings
import requests
import subprocess
import os

"""
This module is used to define al script necessary to extract and store a thumbnail for each
provided item.
Given a digital item an appropriate thumbnail is extracted and saved in the local file system.

NB: attualmente non viene estratto alcun thumbnail ma si utilizzano delle immagini standard.
"""

#ffmpeg -ss 49 -i MONITOR072011.mpg  -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 sample.jpg


def extract_video_thumbnail(func_in, func_out):
	"""
	This function is used to extract a thumbnail image from a video item.
	The thumbnail is created extracting the frame at second 49, cropping and resizing the
	frame size.

	@param func_in: Input parameters of the function that generate this function call
	@param func_out: Output parameters of the function that generate this function call
	"""
	thumb_path = ''

	# construct a thumbnail image from the original digital item
	try:
		file_path  = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])
		thumb_path = os.path.join('/tmp', str(func_out['id']) + '_thumb.png')
		cmd = '/usr/bin/ffmpeg -loglevel fatal -y -ss 10 -i ' + file_path + ' -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
		subprocess.check_output(cmd, shell=True)
		
		if(not os.path.exists(thumb_path)):
			raise Exception("Thumbnail not generated")
	except Exception as e:
		# create a standard thumbnail for a video
		thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'video.png')

	file = open(thumb_path, 'rb')
	multiple_files = [('thumb', ('thumb.png', file, 'image/png')),]

	server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
    	r = requests.put(server_url, files=multiple_files)


def extract_image_thumbnail(func_in, func_out):
	"""
        This function is used to create a thumbnail for a image item.
	A cropped and resized portion of the original image is used as 
	thumbnail for each digital item. The thumbnail image size is 256*256 pixels.

        @param func_in: Input parameters of the function that generate this function call
        @param func_out: Output parameters of the function that generate this function call
        """
	# create a thumbnail image from the original digital item
	thumb_path = ''

	print "Parametri ", func_in, func_out


	try:
                file_path  = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])
                thumb_path = os.path.join('/tmp', str(func_out['id']) + '_thumb.png')
                cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i ' + file_path + ' -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
		subprocess.check_output(cmd, shell=True)

        except Exception as e:
		print e
		# create a standard thumbnail for a video
		thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'image.png')

	file = open(thumb_path, 'rb')
        multiple_files = [('thumb', ('thumb.png', file, 'image/png')),]

	server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
    	r = requests.put(server_url, files=multiple_files)


def extract_audio_thumbnail(func_in, func_out):
	"""
	This function is used to create a thumbnail for an audio item.
        A standard image is used as thumbnail for all audio files.
        
	@param func_in: Input parameters of the function that generate this function call
        @param func_out: Output parameters of the function that generate this function call
	"""
       	# construct a (fake) thumbnail file for the audio file
	thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'audio.png')

	file = open(thumb_path, 'rb')
        multiple_files = [('thumb', ('thumb.png', file, 'image/png')),]


	server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(func_out['id']) + '/'
	print "Chiamata a ", server_url
    	r = requests.put(server_url, files=multiple_files)
