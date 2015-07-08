"""
This module defines all functions necessary to interact withe the ACTIVE core
through the REST API. Functions are used as proxy in order to improve the
communication between modules and to create a plugin script more simply.
"""

from django.conf import settings
import requests


def create_person(name, surname, token=None):
    """
    Method used to create a new person with the provided complete name.
    This method returns the created and stored object in the db.

    @param name: First ame of the person to create and store
    @param surname: Second name of the person to create and store
    @param token: Authentication token necessary to invoke the REST API.
    @return: The object created and stored for the provided person, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/'
    header = {'Authorization': token}
    r = requests.post(url, {'first_name' : name,
                            'last_name'  : surname,
                            'category'   : 'person'},
                      headers=header)

    # check if the person has been created correctly
    if r.status_code != requests.codes.created:
        return None
    return r.json()


def get_person(person_id, token=None):
    """
    Method used to retrieve all data of a person from its id.
    If no person is found the method will return the None value.

    @param person_id: Id of the searched person.
    @param token: Authentication token necessary to invoke the REST API.
    @return: Object containing all person data, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/' + str(person_id) + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    # check if the person has been retrieved correctly
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def get_person_by_name(name, surname, token=None):
    """
    Method used to retrieve all data of a person from its name and surname.
    If no person is found the method will return the None value.

    :param name: name of the searched person.
    :param surname: surname of the searched person.
    :return: Object containing all person data, None in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/search/' + name+'/' + surname + '/'
    header = {'Authorization': token}
    r = requests.get(url, headers=header)

    # check if the person has been retrieved correctly
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def edit_person(person_id, first_name=None, second_name=None, token=None):
    """
    Method used to edit the data associated to a person.
    It returns the updated object if data is correctly edited, None in case of error.

    @param person_id: The id of the person to update.
    @param first_name: if not None is the first name that will be associated to the user.
    @param second_name: If not None is the new second name that will be associated to the user.
    @param token: Authentication token necessary to invoke the REST API.
    @return: The object containing the updated person, None in case of error.
    """
    data = { 'id' : str(person_id) }
    if first_name:
        data['first_name'] = first_name

    if second_name:
        data['last_name'] = second_name


    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/' + str(person_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, data, headers=header)

    print r.text

    # check if the tag has been created correctly
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


def remove_person(person_id, token=None):
    """
    Method used to remove all data of a specific person providing his id.
    A boolean value is returned containing the deleting result.

    :param person_id: Id of the user that will be deleted
    :return: True if the user is deleted, False in case of error.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/' + str(person_id) + '/'
    header = {'Authorization': token}
    r = requests.delete(url, headers=header)

    # check if the person has been deleted correctly
    return r.status_code != requests.codes.no_content


def set_image(person_id, file_path, file_mime, token=None):
    """
    Method used to update the image associated to a person.
    Providing the person id and the path of the file that must be sent,
    it encapsulate all data in a HTTP request.

    @param person_id: Id of the considered person.
    @param file_path: Path to file that will be sent.
    @param file_mime: MIME type of the preview file.
    @param token: Authentication token necessary to invoke the REST API.
    @return: Result of the file update
    """
    f = open(file_path, 'rb')
    dest_file = 'image_' + str(person_id) + "." + file_mime.split('/')[1]
    multiple_files = [('image', (dest_file, f, file_mime)), ]

    url = settings.ACTIVE_CORE_ENDPOINT + 'api/people/' + str(person_id) + '/'
    header = {'Authorization': token}
    r = requests.put(url, files=multiple_files, headers=header)

    return r.status_code == requests.codes.ok
