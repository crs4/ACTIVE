from django.conf import settings
import requests
import subprocess
import os

"""
This module is used to define al script necessary to extract and store a thumbnail for each
provided item.
Given a digital item an appropriate thumbnail is extracted and saved in the local file system.
"""

# ffmpeg -i scenecliptest00001.avi -c:v libx264 -preset ultrafast video.mp4
# opzione per spostare i metadata all'inizio del video: -movflags faststart 
# per sovrascrivere l'output se esiste gia': -y
# per ridurre la verbosita' della console: -loglevel fatal

def convert_video(func_in, func_out):
	try:
		file_path  = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
		ret_path = os.path.splitext(file_path)[0] + '.mp4'
		print(ret_path)
		cmd = '/usr/bin/ffmpeg -loglevel fatal -y -movflags faststart -i  ' + file_path + ' -vc mp4 ' + ret_path
		subprocess.check_output(cmd, shell=True)
		if(not os.path.exists(ret_path)):
                        raise Exception("Converted video not generated")
	except Exception as e:
		print e

def convert_image(func_in, func_out):
	try:
		file_path  = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
		ret_path = os.path.splitext(file_path)[0] + '.png'
		cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i ' + file_path + ' -vc png ' + ret_path
		subprocess.check_output(cmd, shell=True)
		if(not os.path.exists(ret_path)):
			raise Exception("Converted image not generated")
	except Exception as e:
		print e

def convert_audio(func_in, func_out):
	try:
		file_path  = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
		ret_path = os.path.splitext(file_path)[0] + '.mp3'
		cmd = '/usr/bin/ffmpeg -loglevel fatal -y -movflags faststart -i ' + file_path + ' -vc mp3 ' + ret_path
		subprocess.check_output(cmd, shell=True)
		if(not os.path.exists(ret_path)):
			raise Exception("Converted audio not generated")
	except Exception as e:
		print e

















### metodo di esempio che DEVE essere rimosso
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
