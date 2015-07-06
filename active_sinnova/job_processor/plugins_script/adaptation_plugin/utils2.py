"""
This module is used to define al script necessary to extract and store a preview of a digital
item computed from the original one (uploaded by the user).
A new file is saved on the filesystem in the same directory of the original file.
"""

from django.conf import settings
from plugins_script.commons.item import set_preview
import requests
import subprocess
import os


# ffmpeg -i scenecliptest00001.avi -c:v libx264 -preset ultrafast video.mp4
# opzione per spostare i metadata all'inizio del video: -movflags faststart 
# per sovrascrivere l'output se esiste gia':            -y
# per ridurre la verbosita' della console:              -loglevel fatal
# per ridurre il frame rate di un video:                -r 5


def extract_video_preview(func_in, func_out):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """

    # detect start and final absolute paths of video resources
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    preview_path = os.path.join('/tmp', str(func_out['id']) + '_preview.mp4')
    # execute video conversion
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -codec:v libx264 -preset fast -movflags +faststart ' + preview_path
    subprocess.check_output(cmd, shell=True)
    # check if the preview has been generated
    if not os.path.exists(preview_path):
        raise Exception("Preview not generated for video item" + str(func_out['id']))

    # update data about the new generated preview file
    res = set_preview(func_out['id'], preview_path, 'video/mp4')

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for video item" + str(func_out['id']))


def extract_image_preview(func_in, func_out):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """

    # create the start and final path for the image digital items
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    preview_path = os.path.join('/tmp', str(func_out['id']) + 'preview.jpeg')
    # extract image thumbnail
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf scale=-1:600 ' + preview_path
    subprocess.check_output (cmd, shell=True)
    # check if the preview has been created
    if not os.path.exists(preview_path):
        raise Exception("Preview image not generated")

    # update data about the new generated preview file
    res = set_preview(func_out['id'], preview_path, 'image/jpeg')

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for image item" + str(func_out['id']))


def extract_audio_preview(func_in, func_out):

    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    preview_path = os.path.join('/tmp', str(func_out['id']) + 'preview.mp3')
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -ab 128k ' + preview_path
    subprocess.check_output(cmd, shell=True)
    if not os.path.exists(preview_path):
        raise Exception("Audio preview not generated for item " + str(func_out['id']))

    # update data about the new generated preview file
    res = set_preview(func_out['id'], preview_path, 'audio/mp3')

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for audio item" + str(func_out['id']))
