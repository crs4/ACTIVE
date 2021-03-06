# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been defined in order to handle the manipulation of 
item data through CRUD operations.
In this case it is possible to set the value of some fields
using a JSON representation of the object. Updated data will be
sent to the ACTIVE core through the REST API.
"""

from django.conf import settings
import requests


def get_item(item_id, token=None):
    """
    Method used to update the thumbnail associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param item_id: Id of the considered item.
    @param token: Authentication token necessary to invoke the REST API.
    @return: Result of the file retrieval.
    """

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def set_metadata(item_id, values, token=None):
    """
    Method used to update the digital item metadata using a
    dictionary with all fields that must be updated.
    For each digital item type a different endpoint will be used and
    all unnecessary fields will be ignored.
    
    @param item_id: Id of the considered digital item.
    @param values: Dictionary containing updated metadata values.
    @param token: Authentication token necessary to invoke the REST API
    @return: The result of the metadata update.
    """
    # retrieve the digital item
    item = get_item(item_id, token)
    if item is None:
        return False
    
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + item['type'] + '/' + str(item_id) + '/'
    r = requests.put(url, {'mime_type'      : values.get('mime_type', 'application/octet-stream'),
                           'frame_width'    : values.get('frame_width', 0),
                           'frame_height'   : values.get('frame_height', 0),
                           'frame_rate'     : values.get('frame_rate', 0),
                           'duration'       : values.get('duration', 0),
                           'filesize'       : values.get('filesize', 0),
                           'sample_rate'    : values.get('sample_rate', 0),
                           'num_channels'   : values.get('num_channels', 1),
                           'bits_per_sample': values.get('bits_per_sample', 0)
                     },
                     headers={'Authorization': token})
    # return the result of the update
    return r.status_code == requests.codes.ok

"""
def set_video_metadata(item_id, values, token=None):
    
    Method used to update video item metadata using a
    dictionary with all filed that must be updated and associated
    to specific item fields.
    
    @param item_id: Id of the video item that will be considered.
    @param values: Dictionary containing update metadata values.
    @param token: Authentication token necessary to invoke the REST API
    @return: The result of the metadata update.

    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, {'mime_type'    : values['mime_type'],
                           'frame_width'  : values['frame_width'],
                           'frame_height' : values['frame_height'],
                           'frame_rate'   : values['frame_rate'],
                           'duration'     : values['duration'],
                           'format'       : values['format'],
                           'filesize'     : values['filesize']},
                     headers=header)
    # return the result of the update
    return r.status_code == requests.codes.ok


def set_image_metadata(item_id, values, token=None):
    Method used to update image item metadata using a dictionary with 
    all filed that must be updated and associated to specific item fields.
    
    @param item_id: Id of the image item that will be considered.
    @param values: Dictionary containing update metadata values.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The result of the metadata update.
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(item_id) + '/'
    header = {'Authorization' : token}
    r = requests.put(url, {'mime_type'    : values['mime_type'],
                           'frame_width'  : values['frame_width'],
                           'frame_height' : values['frame_height'],
                           'format'       : values['format'],
                           'filesize'     : values['filesize']},
                     headers=header)
    # return the result of the update
    return r.status_code == requests.codes.ok


def set_audio_metadata(item_id, values, token=None):
    Method used to update audio item metadata using a dictionary with
    all filed that must be updated and associated to specific item fields.

    @param item_id: Id of the audio item that will be considered.
    @param values: Dictionary containing update metadata values.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The result of the metadata update.
    
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, {#'id'              : item_id,
                           'mime_type'       : values['mime_type'],
                           'duration'        : values['duration'],
                           'sample_rate'     : values.get('sample_rate', 0),
                           'num_channels'    : values.get('num_channels', 1),
                           'bits_per_sample' : values.get('bits_per_sample', 0),
                           'format'          : values['format'],
                           'filesize'        : values['filesize']},
                     headers=header)
    # return the result of the update
    return r.status_code == requests.codes.ok
"""

def set_status(item_id, status_type, token=None):
    """
    Method used to update the processing status associated to an item.
    If the item has already been labelled with the metadata extraction
    the status value doesn't change.

    @param item_id: Id of the item that will be considered
    @param status_type: Status that will be associated to the item
    @param token: Authentication token necessary to invoke the REST API.
    @return: The result of the uploading phase
    """
    # retrieve the current processing status
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    status = r.json()['state']

    if status_type not in status:
        if len(status) > 0:
            status += ', '
        status += status_type

    # update the processing status for the considered item
    r = requests.put(url, {#'id' : item_id, 
                           'state' : status}, headers=header)

    return r.status_code == requests.codes.ok

def get_status(item_id, token=None):
    """
    Method used to obtain the processing status associated to an item.
    

    @param item_id: Id of the item that will be considered
    @param token: Authentication token necessary to invoke the REST API.
    @return: The status of the item
    """
    # retrieve the current processing status
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    status = r.json()['state']

    return status

def set_preview(item_id, file_path, file_mime, token=None):
    """
    Method used to update the preview associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param item_id: Id of the considered item.
    @param file_path: Path to file that will be sent.
    @param file_mime: MIME type of the preview file.
    @param token: Authentication token necessary to invoke the REST API.
    @return: Result of the file update
    """
    f = open(file_path, 'rb')
    dest_file = 'preview.' + file_mime.split('/')[1]
    multiple_files = [('preview', (dest_file, f, file_mime)), ]

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=multiple_files, headers=header)

    return r.status_code == requests.codes.ok


def set_thumbnail(item_id, file_path, file_mime, token=None):
    """
    Method used to update the thumbnail associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param item_id: Id of the considered item.
    @param file_path: Path to file that will be sent.
    @param file_mime: MIME type of the thumbnail file.
    @param token: Authentication token necessary to invoke the REST API.
    @return: Result of the file update.
    """
    f = open(file_path, 'rb')
    dest_file = 'thumbnail.' + file_mime.split('/')[1]
    multiple_files = [('thumb', (dest_file, f, file_mime)), ]

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=multiple_files, headers=header)

    return r.status_code == requests.codes.ok


def set_values(item_id, values, token=None):
    """
    Method used to update the fields of a generic item object, using a dictionary with
    all fileds that must be updated.

    @param item_id: Id of the digital item that will be considered.
    @param values: Dictionary containing update metadata values.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The result of the metadata update.
    """
    # set only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, values, headers=header)
    # return the result of the update
    return r.status_code == requests.codes.ok


