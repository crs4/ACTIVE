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


def extract_audio_preview(*args, **kwargs):
    """
    This method is used to create the preview for a generic audio item.
    The item is converted in a mp3 file in order to use a standard codec.
    Computations are executed in a distributed way among a cluster node.

    @param auth_dict: Function input that trigger the event which called this script
    @param param_dict: Function output that trigger the event which called this script
    """
    # create the start and final path for the audio digital items
    file_path = os.path.join(settings.MEDIA_ROOT, args[0]['file'])
    preview_path = os.path.join('/tmp', str(args[0]['id']) + 'preview.mp3')
    
    # compute the audio preview in a distribute way
    seq = Seq(_extract_audio_preview)
    Executor().eval(seq, (file_path, preview_path))
    
    # update data about the new generated preview file
    set_preview(args[0]['id'], preview_path, 'audio/mp3', kwargs.get('token', None))
    set_status(args[0]['id'], 'ADAPTED', kwargs.get('token', None))
    
    # remove the preview file from the local filesystem
    os.remove(preview_path)

def _extract_audio_preview(file_path, preview_path):
    """
    This function is used to extract a standard low quality version of the provided audio,
    the resulting audio will be in MP3 format.

    @param file_path: Path of the item that will be considered for preview extraction.
    @param preview_path: Path of the preview that will be generated.
    """
    # extract the audio preview   
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -ab 128k ' + preview_path
    subprocess.check_output(cmd, shell=True)

    #cmd = "/usr/bin/ffmpeg -y -i "
    #cmd += os.path.join(settings.MEDIA_ROOT, 'items', str(func_out['id']), func_out['filename'])
    #cmd += " -acodec pcm_s16le -ac 1 -ar 16000 "
    #cmd += os.path.join('/tmp', str(func_out['id']) + ".wav")
    #subprocess.check_output(cmd, shell=True)

    if not os.path.exists(preview_path):
        raise Exception("Audio preview not generated for item " + file_path)


def extract_image_preview(*args, **kwargs):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.
    Computations are executed in a distributed way

    @param arg: Function arguments (or result of event trigger)
    @param kwargs: Keyword arguments passed to the function (e.g. authentication token)
    """
    # create the start and final path for the image digital items
    file_path = os.path.join(settings.MEDIA_ROOT, args[0]['file'])
    preview_path = os.path.join('/tmp', str(args[0]['id']) + 'preview.jpeg')
    
    # compute the audio preview in a distribute way
    seq = Seq(_extract_image_preview)
    Executor().eval(seq, (file_path, preview_path))
    
    # update data about the new generated preview file
    set_preview(args[0]['id'], preview_path, 'image/jpeg', kwargs.get('token', None))
    set_status(args[0]['id'], 'ADAPTED', kwargs.get('token', None))

    # remove the preview file from the local filesystem
    os.remove(preview_path)
    
def _extract_image_preview(file_path, preview_path):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.

    @param file_path: Path of the item that will be considered for preview extraction.
    @param preview_path: Path of the preview that will be generated.
    """
    print file_path, preview_path
    # extract image preview
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf scale=-1:600 ' + preview_path
    subprocess.check_output (cmd, shell=True)
    # check if the preview has been created
    if not os.path.exists(preview_path):
        raise Exception("Preview image not generated")



def extract_video_preview(*args, **kwargs):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps. Computations are executed in a distributed way,
    on acluster node.

    @param func_in: Function input that trigger the event which called this script
    @param func_out: Function output that trigger the event which called this script
    """
    # detect start and final absolute paths of video resources
    file_path = os.path.join(settings.MEDIA_ROOT, args[0]['file'])
    preview_path = os.path.join('/tmp', str(args[0]['id']) + '_preview.mp4')
    
    # execute the preview extraction in a distributed way
    seq = Seq(_extract_video_preview)
    Executor().eval(seq, (file_path, preview_path))
    
    # update data about the new generated preview file
    set_preview(args[0]['id'], preview_path, 'video/mp4', kwargs.get('token', None))
    set_status(args[0]['id'], 'ADAPTED', kwargs.get('token', None))
    
    # remove the preview file from the local filesystem
    os.remove(preview_path)

def _extract_video_preview(file_path, preview_path):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps.
    
    @param file_path: Path of the item that will be considered for preview extraction.
    @param preview_path: Path of the preview that will be generated.
    """
    # execute video conversion
    cmd  = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path
    cmd += '" -codec:v libx264 -preset fast -movflags +faststart -strict -2 ' + preview_path
    subprocess.check_output(cmd, shell=True)
    # check if the preview has been generated
    if not os.path.exists(preview_path):
        raise Exception("Preview not generated for video item" + file_path)
