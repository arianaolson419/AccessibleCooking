from flask_mongoalchemy import *

import logging
import pdb
import pytz
import re

# import requests

from app import db

def mongo_to_dict(obj):
    """Get dictionary from mongoengine object
    id is represented as a string

    obj         A mongodb object that will be converted to a dictionary
    """
    return_data = []
    if obj is None:
        return None

    # converts the mongoDB id for documents to a string from an ObjectID object
    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in obj:  # check if field is populated
            if field_name in ("id",):
                continue

            data = obj[field_name]
            if isinstance(obj._fields[field_name], ListField):
                return_data.append((field_name, list_field_to_dict(data)))
            elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
                return_data.append((field_name, mongo_to_dict(data)))
            elif isinstance(obj._fields[field_name], DictField):
                return_data.append((field_name, data))
            else:
                return_data.append((field_name, mongo_to_python_type(obj._fields[field_name], data)))

    return dict(return_data)

def request_to_recipe_search(request):
    """ Build search dictionary based on get parameters """
    if isinstance(request, dict):
        req_dict = request
    else:
        req_dict = request_to_dict(request)

    split_to_list = lambda a: a if isinstance(a, list) else a.split(',')

    difficulties = {
        'beginner': ['beginner'],
        'intermediate': ['intermediate'],
        'advanced': ['advanced'],
    }

    preprocessing = {
        'recipe_name':split_to_list,
        'ingredients':split_to_list,
        'equipment':split_to_list,
        'tags':split_to_list,
        'tags_not':split_to_list,
        'difficulty':lambda a: difficulties.get(a, None),
    }

    search_dict = req_dict
    for key, process in preprocessing.items():
        if key in search_dict.keys():
            search_dict[key] = process(search_dict[key])

    return search_dict


def list_field_to_dict(list_field):
    """
    Converts a list of mongodb Objects to a dictionary object

    list_field          list of embedded documents or other object types
    """

    return_data = []

    for item in list_field:
        # if list is of embedded documents, convert each document to a dictionary
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item))
        # convert the data type
        else:
            return_data.append(mongo_to_python_type(item,item))

    return return_data


def mongo_to_python_type(field, data):
    """
    Converts certain fields to appropriate data types

    field       A field in a mongoDB object

    data        corresponding data to the field
    """
    if isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    elif isinstance(field, BooleanField):
        return data
    else:
        return str(data)


def request_to_dict(request):
    """Convert incoming flask requests for objects into a dict"""

    if request.is_json:
        req_dict = request.get_json()  # get_dict returns python dictionary object
    else:
        req_dict = request.values.to_dict(flat=False)
    obj_dict = {}
    for k, v in req_dict.items():
        print(k, v)
        # The to_dict method returns values as lists, which is necessary for
        # the values with the name 'tag', but none of the other fields.
        if k == 'tag':
            obj_dict[k] = v
        elif k == 'difficulty':
            mapping = {'intermediate':2, 'beginner':1, 'advanced':3}
            obj_dict['difficulty'] = mapping[req_dict['difficulty'][0]]
        else:
            obj_dict[k] = v[0]
    print(obj_dict)
    return obj_dict

def form_to_recipe_dict(formdata):
    mapping = {'search':'recipe_name',
                'tag_select':'tags'}
    search_dict = {}
    print(formdata)
    for key, val in formdata.items():
        if key not in ['select'] and val != []: # expand this as needed
            search_dict[mapping[key]] = val
    return search_dict

def check_for_fractions(ingred):
    replacements = {r" 1\/2":" and a half",
                    r" 1\/3":" and a third",
                    r" 1\/4":" and a quarter",
                    r" 1\/8":" and an eighth",
                    r" 3\/4":" and three quarters",
                    r" 2\/3":" and two thirds",
                    r"^1\/2":"Half",
                    r"^1\/3":"One third",
                    r"^1\/4":"One quarter",
                    r"^1\/8":"One eight",
                    r"^3\/4":"Three quarters",
                    r"^2\/3":"Two thirds"}
    for err, rpl in replacements.items():
        ingred = re.sub(err, rpl, ingred)
    return ingred