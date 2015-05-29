"""
This module is used to define all script necessary to associate a proper keyword
with the uploaded item.
The keyword associated is the filename of the item.
"""

from plugins_script.commons.keyword import create_keyword, search_keyword
from plugins_script.commons.tags import create_tag


def _create_or_retrieve_keyword(value):
    """
    Function used in order to create a new keyword associate to
    the string value if it doesn't exist. Otherwise a already existing
    keyword is returned.

    :param value: String which must be associated to an item
    :return: A object corresponding to the keyword.
    """
    # check if the keyword already exists
    k = search_keyword(value)
    # otherwise create a new one
    if not k:
        k = create_keyword(value)
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



def extract_filename_keywords(func_in, func_out):
    """
    This function is used to associate keywords to a digital item
    starting from its filename.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        item_name = ''.join(func_out['filename'].split('.')[0 : -1])

        # extract tokens from filename
        for str in _tokenize_string(item_name):
            keyword = _create_or_retrieve_keyword(str)

            # associate the keyword to the item
            tag = create_tag(func_out['id'], keyword['id'], 'keyword')
            if not tag:
                raise Exception("Error creating tag " + keyword['description'])

            # TODO check if the tag already existis!!!

    except Exception as e:
        print e
        return False

    return True



def extract_audio_keywords(func_in, func_out):
    return extract_filename_keywords(func_in, func_out)

def extract_image_keywords(func_in, func_out):
    return extract_filename_keywords(func_in, func_out)

def extract_video_keywords(func_in, func_out):
    return extract_filename_keywords(func_in, func_out)