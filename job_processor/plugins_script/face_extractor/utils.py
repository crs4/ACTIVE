"""
This module is used to define all scripts necessary to extract the identity
of the faces in a video or image digital item.
Given a digital item it will be analyzed in order to extract this metadata.
"""

from django.conf import settings
from plugins_script.commons.item import set_status
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag
from plugins_script.commons.person import create_person, set_image
from plugins_script.face_extractor.tools.video_face_extractor import VideoFaceExtractor
from plugins_script.face_extractor.tools import constants as c

import os




# TODO rimuovere le cartelle degli item quando vengono cancellati da core!
def remove_data_data(func_in, func_out):
    """
    Function used to remove all item models, indexes etc
    when the item is deleted. This function must be triggered
    as a callback script.

    :param func_in: Input parameters provided by the trigger Action
    :param func_out: Output parameters returned by the trigger Action
    """
    print "CANCELLARE I METADATI DEGLI ITEM!!!"




def video_face_extractor(func_in, func_out):
    """
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """
    
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_id = func_out['id']

    # remove existing tags (and dynamic tags) for the item
    tags = get_tags_by_item(func_out['id'])
    for tag in tags:
        remove_tag(tag['id'])


    # extract faces from video and save metadata on filesystem
    
    fe = VideoFaceExtractor(file_path, str(item_id))
    fe.analyze_video()

    set_status(item_id, "FACE_RECOG")

    people = fe.get_people()


    # retrieve dynamic tags and save on ACTIVE core
    for person_dict in people:

        #print "Tag assegnato al cluster", person_dict['assigned_tag']

        # check the person has been recognized (create new one?)
        person_id = person_dict[c.ASSIGNED_TAG_KEY]
        if person_id == c.UNDEFINED_TAG:
            print "Creata una nuova persona"
            person = create_person("Unknown", "Person")
            person_id = person['id']

        # update the image for the person
        image_path = os.path.join(settings.MEDIA_ROOT, 'video_indexing',
                                  str(item_id), 'Frames',
                                  person_dict[c.MEDOID_FRAME_NAME_KEY])
        set_image(person_id, image_path, 'image/png')

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person_id, "face")

        for segment in person_dict[c.SEGMENTS_KEY]:
            start       = segment[c.SEGMENT_START_KEY]
            duration    = segment[c.SEGMENT_DURATION_KEY]
            bbox_x, bbox_y, width, height = segment[c.FRAMES_KEY][0][c.DETECTION_BBOX_KEY]

            create_dtag(tag['id'], int(start), int(duration), bbox_x, bbox_y, width, height)


def image_face_extractor(func_in, func_out):
    """
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """
    pass