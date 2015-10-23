# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has defines a proxy for the REST API provided to handle models and dataset instances.
It is possible to perform the main CRUD operations over this type of objects.
All operations are executed using JSON serialized objects.
"""

from django.conf import settings
import requests


def get_models(model_type=None, token=None):
    """
    Method used to retrieve all stored models.
    It is possible to filter available models by their type.

    @param model_type: The type of models that will be considered
    @type model_type: String
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: List of JSON serialized model objects
    """
    
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/'
    if model_type is not None:
        url += '?type=' + model_type
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    
    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def get_model(model_id, token=None):
    """
    Method used to retrieve a specific model object by its id.

    @param model_id: Id of the considered item.
    @type model_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: A JSON serialized model object
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/' + str(model_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_models_by_entity(entity_id, token=None):
    """
    Method used to retrieve all stored Model objects associated to a specific entity.

    @param entity_id: The id of the entity which Model objects are associated to.
    @type entity_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The EntityModel objects associated to the given entity, None in case of error.
    @rtype: List of JSON serialized EntityModel objects
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/entitysearch/' + str(entity_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def create_model(entity_id, type, name=None, last_update=None, token=None):
    """
    Method used to create a new model object providing all necessary data.

    @param entity_id: The id of the Entity associated to the model
    @type entity_id: int
    @param type: The type of the model (and also managed data)
    @type type: String    
    @param last_update: The timestamp when the model has been updated/recomputed
    @type last_update: datetime
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: List of JSON serialized model objects
    """
    
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/'
    header = {'Authorization': token}
    model = {'name': name, 'type': type, 'entity': entity_id, 'last_update': last_update}
    r = requests.post(url, model, headers=header)
    
    # check if the model has been created correctely
    if r.status_code != requests.codes.created:
        return None
    return r.json()

def set_model_file(model_id, file_path, token=None):
    """
    Method used to update the model file associated to a Model object.
    Providing the model id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param model_id: Id of the considered model.
    @type model_id: int
    @param file_path: Path to the model file that will be sent.
    @type file_path: String
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file update
    @rtype: bool
    """
    files = [('model_file', open(file_path, 'rb')), ]
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/' + str(model_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=files, headers=header)
    # check if the file has been updated correctely 
    return r.status_code == requests.codes.ok

#def edit_model(model_id, entity_id=None, type=None, name=None, model_file_path=None, last_update=None, token=None):
def edit_model(model_id, entity_id=None, type=None, name=None, last_update=None, token=None):
    """
    Method used to edit the data associated to a EntityModel object.
    It returns the updated object if data is correctly edited, None in case of error.

    @param model_id: The id of the model that will be updated.
    @type model_id: String
    @param entity_id: The id of the entity recognized by the model.
    @type entity_id: int
    @param type: Type of models (and managed files).
    @type type: String
    @param name: Name or description associated to the model.
    @type name: String
    @param model_file_path: Path of the file containing the model.
    @type model_file_path: String
    @param last_update: Time od the last model update.
    @type last_update: Datetime
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The object containing the updated person, None in case of error.
    @rtype: JSON serialized model object
    """
    data = {}
    if name is not None:
        data['name'] = name
#    if model_file_path is not None:
#        data['model_file'] = model_file_path
    if entity_id is not None:
        data['entity'] = entity_id
    if type is not None:
        data['type'] = type
    if last_update is not None:
        data['last_update'] = last_update

    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/' + str(model_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, data, headers=header)
    
    # check if the model has been updated correctely
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def delete_model(model_id, token=None):
    """
    Method used to retrieve a specific model object by its id.

    @param model_id: Id of the considered EntityModel object.
    @type model_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The result of model deletion.
    @rtype: bool
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/' + str(model_id) + '/'
    header = {'Authorization': token}
    r = requests.delete(url, headers=header)
    
    # check if the model has been deleted correctly
    return r.status_code == requests.codes.no_content


def get_instances(trusted=None, used=None, token=None):
    """
    Method used to retrieve all stored Instance objects.
    It is possible to filter available Instance objects by their computation
    status and/or usage (if they are associated to any existing model).

    @param trusted: The type of models that will be considered
    @type trusted: String
    @param used: Flags used to detect if a Instance object is associated to a model.
    @type used: bool
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: List of JSON serialized model objects
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/'
    if used is not None:
        url += '?used=' + str(used)

    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    
    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def get_instances_by_model(model_id, token=None):
    """
    Method used to retrieve all stored Instance objects associated to a specific model.
    It is  possible to filter available Instance objects by their computation
    status and/or usage (if they are associated to any existing model).

    @param model_id: The id of the model which Instances objects are associated to.
    @type model_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The Instance objects associated to the given model, None in case of error.
    @rtype: List of JSON serialized Instance objects
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/models/instancesearch/' + str(model_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    
    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def get_instance(instance_id, token=None):
    """
    Method used to retrieve a specific model object by its id.

    @param model_id: Id of the considered item.
    @type model_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: A JSON serialized model object
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/' + str(instance_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)
    
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def create_instance(type, trusted, model_id=None, token=None):
    """
    Method used to create a new model object providing all necessary data.

    @param type: The type of the instance
    @type type: String
    @param trusted: A flag variable set by the user for model computation
    @type trusted: bool
    @param model_id: The model id which the Instance object is associated to
    @type model_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file retrieval, None in case of error.
    @rtype: List of JSON serialized model objects
    """
    data = {'type': type, 'trusted': trusted}
    if model_id is not None:
        data['entity_model'] = model_id
    
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/'
    header = {'Authorization': token}
    r = requests.post(url, data, headers=header)
    
    # check if the model has been created correctely
    if r.status_code != requests.codes.created:
        return None
    return r.json()

def set_instance_thumbnail(instance_id, thumb_path, token=None):
    """
    Method used to update the thumbnail associated to a Instance object.
    Providing the instance id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param instance_id: Id of the considered item.
    @type instance_id: int
    @param thumb_path: Path to the thumbnail file that will be sent.
    @type thumb_path: String
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file update
    @rtype: bool
    """
    files = [('thumbnail', open(thumb_path, 'rb')), ]
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/' + str(instance_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=files, headers=header)
    # check if the file has been updated correctely
    return r.status_code == requests.codes.ok

def set_instance_feature(instance_id, feature_path, token=None):
    """
    Method used to update the feature file associated to a Instance object.
    Providing the instance id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param instance_id: Id of the considered item.
    @type instance_id: int
    @param feature_path: Path to the thumbnail file that will be sent.
    @type feature_path: String
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: Result of the file update
    @rtype: bool
    """
    files = [('features', open(feature_path, 'rb')), ]
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/' + str(instance_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=files, headers=header)
    # check if the file has been updated correctely 
    return r.status_code == requests.codes.ok

def edit_instance(instance_id, type=None, trusted=None, model_id=None, token=None):
    """
    Method used to edit the data associated to a Instance object.
    It returns the updated object if data is correctly edited, None in case of error.

    @param instance_id: The id of the Instance object that will be updates.
    @type instance_id: int
    @param type: Type of the considered instance.
    @type type: String
    @param trusted: Flag used to detect instances confirmed by the user.
    @type trusted: bool
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The object containing the updated person, None in case of error.
    @rtype: JSON serialized Instance object
    """
    data = {'entity_model': model_id}
    if trusted is not None:
        data['trusted'] = trusted
    if type is not None:
        data['type'] = type
    
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/' + str(instance_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, data, headers=header)
    
    # check if the model has been updated correctely
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def delete_instance(instance_id, token=None):
    """
    Method used to retrieve a specific instance object by its id.

    @param instance_id: Id of the considered Instance object.
    @type instance_id: int
    @param token: Authentication token necessary to invoke the REST API.
    @type token: String
    @return: The result of Instance object deletion.
    @rtype: bool
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'training_set_manager/instances/' + str(instance_id) + '/'
    header = {'Authorization': token}
    r = requests.delete(url, headers=header)
    
    # check if the model has been deleted correctly
    return r.status_code == requests.codes.no_content
