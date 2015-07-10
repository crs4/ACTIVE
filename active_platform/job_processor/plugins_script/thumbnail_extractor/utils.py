"""
This module is used to define al script necessary to extract and store
a thumbnail for each type of supported digital items.
Given a digital item an appropriate thumbnail is extracted and saved
in the local file system. For audio items a standard thumbnail is returned.
"""

from django.conf import settings
from plugins_script.commons.item import set_thumbnail
import subprocess
import os
import shutil


# funzione utilizzata per estrarre una thumbnail all'istante 49
# ffmpeg -ss 49 -i MONITOR0720  11.mpg  -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 sample.jpg


def extract_video_thumbnail(auth_params, func_params):
    """
    This function is used to extract a thumbnail image from a video item.
    The thumbnail is created extracting the frame at second 8, cropping
    and resizing the frame size.

    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    # construct the start and final path for digital items
    file_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
    thumb_path = os.path.join('/tmp', str(func_params['id']) + '_thumb.jpeg')
    # extract the thumbnail for the current video item
    cmd = 'ffmpeg -loglevel fatal -y -ss 8 -i "' + file_path + '" -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
    subprocess.check_output(cmd, shell=True)
    token = auth_params['token']


    # check if the thumbnail has been created otherwise create a standard image
    if not os.path.exists(thumb_path):
        # create the default thumbnail, coping from a known directory
        default_thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'video.jpeg')
        shutil.copyfile(default_thumb_path, thumb_path)

    # send the thumbnail to the core
    res = set_thumbnail(func_params['id'], thumb_path, 'image/jpeg',token)

    # delete the temporary thumbnail from local filesystem
    os.remove(thumb_path)

    if not res:
        raise Exception("Error on video thumbnail generation " + str(func_params['id']))


def extract_image_thumbnail(auth_params, func_params):
    """
    This function is used to create a thumbnail for a image item.
    A cropped and resized portion of the original image is used as
    thumbnail for each digital item. The thumbnail image size is 256*256 pixels.

    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """

    # construct start and final path for digital items
    file_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
    thumb_path = os.path.join('/tmp', str(func_params['id']) + '_thumb.jpeg')
    # generate the thumbnail for the image
    cmd = 'ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
    subprocess.check_output(cmd, shell=True)
    token = auth_params['token']

    # check if the thumbnail has been created otherwise create a standard thumbnail
    if not os.path.exists(thumb_path):
        # create the default thumbnail, coping from a known directory
        default_thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'image.jpeg')
        shutil.copyfile(default_thumb_path, thumb_path)

    # send the thumbnail to the core
    res = set_thumbnail(func_params['id'], thumb_path, 'image/jpeg',token)

    # delete the temporary thumbnail from local filesystem
    os.remove(thumb_path)

    if not res:
        raise Exception("Error on video thumbnail generation " + str(func_params['id']))


def extract_audio_thumbnail(auth_params, func_params):
    """
    This function is used to create a thumbnail for an audio item.
    A standard image is used as thumbnail for all audio files.

    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    # construct a standard thumbnail for the audio file
    thumb_path = os.path.join('/tmp', str(func_params['id']) + '_thumb.jpeg')
    default_thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'audio.jpeg')
    shutil.copyfile(default_thumb_path, thumb_path)
    
    token = auth_params['token']

    # send the thumbnail to the core
    res = set_thumbnail(func_params['id'], thumb_path, 'image/jpeg',token)

    # delete the temporary thumbnail from local filesystem
    os.remove(thumb_path)

    if not res:
        raise Exception("Error on thumbnail generation for audio item " + str(func_params['id']))
