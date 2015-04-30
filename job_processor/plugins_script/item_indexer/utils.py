from django.conf import settings
import requests
import os


"""
This module is used to define all script necessary to associate a proper keyword 
with the uploaded item.
The keyword associated is the filename of the item.
"""

# funzione utilizzata per estrarre una thumbnail all'istante 49
# ffmpeg -ss 49 -i MONITOR0720  11.mpg  -vf "crop=min(iw\,ih):min(ih\,iw), scale=256:256" -vframes 1 sample.jpg


def extract_video_keywords(func_in, func_out):
    """
    This function is used to create a keyword associated with a video item.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        video_title = func_out['filename']

        server_url_keyword= settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/'
        data = {'description': video_title, 'category': 'Keyword - '+video_title}
        rk = requests.post(server_url_keyword, data=data)
        print "Sending video keyword to ", server_url_keyword, rk.status_code

        if rk.status_code == requests.codes.ok or rk.status_code == requests.codes.created:
            video_id = func_out['id']
            server_url_tags= settings.ACTIVE_CORE_ENDPOINT + 'api/tags/'
            rt = requests.post(server_url_tags, data={'type':'video', 'entity': rk.json()['id'], 'item': video_id})
            print "Sending video tag to ", server_url_tags
        else:
            raise Exception("Keyword not created - " + video_title)

    except Exception as e:
        print e
   


def extract_image_keywords(func_in, func_out):
    """
    This function is used to create a keyword associated with an image item.

    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        image_title = func_out['filename']

        # TODO splittare il nome del file e indicizzare tutti i token ottenuti?

        server_url_keyword= settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/'
        data = {'description': image_title, 'category': 'Keyword - '+image_title}
        rk = requests.post(server_url_keyword, data=data)
        print "Sending image keyword to ", server_url_keyword, rk.status_code

        #if rk.status_code == requests.codes.ok or rk.status_code == requests.codes.created:
        print rk.json()
        image_id = func_out['id']
        print image_id
        server_url_tags = settings.ACTIVE_CORE_ENDPOINT + 'api/tags/'
        print server_url_tags
        rt = requests.post(server_url_tags, data={'type':'image', 'entity': rk.json()['id'], 'item': image_id})
        print "Sending image tag to ", server_url_tags
        #else:
        #    raise Exception("Keyword not created - " + image_title)

    except Exception as e:
        print e


def extract_audio_keywords(func_in, func_out):
    """
    This function is used to create a keyword associated with an audio item.


    @param func_in: Input parameters of the function that generate this function call
    @param func_out: Output parameters of the function that generate this function call
    """

    try:
        audio_title = func_out['filename']

        server_url_keyword= settings.ACTIVE_CORE_ENDPOINT + 'api/keywords/'
        data = {'description': audio_title, 'category': 'Keyword - '+audio_title}
        rk = requests.post(server_url_keyword, data=data)
        print "Sending audio keyword to ", server_url_keyword, rk.status_code

        if rk.status_code == requests.codes.ok or rk.status_code == requests.codes.created:
            audio_id = func_out['id']
            server_url_tags= settings.ACTIVE_CORE_ENDPOINT + 'api/tags/'
            rt = requests.post(server_url_tags, data={'type':'audio', 'entity': rk.json()['id'], 'item': audio_id})
            print "Sending audio tag to ", server_url_tags
        else:
            raise Exception("Keyword not created - " + audio_title)

    except Exception as e:
        print e
