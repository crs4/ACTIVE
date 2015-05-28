"""
This module is used to define all scripts necessary to extract the identity
of the faces in a video or image digital item.
Given a digital item it will be analyzed in order to extract this metadata.
"""

from django.conf import settings
from plugins_script.commons.item import set_status
from plugins_script.commons.tags import create_tag, create_dtag
from plugins_script.commons.person import create_person
from tools.face_extractor import FaceExtractor

import os


def video_face_extractor(func_in, func_out):
    """
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """
    fe = FaceExtractor()
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_id = func_out['id']

    print func_in
    print func_out


    # extract faces from video and save metadata on filesystem
    fe.analizeVideo(file_path)

    set_status(item_id, "FACE_RECOG")


    # retrieve dynamic tags and save on ACTIVE core
    for person_dict in fe.recognized_faces:

        #print "Tag assegnato al cluster", person_dict['assigned_tag']

        # check the person has been recognized (create new one?)
        #person = person_dict['assigned_tag']
        #if person == 0:
        print "Creata una nuova persona"
        person = create_person("Unknown", "Person")

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person['id'], "face")

        for segment in person_dict['segments']:
            start       = segment['segment_start']
            duration    = segment['segment_duration']
            bbox_x, bbox_y, width, height = segment['images'][0]['detection_bbox']

            dtag = create_dtag(tag['id'], int(start), int(duration), bbox_x, bbox_y, width, height)


def image_face_extractor(func_in, func_out):
    """
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """
    pass
