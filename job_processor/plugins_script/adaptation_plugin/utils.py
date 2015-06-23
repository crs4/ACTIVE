"""
This module is used to define al script necessary to extract and store a preview of a digital
item computed from the original one (uploaded by the user).
A new file is saved on the filesystem in the same directory of the original file.
"""

from django.conf import settings
from plugins_script.commons.item import set_preview, set_status
from skeleton.skeletons import Farm, Seq
from skeleton.visitors import Executor
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
    the resulting video will be in MPEG-4 format and 5fps. Computations are executed in a distributed way,
    on acluster node.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_video_preview)
    return Executor().eval(seq, [func_in, func_out])

def _extract_video_preview(params):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps.

    @param params: Array containing all necessary function parameters
    """

    auth_dict  = params[0]
    param_dict = params[1]

    # detect start and final absolute paths of video resources
    file_path = os.path.join(settings.MEDIA_ROOT, param_dict['file'])
    preview_path = os.path.join('/tmp', str(param_dict['id']) + '_preview.mp4')
    # execute video conversion
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -codec:v libx264 -preset fast -movflags +faststart ' + preview_path
    subprocess.check_output(cmd, shell=True)
    # check if the preview has been generated
    if not os.path.exists(preview_path):
        raise Exception("Preview not generated for video item" + str(param_dict['id']))

    # update data about the new generated preview file
    res = set_preview(param_dict['id'], preview_path, 'video/mp4', auth_dict['token'])

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for video item" + str(param_dict['id']))

    set_status(param_dict['id'], 'ADAPTED', auth_dict['token'])
    return True


def extract_image_preview(auth_dict, param_dict):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.
    Computations are executed in a distributed way

    @param auth_dict: Function input that trigger the event which called this script
    @param param_dict: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_image_preview)
    return Executor().eval(seq, [auth_dict, param_dict])


def _extract_image_preview(params):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.

    @param params: Array containing all necessary function parameters.
    """

    auth_dict  = params[0]
    param_dict = params[1]

    # create the start and final path for the image digital items
    file_path = os.path.join(settings.MEDIA_ROOT, param_dict['file'])
    preview_path = os.path.join('/tmp', str(param_dict['id']) + 'preview.jpeg')
    # extract image thumbnail
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf scale=-1:600 ' + preview_path
    subprocess.check_output (cmd, shell=True)
    # check if the preview has been created
    if not os.path.exists(preview_path):
        raise Exception("Preview image not generated")

    # update data about the new generated preview file
    res = set_preview(param_dict['id'], preview_path, 'image/jpeg', auth_dict['token'])

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for image item" + str(param_dict['id']))

    set_status(param_dict['id'], 'ADAPTED', auth_dict['token'])
    return True


def extract_audio_preview(auth_dict, param_dict):
    """
    This method is used to create the preview for a generic audio item.
    The item is converted in a mp3 file in order to use a standard codec.
    Computations are executed in a distributed way among a cluster node.

    @param auth_dict: Function input that trigger the event which called this script
    @param param_dict: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_audio_preview)
    return Executor().eval(seq, [auth_dict, param_dict])

def _extract_audio_preview(params):
    """
    This function is used to extract a standard low quality version of the provided audio,
    the resulting audio will be in MP3 format.

    @param params: Array containing all necessary function parameters.
    """
    auth_dict  = params[0]
    param_dict = params[1]

    file_path = os.path.join(settings.MEDIA_ROOT, param_dict['file'])
    preview_path = os.path.join('/tmp', str(param_dict['id']) + 'preview.mp3')
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -ab 128k ' + preview_path
    subprocess.check_output(cmd, shell=True)

    #cmd = "/usr/bin/ffmpeg -y -i "
    #cmd += os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['filename'])
    #cmd += " -acodec pcm_s16le -ac 1 -ar 16000 "
    #cmd += os.path.join('/tmp', str(func_out['id']) + ".wav")
    #subprocess.check_output(cmd, shell=True)

    if not os.path.exists(preview_path):
        raise Exception("Audio preview not generated for item " + str(param_dict['id']))

    # update data about the new generated preview file
    res = set_preview(param_dict['id'], preview_path, 'audio/mp3', auth_dict['token'])

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for audio item" + str(param_dict['id']))

    set_status(param_dict['id'], 'ADAPTED', auth_dict['token'])
    return True
