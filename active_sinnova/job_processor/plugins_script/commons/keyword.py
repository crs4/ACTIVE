"""
Module used to handle keywords interacting with the ACTIVE core through
the provided REST API.
"""

from django.conf import settings
import requests


def create_keyword(value):
    """
    Method used to create a new keyword providing string associated.
    This string will be processed and stored by the ACTIVE core.
    The object containing keyword information is returned.

    :param value: String that will be stored as keyword.
    :return: The new keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/'
    r = requests.post(url, {'category'    : 'keyword',
                            'description' : value})
    print r.text[:10000]
    print "Creazione keyword", value
    # check if the keyword has been created correctly
    if r.status_code != requests.codes.created:
        return None
    return r.json()


def get_keyword(keyword_id):
    """
    Method used to retrieve a specific keyword providing its id.
    A object JSON serialized is returned, if any.

    :param keyword_id: Id of the keyword that will be retrieved.
    :return: The keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/' + str(keyword_id)
    r = requests.get(url)

    # check if the keyword has been retrieved correctly
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def search_keyword(keyword_value):
    """
    Method used to retrieve a keyword providing a string.
    The provided string is used to find the most similar keyword.
    A object JSON serialized is returned, if any.

    :param keyword_value: String used to find a keyword.
    :return: The keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/search/' + keyword_value
    r = requests.get(url)

    # check if the keyword has been found
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def remove_keyword(keyword_id):
    """
    Method used to delete a specific keyword providing its id.
    A object JSON serialized is returned, if any.

    :param keyword_id: Id of the keyword that will be deleted.
    :return: The result of keyword deletion.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/' + str(keyword_id)
    r = requests.delete(url)

    # check if the keyword has been deleted correctly
    return r.status_code == requests.codes.no_content

