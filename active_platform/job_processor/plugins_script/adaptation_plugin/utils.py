# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to define al script necessary to extract and store a preview of a digital
item computed from the original one (uploaded by the user).
A new file is saved on the filesystem in the same directory of the original file.
"""

from plugins_script.commons.utils import get_media_root
from plugins_script.commons.item import set_preview
from skeleton.skeletons import Farm, Seq
from skeleton.visitors import Executor
import requests
import subprocess
import os


# ffmpeg -i scenecliptest00001.avi -c:v libx264 -preset ultrafast video.mp4
# option used to move the metadata on the top of the file: -movflags faststart 
# for overriding the output if already exists:             -y
# reduce the verbosity:                                    -loglevel fatal
# reduce the video frame rate:                             -r 5


def extract_video_preview(auth_params, func_params):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps. Computations are executed in a distributed way,
    on acluster node.

    @param auth_params: Function input that trigger the event which called this script
    @param func_params: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_video_preview)
    return Executor().eval(seq, [auth_params, func_params])

def _extract_video_preview(params):
    """
    This function is used to extract a standard low quality version of the provided video,
    the resulting video will be in MPEG-4 format and 5fps.

    @param params: Array containing all necessary function parameters
    """
    auth_params  = params[0]
    func_params = params[1]

    # detect start and final absolute paths of video resources
    file_path = os.path.join(get_media_root(), func_params['file'])
    preview_path = os.path.join('/tmp', str(func_params['id']) + '_preview.mp4')
    token = auth_params['token']
    
    # execute video conversion
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -codec:v libx264 -preset fast -movflags +faststart -strict -2 ' + preview_path
    subprocess.check_output(cmd, shell=True)
    # check if the preview has been generated
    if not os.path.exists(preview_path):
        raise Exception("Preview not generated for video item" + str(func_params['id']))

    # update data about the new generated preview file
    res = set_preview(func_params['id'], preview_path, 'video/mp4', token)

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for video item" + str(func_params['id']))
    return True


def extract_image_preview(auth_params, func_params):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.
    Computations are executed in a distributed way

    @param auth_params: Function input that trigger the event which called this script
    @param func_params: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_image_preview)
    return Executor().eval(seq, [auth_params, func_params])

def _extract_image_preview(params):
    """
    This function is used to extract a standard low quality version of the provided image,
    the resulting video will be in PNG format with a scaled resolution.

    @param params: Array containing all necessary function parameters.
    """

    auth_params  = params[0]
    func_params = params[1]

    # create the start and final path for the image digital items
    file_path = os.path.join(get_media_root(), func_params['file'])
    preview_path = os.path.join('/tmp', str(func_params['id']) + 'preview.jpeg')
    token = auth_params['token']
    # extract image thumbnail
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf scale=-1:600 ' + preview_path
    subprocess.check_output (cmd, shell=True)
    # check if the preview has been created
    if not os.path.exists(preview_path):
        raise Exception("Preview image not generated")

    # update data about the new generated preview file
    res = set_preview(func_params['id'], preview_path, 'image/jpeg', token)

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for image item" + str(func_params['id']))
    return True

def extract_audio_preview(auth_params, func_params):
    """
    This method is used to create the preview for a generic audio item.
    The item is converted in a mp3 file in order to use a standard codec.
    Computations are executed in a distributed way among a cluster node.

    @param auth_params: Function input that trigger the event which called this script
    @param func_params: Function output that trigger the event which called this script
    """
    seq = Seq(_extract_audio_preview)
    return Executor().eval(seq, [auth_params, func_params])

def _extract_audio_preview(params):
    """
    This function is used to extract a standard low quality version of the provided audio,
    the resulting audio will be in MP3 format.

    @param params: Array containing all necessary function parameters.
    """
    auth_params  = params[0]
    func_params = params[1]
    # create the start and final path for the audio digital items
    file_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
    preview_path = os.path.join('/tmp', str(func_params['id']) + 'preview.mp3')
    token = auth_params['token']
    # extract audio preview
    cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -ab 128k ' + preview_path
    subprocess.check_output(cmd, shell=True)
    # check if the preview has been created
    if not os.path.exists(preview_path):
        raise Exception("Audio preview not generated for item " + str(func_params['id']))

    # update data about the new generated preview file
    res = set_preview(func_params['id'], preview_path, 'audio/mp3', token)

    # remove the preview file from the local filesystem
    os.remove(preview_path)

    if not res:
        raise Exception("Preview not generated for audio item" + str(func_params['id']))
    return True

