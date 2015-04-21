from django.conf import settings
import requests
import subprocess
import os

"""
This module is used to define al script necessary to extract and store a preview of a digital
item computed from the original one (uploaded by the user).
A new file is saved on the filesystem in the same directory of the original file.
"""

# ffmpeg -i scenecliptest00001.avi -c:v libx264 -preset ultrafast video.mp4
# opzione per spostare i metadata all'inizio del video: -movflags faststart 
# per sovrascrivere l'output se esiste gia':            -y
# per ridurre la verbosita' della console:              -loglevel fatal
# per ridurre il frame rate di un video:                -r 5


def convert_video(func_in, func_out):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """

    try:
        # detect start and final absolute paths of video resources
        file_path = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
        preview_path = os.path.join('/tmp', str(func_out['id']) + '_preview.mp4')
        # execute video conversion
        cmd = '/usr/bin/ffmpeg -loglevel fatal -y -movflags faststart -i  "' + file_path + '" -vc mp4 -r 5' + preview_path
        subprocess.check_output(cmd, shell=True)
        # check if the preview has been generated
        if (not os.path.exists(preview_path)):
            raise Exception("Preview video not generated")

        # update data about the new generated preview file
        file = open(preview_path, 'rb')
        multiple_files = [('preview', ('preview.mp4', file, 'video/mp4')), ]
        # send updated data to the core using the REST API
        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(func_out['id']) + '/'
        r = requests.put(server_url, files=multiple_files)
        print "Invio della preview a ", server_url

    except Exception as e:
        print e


def convert_image(func_in, func_out):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """

    try:
        # create the start and final path for the image digital items
        file_path = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
        preview_path = os.path.join('/tmp', str(func_out['id']) + 'preview.jpeg')
        # extract image thumbnail
        cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vc png ' + preview_path
        subprocess.check_output(cmd, shell=True)
        # check if the preview has been created
        if (not os.path.exists(preview_path)):
            raise Exception("Preview image not generated")

        # update data about the new generated preview file
        file = open(preview_path, 'rb')
        multiple_files = [('preview', ('preview.jpeg', file, 'image/jpeg')), ]
        # send updated data to the core using the REST API
        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(func_out['id']) + '/'
        r = requests.put(server_url, files=multiple_files)
        print "Invio della preview a ", server_url

    except Exception as e:
        print e


def convert_audio(func_in, func_out):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['file'])
        preview_path = os.path.join('/tmp', str(func_out['id']) + 'preview.mp3')
        cmd = '/usr/bin/ffmpeg -loglevel fatal -y -b 128k -i "' + file_path + '" ' + preview_path
        subprocess.check_output(cmd, shell=True)
        if (not os.path.exists(preview_path)):
            raise Exception("Audio preview not generated for item " + str(func_out['id']))

        # update data about the new generated preview file
        file = open(preview_path, 'rb')
        multiple_files = [('preview', ('preview.mp3', file, 'audio/mp3')), ]
        # send updated data to the core using the REST API
        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(func_out['id']) + '/'
        r = requests.put(server_url, files=multiple_files)
        print "Invio della preview a ", server_url

    except Exception as e:
        print e
