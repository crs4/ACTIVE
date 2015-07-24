"""
Module used to handle keywords interacting with the ACTIVE core through
the provided REST API.
"""

from django.conf import settings
import requests


def create_keyword(value, token=None):
    """
    Method used to create a new keyword providing string associated.
    This string will be processed and stored by the ACTIVE core.
    The object containing keyword information is returned.

    @param value: String that will be stored as keyword.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The new keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/'
    header = {'Authorization': token}
    r = requests.post(url, {'category'    : 'keyword',
                            'description' : value},
                      headers=header)

    # check if the keyword has been created correctly
    if r.status_code != requests.codes.created:
        return None
    return r.json()


def get_keyword(keyword_id, token=None):
    """
    Method used to retrieve a specific keyword providing its id.
    A object JSON serialized is returned, if any.

    @param keyword_id: Id of the keyword that will be retrieved.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/' + str(keyword_id)
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    # check if the keyword has been retrieved correctly
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def search_keyword(keyword_value, token=None):
    """
    Method used to retrieve a keyword providing a string.
    The provided string is used to find the most similar keyword.
    A object JSON serialized is returned, if any.

    @param keyword_value: String used to find a keyword.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The keyword object, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/search/' + keyword_value
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    # check if the keyword has been found
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def remove_keyword(keyword_id, token=None):
    """
    Method used to delete a specific keyword providing its id.
    A object JSON serialized is returned, if any.

    @param keyword_id: Id of the keyword that will be deleted.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The result of keyword deletion.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/' + str(keyword_id)
    header = {'Authorization': token}
    r = requests.delete(url, headers=header)

    # check if the keyword has been deleted correctly
    return r.status_code == requests.codes.no_content
