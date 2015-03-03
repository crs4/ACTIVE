"""
This file contains both function and binding to functions, in order to invoke
the correct functionality when an HTTP request is done.
"""

from django.shortcuts import render
from django.http import HttpResponse
from core.models      import Person, Occurrence
import json
from django.core import serializers


"""
Function that allow to obtain main information for each Person objects saved in the database.
Data returned is converted in a JSON format, a list of serialized objects.
"""
def get_all_person(request):
    # variable that will be converted in JSON format
    data = []
    # append all converted objects
    for p in Person.objects.all():
        data.append(p.__json__())
    # return converted results (if any)
    return HttpResponse(json.dumps(data), content_type = "application/json")

"""
Function used to obtain information of a specific Person object.
All attributes are serialized and returned in JSON format.
"""
def get_person(request):
    # variable for result data
    data = {}
    # check if a Person id has been specified
    if "person_id" in request.GET :
        person_id = request.GET.__getitem__("person_id")
        try:
            data = Person.objects.get(id=person_id).__json__()
        except:
            print("Selected person doesn't exist")
    # return converted result (if any)
    return HttpResponse(json.dumps(data), content_type = "application/json")

"""
Function used to obtain all occurrences of a specific Person and/or Item.
Resulting data is serialized and returned in JSON format.
"""
def get_occurrences(request):
    # variable for result data
    data = []

    # check if a Person has been specified
    person_id = request.GET.__getitem__("person_id") if (request.GET.__contains__("person_id")) else None
    # check if an Item has been specified
    item_id = request.GET.__getitem__("item_id") if (request.GET.__contains__("item_id")) else None

    results = []
    if person_id is not None and item_id is not None:
        results = Occurrence.objects.filter(person=person_id).filter(item=item_id)
    elif person_id is not None:
        results = Occurrence.objects.filter(person=person_id).all()
    elif item_id is not None:
        results = Occurrence.objects.filter(item=item_id).all()
    else :
        results = Occurrence.objects.all()

    # print obtained results
    for o in results:
        data.append(o.__json__())

     # return converted result (if any)
    return HttpResponse(json.dumps(data), content_type = "application/json")
