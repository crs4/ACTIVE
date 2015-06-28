"""
This module is used to extract all available metadata contained in a digital item.
When item metadata has been extracted it is saved on the ACTIVE core, using the proxy methods
that ill invoke the REST API.
"""

from django.conf import settings
from plugins_script.commons.item import set_status, set_video_metadata, set_image_metadata, set_audio_metadata
import subprocess
import os

def extract_video_data(func_in, func_out):
    """
    This function is used to extract relevant metadata from a video item
    and then save this data on the active core.

    :param func_in: Input parameters of the function that generate this function call
    :param func_out: Output parameters of the function that generate this function call
    """
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_info = get_exif_metadata(file_path)

    if not set_video_metadata(func_out['id'], item_info):
        raise Exception('Error on metadata update')

    if not set_status(func_out['id'], 'ANALYZED'):
        raise Exception('Error on processing status update')

    print "Extracted and saved metadata for video item", func_out['id']

def extract_image_data(func_in, func_out):
    """
    This function is used to extract relevant metadata from a image item
    and then save this data on the active core.

    :param func_in: Input parameters of the function that generate this function call
    :param func_out: Output parameters of the function that generate this function call
    """
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_info = get_exif_metadata(file_path)

    if not set_image_metadata(func_out['id'], item_info):
        raise Exception('Error on metadata update')

    if not set_status(func_out['id'], 'ANALYZED'):
        raise Exception('Error on processing status update')


def extract_audio_data(func_in, func_out):
    """
    This function is used to extract relevant metadata from a video item
    and then save this data on the active core.

    :param func_in: Input parameters of the function that generate this function call
    :param func_out: Output parameters of the function that generate this function call
    """
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_info = get_exif_metadata(file_path)

    if not set_audio_metadata(func_out['id'], item_info):
        raise Exception('Error on metadata update')

    if not set_status(func_out['id'], 'ANALYZED'):
        raise Exception('Error on processing status update')



#############################################################
######## utils for metadata extraction using ExifTool #######
#############################################################
def get_exif_metadata(item_path):
    """
    Function used to extract the metadata associated to a given digital item.
    This is a wrapper for the Exiftool shell command and it will provide all metadata
    extracted by this command.

    :param item_path: Item absolute path that will be considered for metadata extraction.
    :returns: A dictionary containing all extracted item metadata.
    """
    res = subprocess.check_output('exiftool "' + item_path + '"' , shell=True)
    # extract fields and remove spaces 
    temp_dict = {}
    for row in res.split('\n')[:-1]:
            temp = row.split(':')
            key = temp[0].strip().strip()
            value = ':'.join(temp[1:]).strip().strip()
            temp_dict[key] = value

    # convert the duration representation
    convert_duration(temp_dict)

    # convert fields in a standard representation 
    keys = [('mime_type', 'MIME Type'),
            ('frame_width', 'Image Width'),
            ('frame_height', 'Image Height'),
            ('duration', 'Duration'),
            ('duration', 'Play Duration'),
            ('format', 'File Type'),
            ('num_channels', 'Num Channels'),
            ('sample_rate', 'Sample Rate'),
            ('bits_per_sample', 'Bits Per Sample'),
            ('frame_rate', 'Video Frame Rate'),
            ('frame_rate', 'Frame Rate'),
            ('filesize', 'File Size')]

    res_dict = {}
    for k in keys:
        if k[1] in temp_dict:
            res_dict[k[0]] = temp_dict[k[1]]

    # remove non numeric characters from frame rate field
    if 'frame_rate' in res_dict:
        res_dict['frame_rate'] = res_dict['frame_rate'].replace('fps', '')

    # set a default num channels if not available
    if 'Channel Mode' in res_dict:
        if res_dict['Channel Mode'] != 'Single Channel':
            print "NUMERO DI CANALI  ", res_dict['Channel Mode']
        else:
            res_dict['num_channels'] = 1

    return res_dict


def convert_duration(item_info):
    """
    Function used to convert the duration field extracted from the metadata
    to seconds (positive integer value).

    :param item_info: Dictionary that will be updated, editing the Duration field.
    :returns: Updated item metadata dictionary
    """

    if 'Duration' not in item_info:
        return

    # remove all non numeric string at the end
    temp = item_info['Duration'].replace('(approx)', '').replace('s', '').strip().strip()

    # detect the format of the duration - H:MM:SS or decimal seconds
    if ':' in temp:
        l = temp.split(':')
        item_info['Duration'] = int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
    else:
        item_info['Duration'] = int(float(temp))

    return item_info
