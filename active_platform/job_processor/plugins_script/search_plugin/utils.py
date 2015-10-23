# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.



import json
import os
import subprocess

from plugins_script.commons.keyword import get_keyword_by_item
from plugins_script.commons.person import get_person_by_item
from plugins_script.commons.search import create_index, exists_index, update_index, delete_index

def create_search_item(auth_params, func_params):
    """
    This function is used to create, or update if already exists, an item on elasticsearch

    :param auth_params: Input parameters of the function that generate this function call
    :param func_params: Output parameters of the function that generate this function call
    """

    token = auth_params['token']
    
    keywords_resp = get_keyword_by_item(func_params['id'], token)
    people = get_person_by_item(func_params['id'], token)
    
    keywords = []
   
    for k in keywords_resp:
        keywords.append(k['description'])
    
    func_params['keywords'] = keywords + people
        
    del func_params['thumb']
    del func_params['preview']


    exists = exists_index(func_params, token)
    exists = exists.json()
    #if exists['results']:
    if 'results' in exists:
        update_index(func_params, token)
    else:
        create_index(func_params, token)
    
    
    
def delete_search_item(auth_params, func_params):
    """
    This function is used to delete an item on elasticsearch

    :param auth_params: Input parameters of the function that generate this function call
    :param func_params: Output parameters of the function that generate this function call
    """
    token = auth_params['token']
    
    exists = exists_index(func_params, token)
    exists = exists.json()
    if exists['results']:
        delete_index(func_params, token)
    

