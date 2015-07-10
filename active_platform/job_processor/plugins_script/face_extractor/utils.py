"""
This module is used to define all scripts necessary to extract the identity
of the faces in a video or image digital item.
Given a digital item it will be analyzed in order to extract this metadata.
"""

from django.conf import settings
from plugins_script.commons.item import set_status
from plugins_script.commons.keyword import create_keyword
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag
from plugins_script.commons.person import create_person, set_image, get_person_by_name
from plugins_script.face_extractor.tools.video_face_extractor import VideoFaceExtractor
from plugins_script.face_extractor.tools import constants as c

import os


def createTagKeyword(item_id, first_name, last_name, token='Bearer 1234'):
    """
    Funzione temporanea utilizzata per creare una
    keyword contenente il nome della persona e
    associarla all'item in cui compare.
    Necessaria solo per la ricerca nella demo di sinnova!
    """
    k1 = create_keyword(first_name, token)
    k2 = create_keyword(last_name, token)
   
    t1 = create_tag(item_id, k1['id'], 'keyword', token)
    t2 = create_tag(item_id, k2['id'], 'keyword', token)


def remove_video_data(auth_params, func_params):
    """
    Function used to remove all item models, indexes etc
    when the video item is deleted. This function must be triggered
    as a callback script.

    :param auth_dict: Input parameters provided by the trigger Action
    :param param_dict: Output parameters returned by the trigger Action
    """
    #print settings.MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
    item_id = func_params['id']

    fe = VideoFaceExtractor(file_path, str(item_id))

    fe.delete_analysis_results()

    return True




def video_face_extractor(auth_params, func_params):
    """
    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    
    file_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
    item_id = func_params['id']

    # remove existing tags (and dynamic tags) for the item
    tags = get_tags_by_item(func_params['id'], auth_params['token'])
    for tag in tags:
        if tag['type'] == 'face':
            remove_tag(tag['id'], auth_params['token'])


    # extract faces from video and save metadata on filesystem
    
    fe = VideoFaceExtractor(file_path, str(item_id))
    fe.analyze_video()

    set_status(item_id, "FACE_RECOG", auth_params['token'])

    people = fe.get_people()


    # retrieve dynamic tags and save on ACTIVE core
    for person_dict in people:

        #print "Tag assegnato al cluster", person_dict['assigned_tag']

        #~ # update the image for the person
        #~ image_path = os.path.join(settings.MEDIA_ROOT,'items',
                                  #~ str(item_id), 'Face extraction',
                                  #~ 'Face recognition', 'Key frames',
                                  #~ person_dict[c.KEYFRAME_NAME_KEY])
        #~ set_image(person_id, image_path, 'image/png')

        # check the person has been recognized (create new one?)
        person_id = person_dict[c.ASSIGNED_TAG_KEY]
        if person_id == c.UNDEFINED_TAG:
            print "Creata una nuova persona"
            person = create_person("Unknown", str(func_params['id'])+'_'+str(person_dict['person_counter']), auth_params['token'])

        else:
            # Find id person by name and surname
            tag_parts = person_id.split(c.TAG_SEP)
            surname = tag_parts[0]
            name = tag_parts[1]
            person = create_person(name, surname, auth_params['token'])

        person_id = person['id']
        
        # update the image for the person
        image_path = os.path.join(settings.MEDIA_ROOT,'items',
                                  str(item_id), 'Face extraction',
                                  'Face recognition', 'Key frames',
                                  person_dict[c.KEYFRAME_NAME_KEY])
        set_image(person_id, image_path, 'image/png', auth_params['token'])
        #~ if person['image'] == "unknown_user.png":
            #~ set_image(person_id, image_path, 'image/png')


        # create a tag for user name
        #createTagKeyword(item_id, person['first_name'], person['last_name'])
        

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person_id, "face", auth_params['token'])

        for segment in person_dict[c.SEGMENTS_KEY]:
            start       = segment[c.SEGMENT_START_KEY]
            duration    = segment[c.SEGMENT_DURATION_KEY]
            bbox_x, bbox_y, width, height = segment[c.FRAMES_KEY][0][c.DETECTION_BBOX_KEY]

            create_dtag(tag['id'], int(start), int(duration), bbox_x, bbox_y, width, height, auth_params['token'])


def image_face_extractor(auth_params, func_params):
    """
    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    pass

