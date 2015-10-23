# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.



"""
This module is used to define all scripts necessary to extract the identity
of the faces in a video or image digital item.
Given a digital item it will be analyzed in order to extract this metadata.
"""

#from django.conf import settings
from plugins_script.commons.utils import get_media_root
from plugins_script.commons.item import set_status, get_item, get_status
from plugins_script.commons.keyword import create_keyword
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag, create_uniform_dtags
from plugins_script.commons.person import create_person, set_image, get_person_by_name, get_person
from plugins_script.face_extractor.tools.face_models import FaceModels
from plugins_script.face_extractor.tools.video_face_extractor import VideoFaceExtractor
from plugins_script.face_extractor.tools import constants as c

import plugins_script.commons.training_set_manager as tsm
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


def remove_video_recognitions(auth_dict, param_dict):
    """
    Function used to remove video recognition data

    :param auth_dict: Input parameters provided by the trigger Action
    :param param_dict: Output parameters returned by the trigger Action
    """
    file_path = os.path.join(get_media_root(), param_dict['file'])
    item_id = param_dict['id']

    fe = VideoFaceExtractor(file_path, str(item_id))

    fe.delete_recognition_results()

    return True


def remove_video_data(auth_params, func_params):
    """
    Function used to remove all item models, indexes etc
    when the video item is deleted. This function must be triggered
    as a callback script.

    :param auth_dict: Input parameters provided by the trigger Action
    :param param_dict: Output parameters returned by the trigger Action
    """
    file_path = os.path.join(get_media_root(), func_params['file'])
    item_id = func_params['id']

    fe = VideoFaceExtractor(file_path, str(item_id))

    fe.delete_analysis_results()

    return True


# TODO DELETE?
def update_face_model(auth_dict, param_dict):
    """
    Function used to update global face models
    used as training set for people recognition.

    :param auth_dict: Input parameters provided by the trigger Action
    :param param_dict: Output parameters returned by the trigger Action
    """

    # Get instances associated to model
    model_id = param_dict['id']
    instances = tsm.get_instances_by_model(model_id, auth_params['token'])

    # Get aligned faces from instances
    aligned_faces_list = []
    for instance in instances:
        aligned_face_path = instance['features']
        aligned_faces_list.append(aligned_face_path)

    fm = FaceModels()

    model_file_path = fm.create_model_from_image_list(aligned_faces_list)

    tsm.set_model_file(model_id, model_file_path, auth_params['token'])


def delete_face_model(auth_dict, param_dict):
    """
    Function used to delete face model

    :param auth_dict: Input parameters provided by the trigger Action
    :param param_dict: Output parameters returned by the trigger Action
    """
    
    model_id = param_dict['id']
    
    fm = FaceModels()
    
    fm.delete_model(model_id)
    
    tsm.delete_model(model_id, auth_params['token'])
    
    return ok


# TODO DELETE?
def video_face_extractor(auth_params, func_params):
    """
    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    
    file_path = os.path.join(get_media_root(), func_params['file'])
    item_id = func_params['id']

    # remove existing tags (and dynamic tags) for the item
    tags = get_tags_by_item(func_params['id'], auth_params['token'])
    for tag in tags:
        if tag['type'] == 'face':
            remove_tag(tag['id'], auth_params['token'])


    # extract faces from video and save metadata on filesystem

    # Get available models
    model_type = 'video'
    models = tsm.get_models(model_type, auth_params['token'])['results']

    # Create dictionary with models
    models_list = []
    for model in models:
        model_id = model['id']
        model_file = model['model_file']
        entity_id = model['entity']
        person = get_person(entity_id, auth_params['token'])
        name = person['first_name']
        surname = person['last_name']
        tag = surname + c.TAG_SEP + name

        model_dict = {c.MODEL_ID_KEY: model_id,
                      c.MODEL_FILE_KEY: model_file,
                      c.TAG_KEY: tag
                      }
        models_list.append(model_dict)

    fe = VideoFaceExtractor(file_path, str(item_id), models_list)

    fe.analyze_video()

    set_status(item_id, "FACE_RECOG", auth_params['token'])

    people = fe.get_people()
    
    uniform_tag_ids_arr =[]
    # retrieve dynamic tags and save them on ACTIVE core
    for person_dict in people:

        #print "Tag assegnato al cluster", person_dict['assigned_tag']

        #~ # update the image for the person
        #~ image_path = os.path.join(get_media_root(),'items',
                                  #~ str(item_id), 'Face extraction',
                                  #~ 'Face recognition', 'Key frames',
                                  #~ person_dict[c.KEYFRAME_NAME_KEY])
        #~ set_image(person_id, image_path, 'image/png')

        # check if the person has been recognized
        model_id = person_dict[c.ASSIGNED_LABEL_KEY]
        trusted = False
        instance_id = None
        if model_id == c.UNDEFINED_LABEL:
            print "Creata una nuova persona"
            person = create_person(
                "Unknown", str(func_params['id']) + '_' +
                str(person_dict['person_counter']),
                auth_params['token'])
            person_id = person['id']
            # Create a model for the unknown instance
            model = tsm.create_model(person_id, 'video', person['first_name']+' '+person['last_name'], token=auth_params['token']) 
            instance = tsm.create_instance(model_type, False, model_id=model['id'], token=auth_params['token'])
        else:
            # Create model instance
            instance = tsm.create_instance(
                model_type, trusted, model_id=model_id,
                token=auth_params['token'])
            model = tsm.get_model(model_id)
            person_id = model['entity']

        # update the image for the person
        image_path = os.path.join(fe.rec_path,
                                  c.FACE_RECOGNITION_KEY_FRAMES_DIR,
                                  person_dict[c.KEYFRAME_NAME_KEY])
        set_image(person_id, image_path, 'image/png', auth_params['token'])
        tsm.set_instance_thumbnail(
            instance['id'], image_path, token=auth_params['token'])

        # Get aligned face and set it as instance feature
        print person_dict.keys()
        aligned_face_path = os.path.join(fe.align_path, person_dict[c.MEDOID_ALIGNED_FACE_KEY])
        tsm.set_instance_feature(instance['id'], aligned_face_path, token=auth_params['token'])

        # TODO DELETE?
        # else:
        #     # Find id person by name and surname
        #     tag_parts = person_id.split(c.TAG_SEP)
        #     surname = tag_parts[0]
        #     name = tag_parts[1]
        #     person = create_person(name, surname, auth_params['token'])

        #person_id = person['id']

        #~ if person['image'] == "unknown_user.png":
            #~ set_image(person_id, image_path, 'image/png')


        # create a tag for user name
        #createTagKeyword(item_id, person['first_name'], person['last_name'])

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person_id, "face", auth_params['token'])
        #create audio+video tag
        #uniform_tag = create_tag(item_id, person_id, "face+speaker", auth_params['token'])
        #uniform_tag_ids_arr.append[uniform_tag['id']]

        for segment in person_dict[c.SEGMENTS_KEY]:
            start = segment[c.SEGMENT_START_KEY]
            duration = segment[c.SEGMENT_DURATION_KEY]
            bbox_x, bbox_y, width, height = segment[c.FRAMES_KEY][0][c.DETECTION_BBOX_KEY]

            create_dtag(tag['id'], int(start), int(duration), bbox_x, bbox_y, width, height, auth_params['token'])
    
    """    
    item_status = get_status(item_id, token)
    if "SPEAKER_RECOG" in item_status['status']:       
        #create dtags for audio+video tag
        for u_tag_id in uniform_tag_ids_arr:
            create_uniform_dtags(item_id, u_tag_id, auth_params['token'])
    """
    create_uniform_dtags(item_id, auth_params['token'])


def __build_model(auth_params, func_params):
    """
    This script has been defined in order to build (or update) a 
    face recognition model for a specific person based on a
    set of instances previously extracted and saved.
    The object representation of the model must already exist.
    """
    token = auth_params.get('token', '1234')
    model_id = func_params.get('id', 0)

    # retrieve the entity model object if exists
    model = get_model(model_id, token)
    if model is None:
        raise Exception('The provided model id is not valid!')    

    # retrieve all instances associated to the model
    instances = get_instances_by_model(model_id, token)['results']
    inst_paths = []
    for inst in instances:
        inst_paths.append(os.path.join(get_media_root(), inst['features']))
        
    fm = FaceModels()
    
    model_file_path = fm.create_model_from_image_list(aligned_faces_list)
    
    tsm.set_model_file(model_id, model_file_path, token=token)
    
    
def __recognize_instance(auth_params, func_params):
    """
    This script has been defined in order to recognize
    face instances that are saved into the database
    according to existent models
    """
    try:
        token = auth_params.get('token', '1234')
        instance_id = func_params["id"]
        instance_path = os.path.join(
            get_media_root(), func_params["features"])

        # Get available models
        model_type = 'video'
        models = tsm.get_models(model_type, auth_params['token'])

        # Create dictionary with models
        models_list = []
        for model in models:
            model_id = model['id']
            model_file = os.path.join(
                get_media_root(), model['model_file'])
            model_dict = {c.MODEL_ID_KEY: model_id,
                          c.MODEL_FILE_KEY: model_file,
                          }
            models_list.append(model_dict)

        fm = FaceModels(models_list)

        # Recognize given instance
        face = cv2.imread(instance_path, cv2.IMREAD_GRAYSCALE)
        (model_id, conf) = fm.recognize_face(face)

        # update the instance reference if recognized
        if model_id != c.UNDEFINED_LABEL:
            edit_instance(instance_id, model_id=label, token=token)
            return 'Instance ' + instance_id + ' associated to model ' + model_id
        return 'Instance ' + instance_id + ' not recognized by any model'

        # TODO modificare i dynamic tag per associare automaticamente la persona ?

    except Exception as e:
        print e
        return 'Error on instance recognition'


def __generate_instances(auth_params, func_params):
    """
    @param auth_params: Input parameters of the function
                        that generate this function call
    @param func_params: Output parameters of the function
                        that generate this function call
    """
    
    file_path = os.path.join(get_media_root(), func_params['file'])
    item_id = func_params['id']

    # remove existing tags (and dynamic tags) for the item
    tags = get_tags_by_item(func_params['id'], auth_params['token'])
    for tag in tags:
        if tag['type'] == 'face':
            remove_tag(tag['id'], auth_params['token'])


    # extract faces from video and save metadata on filesystem

    # Get available models
    model_type = 'video'
    models = tsm.get_models(model_type, auth_params['token'])

    # Create dictionary with models
    models_list = []
    for model in models:
        model_id = model['id']
        model_file = os.path.join(
            get_media_root(), model['model_file'])
        entity_id = model['entity']
        person = get_person(entity_id, auth_params['token'])
        name = person['first_name']
        surname = person['last_name']
        tag = surname + c.TAG_SEP + name

        model_dict = {c.MODEL_ID_KEY: model_id,
                      c.MODEL_FILE_KEY: model_file,
                      c.TAG_KEY: tag
                      }
        models_list.append(model_dict)

    fe = VideoFaceExtractor(file_path, str(item_id), models_list)

    fe.analyze_video()

    set_status(item_id, "FACE_RECOG", auth_params['token'])

    people = fe.get_people()
    
    uniform_tag_ids_arr = []
    # retrieve dynamic tags and save them on ACTIVE core
    for person_dict in people:

        #print "Tag assegnato al cluster", person_dict['assigned_tag']

        #~ # update the image for the person
        #~ image_path = os.path.join(get_media_root(),'items',
                                  #~ str(item_id), 'Face extraction',
                                  #~ 'Face recognition', 'Key frames',
                                  #~ person_dict[c.KEYFRAME_NAME_KEY])
        #~ set_image(person_id, image_path, 'image/png')

        # check if the person has been recognized
        model_id = person_dict[c.ASSIGNED_LABEL_KEY]
        trusted = False
        instance_id = None
        if model_id == c.UNDEFINED_LABEL:
            print "Creata una nuova persona"
            person = create_person(
                "Unknown", str(func_params['id']) + '_' +
                str(person_dict['person_counter']),
                auth_params['token'])
            person_id = person['id']
            # Create a model for the unknown instance
            model = tsm.create_model(
                person_id, 'video',
                person['first_name'] + ' ' + person['last_name'],
                token=auth_params['token'])
            instance = tsm.create_instance(
                model_type, False, model_id=model['id'],
                token=auth_params['token'])
        else:
            # Create model instance
            instance = tsm.create_instance(
                model_type, trusted, model_id=model_id,
                token=auth_params['token'])
            model = tsm.get_model(model_id)
            person_id = model['entity']

        # update the image for the person
        image_path = os.path.join(fe.rec_path,
                                  c.FACE_RECOGNITION_KEY_FRAMES_DIR,
                                  person_dict[c.KEYFRAME_NAME_KEY])
        set_image(person_id, image_path, 'image/png', auth_params['token'])
        tsm.set_instance_thumbnail(
            instance['id'], image_path, token=auth_params['token'])

        # Get aligned face and set it as instance feature
        print person_dict.keys()
        aligned_face_path = os.path.join(fe.align_path, person_dict[c.MEDOID_ALIGNED_FACE_KEY])
        tsm.set_instance_feature(instance['id'], aligned_face_path, token=auth_params['token'])

        # TODO DELETE?
        # else:
        #     # Find id person by name and surname
        #     tag_parts = person_id.split(c.TAG_SEP)
        #     surname = tag_parts[0]
        #     name = tag_parts[1]
        #     person = create_person(name, surname, auth_params['token'])

        #person_id = person['id']

        #~ if person['image'] == "unknown_user.png":
            #~ set_image(person_id, image_path, 'image/png')


        # create a tag for user name
        #createTagKeyword(item_id, person['first_name'], person['last_name'])

        # create a tag (occurrence of a person in a digital item)
        tag = create_tag(item_id, person_id, "face", auth_params['token'])
        #create audio+video tag
        #uniform_tag = create_tag(item_id, person_id, "face+speaker", auth_params['token'])
        #uniform_tag_ids_arr.append[uniform_tag['id']]

        for segment in person_dict[c.SEGMENTS_KEY]:
            start = segment[c.SEGMENT_START_KEY]
            duration = segment[c.SEGMENT_DURATION_KEY]
            bbox_x, bbox_y, width, height = segment[c.FRAMES_KEY][0][c.DETECTION_BBOX_KEY]

            create_dtag(tag['id'], int(start), int(duration), bbox_x, bbox_y,
                        width, height, auth_params['token'])
    
    """    
    item_status = get_status(item_id, token)
    if "SPEAKER_RECOG" in item_status['status']:       
        #create dtags for audio+video tag
        for u_tag_id in uniform_tag_ids_arr:
            create_uniform_dtags(item_id, u_tag_id, auth_params['token'])
    """
    create_uniform_dtags(item_id, auth_params['token'])


def image_face_extractor(auth_params, func_params):
    """
    @param auth_params: Input parameters of the function that generate this function call
    @param func_params: Output parameters of the function that generate this function call
    """
    pass

