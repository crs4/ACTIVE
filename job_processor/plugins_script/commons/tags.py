"""
Module used to define all methods necessary to interact with the ACTIVE core
using some objects instead of JSON serialized data.
All defined methods are used to retrieve, create and update tags and dynamic tags
stored by the core and accessible through the REST API.
"""

from django.conf import settings
import requests


def create_tag(item_id, entity_id, tag_type):
    """
    Method used to create a new tag providing the item id and the person id
    which occurs in the digital item.

    :param item_id: Id of the considered digital item.
    :param entity_id: Id of the person which occurs in the digital item.
    :param tag_type: Type of the tag that will be generated.
    :return: The new tag object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/'
    r = requests.post(url, {'entity' : str(entity_id),
                            'item'   : str(item_id),
                            'type'   : tag_type})

    # check if the tag has been created correctly
    if r.status_code != requests.codes.created:
        return None
    return r.json()


def get_tag(tag_id):
    """
    Function used to retrieve data associated to a
    specific Tag providing its id.
    Return an object if the tag has been found, None if error.

    :param tag_id: Id of the Tag that will be retrieved.
    :return: Object containing Tag data, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/' + str(tag_id)
    r = requests.get(url)

    # scan result and delete one dynamic tag at time
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_tags_by_item(item_id):
    """
    Function used to retrieve all tags associated to a
    specific digital item, providing its id.
    A list of tag object JSON serialized is returned.

    :param item_id: Id of the item used to retrieve tags.
    :return: A list of tag objects, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/search/item/' + str(item_id)
    r = requests.get(url)

    # check for result
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_tags_by_person(person_id):
    """
    Function used to retrieve all tags associated to a
    specific person, providing its id.
    A list of tag object JSON serialized is returned.

    :param item_id: Id of the person used to retrieve tags.
    :return: A list of tag objects, None in case of error
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/search/person/' + str(person_id)
    r = requests.get(url)

    # check for result
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


# inserire un metodo che consente di modificare i tag


def remove_tag(tag_id):
    """
    Method used to delete a tag with all associated dynamic tags providing its id.
    The method returns the deletion result.

    @param tag_id: Id of the tag that will be deleted.
    @return: The result of the tag deletion.
    """

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/' + str(tag_id)
    r = requests.delete(url)

    # check if the dynamic tag has been created correctly
    return r.status_code == requests.codes.no_content





def create_dtag(tag_id, start, duration, bbox_x=0, bbox_y=0, bbox_width=0, bbox_height=0):
    """
    Method used to crate a dynamic tag, starting from an existing tag which stores the
    occurrence of a person in a digital item. The dynamic tag will store all details
    about the occurrence.

    :param tag_id: Id of the tag that will be associated to the dynamic tag.
    :param start: Initial instant of the occurrence.
    :param duration: Duration of the occurrence.
    :param bbox_x: Bounding box x value highlighting the occurrence.
    :param bbox_y: Bounding box y value highlighting the occurrence.
    :param bbox_width: Width of the bounding box.
    :param bbox_height: Height of the bounding box.
    :return: The new object created, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/dtags/'
    r = requests.post(url, {'tag'        : str(tag_id),
                            'start'      : start,
                            'duration'   : duration,
                            'x_position' : bbox_x,
                            'y_position' : bbox_y,
                            'size_width' : bbox_width,
                            'size_height': bbox_height})

    # check if the dynamic tag has been created correctly
    if r.status_code != requests.codes.created:
        return None
    return r.json()


def get_dtag(dtag_id):
    """
    Function used to retrieve data associated to a
    specific Dyanmic Tag providing its id.
    Return an object if the dynamic tag has been found, None if error.

    :param tag_id: Id of the Tag that will be retrieved.
    :return: Object containing Tag data, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/dtags/' + str(dtag_id)
    r = requests.get(url)

    # check the result
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_dtags_by_person(person_id):
    """
    Method used to retrieve all dynamic tags associated
    to a specific person providing its id.
    The method returns a list of objects JSON serialized.

    @param person_id: Id of the person used to find dynamic tags associated to him.
    @return: A list of Dynamic Tags, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/dtags/search/person/' + str(person_id)
    r = requests.get(url)

    # check the result
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_dtags_by_item(item_id):
    """
    Method used to retrieve all dynamic tags associated to a specific item providing its id.
    The method returns a list of object JSON serialized.

    @param item_id: Id of the item used to find dynamic tags associated ot it.
    @return: The result of the dynamic tag deletion.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/dtags/search/item/' + str(item_id)
    r = requests.get(url)

    # check the result
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def remove_dtag(dtag_id):
    """
    Method used to delete a dynamic tag providing its id.
    The method returns the deletion result.

    @param tag_id: Id of the tag that will be deleted.
    @return: The result of the tag deletion.
    """

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/dtags/' + str(dtag_id)
    r = requests.delete(url)

    # check if the dynamic tag has been created correctly
    return r.status_code == requests.codes.no_content