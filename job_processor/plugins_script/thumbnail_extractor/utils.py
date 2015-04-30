from django.conf import settings
import requests
import subprocess
import os
import shutil


"""
This module is used to define al script necessary to extract and store
a thumbnail for each type of supported digital items.
Given a digital item an appropriate thumbnail is extracted and saved
in the local file system. For audio items a standard thumbnail is returned.
"""

# funzione utilizzata per estrarre una thumbnail all'istante 49
# ffmpeg -ss 49 -i MONITOR0720  11.mpg  -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 sample.jpg


def extract_video_thumbnail(func_in, func_out):
    """
    This function is used to extract a thumbnail image from a video item.
    The thumbnail is created extracting the frame at second 10, cropping
    and resizing the frame size.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        # construct the start and final path for digital items
        file_path = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])
        thumb_path = os.path.join('/tmp', str(func_out['id']) + '_thumb.jpeg')
        # extract the thumbnail for the current video item
        cmd = '/usr/bin/ffmpeg -loglevel fatal -y -ss 10 -i "' + file_path + '" -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
        subprocess.check_output(cmd, shell=True)

        # check if the thumbnail has been created and create a standard image
        if (not os.path.exists(thumb_path)):
            # create the default thumbnail, coping from a known directory
            print 'Video item thumbnail not generated'
            default_thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'video.jpeg')
            shutil.copyfile(default_thumb_path, thumb_path)

        # send the thumbnail to the core
        file = open(thumb_path, 'rb')
        multiple_files = [('thumb', ('thumb.jpeg', file, 'image/jpeg')), ]
        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(func_out['id']) + '/'
        r = requests.put(server_url, files=multiple_files)
        print 'Sending thumbnail to ', server_url

        # delete the temporary thumbnail from local filesystem
        os.remove(thumb_path)

    except Exception as e:
        print e


def extract_image_thumbnail(func_in, func_out):
    """
    This function is used to create a thumbnail for a image item.
    A cropped and resized portion of the original image is used as
    thumbnail for each digital item. The thumbnail image size is 256*256 pixels.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        # construct start and final path for digital items
        file_path = os.path.join(settings.MEDIA_ROOT, 'items', func_out['file'])
        thumb_path = os.path.join('/tmp', str(func_out['id']) + '_thumb.jpeg')
        # generate the thumbnail for the image
        cmd = '/usr/bin/ffmpeg -loglevel fatal -y -i "' + file_path + '" -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 ' + thumb_path
        subprocess.check_output(cmd, shell=True)
        # check if the thumbnail has been created and create a standard thumbnail
        if (not os.path.exists(thumb_path)):
            # create the default thumbnail, coping from a known directory
            print "Image item thumbnail not generated"
            default_thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'image.jpeg')
            shutil.copyfile(default_thumb_path, thumb_path)

        # send the thumbnail to the core
        file = open(thumb_path, 'rb')
        multiple_files = [('thumb', ('thumb.jpeg', file, 'image/jpeg')), ]
        server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(func_out['id']) + '/'
        
        r = requests.put(server_url, files=multiple_files)
        print 'Sending thumbnail to ', server_url

        # delete the temporary thumbnail from local filesystem
        os.remove(thumb_path)
    except Exception as e:
        print e



def extract_audio_thumbnail(func_in, func_out):
    """
    This function is used to create a thumbnail for an audio item.
    A standard image is used as thumbnail for all audio files.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    # construct a standard thumbnail file for the audio file
    thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', 'audio.jpeg')
    file = open(thumb_path, 'rb')
    multiple_files = [('thumb', ('thumb.jpeg', file, 'image/jpeg')), ]

    # send the thumbnail to the core
    server_url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(func_out['id']) + '/'
    r = requests.put(server_url, files=multiple_files)
    print "Sending thumbnail to ", server_url
