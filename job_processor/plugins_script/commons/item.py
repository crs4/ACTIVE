"""
This module has been defined in order to handle the manipulation of 
item data through CRUD operations.
In this case it is possible to set the value of some fields
using a JSON representation of the object. Updated data will be
sent to the ACTIVE core through the REST API.
"""

from django.conf import settings
import requests


def set_video_metadata(item_id, values):
    """
    Method used to update video item metadata using a
    dictionary with all filed that must be updated and associated
    to specific item fields.
    
    :param item_id: Id of the video item that will be considered.
    :param values: Dictionary containing update metadata values.
    :return: The result of the metadata update.
    """
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/video/' + str(item_id) + '/'
    r = requests.put(url, {'id'           : item_id,
                           'mime_type'    : values['mime_type'],
                           'frame_width'  : values['frame_width'],
                           'frame_height' : values['frame_height'],
                           'frame_rate'   : values['frame_rate'],
                           'duration'     : values['duration'],
                           'format'       : values['format'],
                           'filesize'     : values['filesize'] })
    # return the result of the update
    return r.status_code == requests.codes.ok


def set_image_metadata(item_id, values):
    """
    Method used to update image item metadata using a dictionary with 
    all filed that must be updated and associated to specific item fields.
    
    :param item_id: Id of the image item that will be considered.
    :param values: Dictionary containing update metadata values.
    :return: The result of the metadata update.
    """
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/image/' + str(item_id) + '/'
    r = requests.put(url, {'id'           : item_id,
                           'mime_type'    : values['mime_type'],
                           'frame_width'  : values['frame_width'],
                           'frame_height' : values['frame_height'],
                           'format'       : values['format'],
                           'filesize'     : values['filesize'] })
    # return the result of the update
    return r.status_code == requests.codes.ok


def set_audio_metadata(item_id, values):
    """
    Method used to update audio item metadata using a dictionary with
    all filed that must be updated and associated to specific item fields.

    :param item_id: Id of the audio item that will be considered.
    :param values: Dictionary containing update metadata values.
    :return: The result of the metadata update.
    """
    # extract only the needed fields
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/audio/' + str(item_id) + '/'
    r = requests.put(url, {'id'              : item_id,
                           'mime_type'       : values['mime_type'],
                           'duration'        : values['duration'],
                           'sample_rate'     : values.get('sample_rate', 0),
                           'num_channels'    : values.get('num_channels', 1),
                           'bits_per_sample' : values.get('bits_per_sample', 0),
                           'format'          : values['format'],
                           'filesize'        : values['filesize'] })
    # return the result of the update
    return r.status_code == requests.codes.ok


def set_status(item_id, status_type):
    """
    Method used to update the processing status associated to an item.
    If the item has already been labelled with the metadata extraction
    the status value doesn't change.

    :param item_id: Id of the item that will be considered
    :param status_type: Status that will be associated to the item
    :return: The result of the uploading phase
    """
    # retrive the current processing status
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    r = requests.get(url)
    status = r.json()['state']

    if status_type not in status:
        if len(status) > 0:
            status += ', '
        status += status_type

    # update the processing status for the considered item
    r = requests.put(url, {'id' : item_id, 'state' : status})

    return r.status_code == requests.codes.ok


def set_preview(item_id, file_path, file_mime):
    """
    Method used to update the preview associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    :param item_id: Id of the considered item.
    :param file_path: Path to file that will be sent.
    :param file_mime: MIME type of the preview file.
    :return: Result of the file update
    """
    f = open(file_path, 'rb')
    dest_file = 'preview.' + file_mime.split('/')[1]
    multiple_files = [('preview', (dest_file, f, file_mime)), ]

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    r = requests.put(url, files=multiple_files)

    return r.status_code == requests.codes.ok


def set_thumbnail(item_id, file_path, file_mime):
    """
    Method used to update the thumbnail associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    :param item_id: Id of the considered item.
    :param file_path: Path to file that will be sent.
    :param file_mime: MIME type of the thumbnail file.
    :return: Result of the file update.
    """
    f = open(file_path, 'rb')
    dest_file = 'thumbnail.' + file_mime.split('/')[1]
    multiple_files = [('thumb', (dest_file, f, file_mime)), ]

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    r = requests.put(url, files=multiple_files)

    return r.status_code == requests.codes.ok


def get_item(item_id):
    """
    Method used to update the thumbnail associate to an item.
    Providing the item id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    :param item_id: Id of the considered item.
    :return: Result of the file retrieval.
    """

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/items/' + str(item_id) + '/'
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        return None
    return r.json()








