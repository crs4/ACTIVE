"""
This module is used to define all script necessary to associate a proper keyword
with the uploaded item.
The keyword associated is the filename of the item.
"""

from plugins_script.commons.keyword import create_keyword, search_keyword
from plugins_script.commons.tags import create_tag


def _create_or_retrieve_keyword(value, token=None):
    """
    Function used in order to create a new keyword associate to
    the string value if it doesn't exist. Otherwise a already existing
    keyword is returned.

    :param value: String which must be associated to an item
    :return: A object corresponding to the keyword.
    """
    # check if the keyword already exists
    k = search_keyword(value, token)
    # otherwise create a new one
    if not k:
        k = create_keyword(value, token)
    # return the keyword object
    return k


def _tokenize_string(value):
    """
    Method used to tokenize a given string.
    This method split a string on each non alphanumeric
    character and store it in a

    :param value: A string that must be tokenized.
    :return: A list of string obtained from the input one.
    """
    keywords = []
    temp = ''

    for v in value:
        if v != '_' and v.isalnum():
            temp += str(v)
        elif len(temp) > 0:
            keywords.append(temp.lower())
            temp = ''

    if len(temp) > 0:
        keywords.append(temp.lower())

    return keywords


def extract_filename_keywords(auth_dict, param_dict):
    """
    This function is used to associate keywords to a digital item
    starting from its filename.

    @param auth_dict: Dictionary containing the authorization parameters
    @param param_dict: Dictionary containing the function parameters
    """

    try:
        item_name = ''.join(param_dict['filename'].split('.')[0 : -1])

        # extract tokens from filename
        for str in _tokenize_string(item_name):
            keyword = _create_or_retrieve_keyword(str, auth_dict['token'])

            # associate the keyword to the item
            tag = create_tag(param_dict['id'], keyword['id'], 'keyword', auth_dict['token'])
            if not tag:
                raise Exception("Error creating tag " + keyword['description'])

            # TODO check if the tag already exists!!!

    except Exception as e:
        print e
        return False

    return True


def extract_audio_keywords(auth_dict, param_dict):
    """
    Function used to extract the available keywords for audio digital items.

    :param auth_dict: Dictionary containing the authorization parameters
    :param param_dict:  Dictionary containing the function parameters
    :return: The result of keyword extraction
    """
    return extract_filename_keywords(auth_dict, param_dict)


def extract_image_keywords(auth_dict, param_dict):
    """
    Function used to extract the available keywords for image digital items.

    :param auth_dict: Dictionary containing the authorization parameters
    :param param_dict:  Dictionary containing the function parameters
    :return: The result of keyword extraction
    """
    return extract_filename_keywords(auth_dict, param_dict)


def extract_video_keywords(auth_dict, param_dict):
    """
    Function used to extract the available keywords for video digital items.

    :param auth_dict: Dictionary containing the authorization parameters
    :param param_dict:  Dictionary containing the function parameters
    :return: The result of keyword extraction
    """
    return extract_filename_keywords(auth_dict, param_dict)