# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
import json
import requests


def request_builder(op_name, item, token):
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/search/items/' + op_name
    header = {'content-type':'application/json', 'Authorization':token}
    r = requests.post(url, data=json.dumps({'doc_type':'items', 'params':item}), headers=header)
    return r

def create_index(item, token=None):
    """
    Method used to  index a new item on elasticsearch
    @param item: the item.
    """
    print "create index"
    r = request_builder('create', item, token)

def exists_index(item, token=None):
    """
    Method used to  index a new item on elasticsearch providing the item id
    @param item: Id of the considered digital item.
    """
    r = request_builder('exists', item, token)
    return r

def update_index(item, token=None):
    """
    Method used to update an item on elasticsearch
    @param item: the item.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/search/items/update'
    header = {'content-type':'application/json', 'Authorization':token}
    r = requests.put(url, data=json.dumps({'doc_type':'items', 'params':item}), headers=header)

def delete_index(item, token=None):
    """
    Method used to  delete an item on elasticsearch providing the item id
    @param item: The item.
    """
    url = settings.ACTIVE_CORE_ENDPOINT + 'api/search/items/delete'
    header = {'content-type':'application/json', 'Authorization':token}
    r = requests.delete(url, data=json.dumps({'doc_type':'items', 'params':item}), headers=header)
