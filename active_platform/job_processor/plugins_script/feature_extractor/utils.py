# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""
This module is used to extract all available metadata contained in a digital item.
When item metadata has been extracted it is saved on the ACTIVE core, using the proxy methods
that ill invoke the REST API.
"""

from plugins_script.commons.utils import get_media_root
from plugins_script.commons.item  import set_status, set_metadata
import subprocess
import os


def extract_metadata(auth_params, func_params):
    """
    This function is used to extract relevant metadata from a
    digital item and then save this data on the ACTIVE Core.

    :param auth_params: Authentication parameters
    :param func_params: Function parameters
    """
    file_path = os.path.join(get_media_root(), func_params['file'])
    item_info = get_exif_metadata(file_path)
    token = auth_params['token']

    if not set_metadata(func_params['id'], item_info, token):
        raise Exception('Error on metadata update')

    if not set_status(func_params['id'], 'ANALYZED', token):
        raise Exception('Error on processing status update')

    print 'Extracted and saved metadata for digital item', func_params['id']


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
