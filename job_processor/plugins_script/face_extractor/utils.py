"""
This module is used to define all scripts necessary to extract the identity
of the faces in a video or image digital item.
Given a digital item it will be analyzed in order to extract this metadata.
"""

from django.conf import settings
from plugins_script.commons.item import set_status, get_item
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag
from plugins_script.commons.person import create_person, set_image, get_person
from plugins_script.face_extractor.tools.face_models import FaceModels
from plugins_script.face_extractor.tools.video_face_extractor import VideoFaceExtractor
from plugins_script.face_extractor.tools import constants as c
from skeleton.skeletons import Seq, Farm
from skeleton.visitors import Executor
import os

def remove_video_recognitions(func_in, func_out):
    """
    Function used to remove video recognition data

    :param func_in: Input parameters provided by the trigger Action
    :param func_out: Output parameters returned by the trigger Action
    """
    print settings.MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_id = func_out['id']

    fe = VideoFaceExtractor(file_path, str(item_id))

    fe.delete_recognition_results()

    return True


def remove_video_data(func_in, func_out):
    """
    Function used to remove all item models, indexes etc
    when the video item is deleted. This function must be triggered
    as a callback script.

    :param func_in: Input parameters provided by the trigger Action
    :param func_out: Output parameters returned by the trigger Action
    """
    print settings.MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_id = func_out['id']

    fe = VideoFaceExtractor(file_path, str(item_id))

    fe.delete_analysis_results()

    return True

"""
def video_face_extractor(func_in, func_out):
    ""
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    ""
    seq = Seq(_video_face_extractor)
    return Executor().eval(seq, [func_in, func_out])
"""


def update_face_model(func_in, func_out):
    """
    Function used to update global face models 
    used as training set for face recognition.

    :param func_in: Input parameters provided by the trigger Action
    :param func_out: Output parameters returned by the trigger Action
    """
    
    tag_id = func_out['id']
    person_id = func_out['entity']
    item_id = func_out['item']

    person = get_person(person_id)
    if not person:
        print "Persona non trovata!!! ", person_id
        
    item = get_item(item_id)
    if not item:
        print "Item non trovato!!!", item_id
        
    if person and item:        

        name = person['first_name']
        surname = person['last_name']
        tag = surname + c.TAG_SEP + name


        file_path = os.path.join(settings.MEDIA_ROOT, item['file'])
        print file_path

        fe = VideoFaceExtractor(file_path, str(item_id))

        person_counter = fe.get_person_counter(tag_id)

        if person_counter:
            fe.add_keyface_to_models(person_id, person_counter, tag)


def delete_face_model(func_in, func_out):
    """
    Function used to delete face model related to deleted person.

    :param func_in: Input parameters provided by the trigger Action
    :param func_out: Output parameters returned by the trigger Action
    """
    
    person_id = func_out['id']
    
    fm = FaceModels()
    
    ok = fm.remove_label(person_id)
    
    return ok
    

def video_face_extractor(func_in, func_out):
    """
    Function used to extract dynamic tags from a video item.
    
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call

    :param params: Parameters used by this function
    :return: The result
    """

    #func_in = params[0]
    #func_out = params[1]
    
    file_path = os.path.join(settings.MEDIA_ROOT, func_out['file'])
    item_id = func_out['id']

    # TO BE DELETED?
    # remove existing tags (and dynamic tags) for the item
    tags = get_tags_by_item(func_out['id'])
    for tag in tags:
        remove_tag(tag['id'])

    # os.environ['TESSDATA_PREFIX'] = '/var/spool/active/job_processor/plugins_script/face_extractor/tools/'
    # print ('TESSDATA_PREFIX', os.environ['TESSDATA_PREFIX'])


    # extract faces from video and save metadata on filesystem
    
    fe = VideoFaceExtractor(file_path, str(item_id))
    fe.analyze_video()

    set_status(item_id, "FACE_RECOG")

    people = fe.get_people()


    # retrieve dynamic tags and save on ACTIVE core
    for person_dict in people:

        print "Tag assegnato al cluster", person_dict['assigned_tag']

        # check the person has been recognized (create new one?)
        person_id = person_dict[c.ASSIGNED_LABEL_KEY]
        if person_id == c.UNDEFINED_LABEL:
            print "Creata una nuova persona"
            person = create_person("Unknown", "Person" + str(people.index(person_dict)) + '_' + str(item_id))
            person_id = person['id']

        # update the image for the person
        image_path = os.path.join(settings.MEDIA_ROOT, 'video_indexing',
                                  str(item_id), c.FACE_RECOGNITION_DIR,
                                  c.FACE_RECOGNITION_KEY_FRAMES_DIR,
                                  person_dict[c.KEYFRAME_NAME_KEY])
        set_image(person_id, image_path, 'image/png')

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person_id, "face")
        
        person_counter = person_dict[c.PERSON_COUNTER_KEY]
        tag_id = tag['id']
        fe.store_tag_id(person_counter, tag_id)

        for segment in person_dict[c.SEGMENTS_KEY]:
            start       = segment[c.SEGMENT_START_KEY]
            duration    = segment[c.SEGMENT_DURATION_KEY]
            bbox_x, bbox_y, width, height = segment[c.FRAMES_KEY][0][c.DETECTION_BBOX_KEY]

            dtag = create_dtag(
            tag['id'], int(start), int(duration), bbox_x, bbox_y, width, height)
     
    # YAML file with recognition results must be updated 
    # in order to permanently store tag ids       
    fe.update_rec_file()


def image_face_extractor(func_in, func_out):
    """
    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """
    pass
