from flask_mongoalchemy import *
from bson.objectid import *
from app.helper_functions.media import video_id_from_url
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app.document_models.object_documents import Instruction, Ingredient, Equipment

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

def request_to_tip_search(request):
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
        'tip_name':split_to_list,
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
        # The to_dict method returns values as lists, which is necessary for
        # the values with the name 'tag', but none of the other fields.
        if k == 'tag' or k == 'tip':
            obj_dict[k] = v
        elif k == 'difficulty':
            obj_dict['difficulty'] = req_dict['difficulty'][0]
        else:
            obj_dict[k] = check_for_fractions(v[0])
    return obj_dict

def dict_to_recipe(request_dict, recipe=None):
    ingredients = []
    line_num = 0
    for line in request_dict['ingredients'].split('\n'):
        ingredients.append(Ingredient(line=line.strip(), line_num=line_num))
        line_num+=1

    equipment = []
    line_num = 0
    for line in request_dict['equipment'].split('\n'):
        equipment.append(Equipment(line=line.strip(), line_num=line_num))
        line_num+=1

    instructions = []
    line_num = 0
    for line in request_dict['instructions'].split('\n'):
        instructions.append(Instruction(line=line.strip(), line_num=line_num))
        line_num+=1

    if recipe:
        recipe.recipe_name=request_dict['recipe_name']
        recipe.description=request_dict['description']
        recipe.media_type=request_dict['media_type']
        recipe.ingredients=ingredients
        recipe.equipment=equipment
        recipe.instructions=instructions
        recipe.difficulty=request_dict['difficulty']
        recipe.servings=request_dict['servings']
        recipe.time=request_dict['time']
        recipe.tags=request_dict['tag']
        recipe.tips=[]

        if request_dict['media_type'] == 'Video':
            recipe.video_id = video_id_from_url(request_dict['media_url'])
        elif request_dict['media_type'] == 'Audio':
            new_recipe.media_url = request_dict['media_url']

        recipe.save()
        return recipe

    else:
        new_recipe = Recipe(
                    recipe_name=request_dict['recipe_name'],
                    description=request_dict['description'],
                    media_type=request_dict['media_type'],
                    ingredients=ingredients,
                    equipment=equipment,
                    instructions=instructions,
                    difficulty=request_dict['difficulty'],
                    servings=request_dict['servings'],
                    time=request_dict['time'],
                    tags=request_dict['tag'],
                    tips=[])

        if request_dict['media_type'] == 'Video':
            new_recipe.video_id = video_id_from_url(request_dict['media_url'])
        elif request_dict['media_type'] ==  'Audio':
            new_recipe.media_url = request_dict['media_url']

        new_recipe.save()
        return new_recipe

def dict_to_tip(request_dict):
    print(request_dict)

    new_tip = Tip(
                tip_name=request_dict['tip_name'],
                media_type=request_dict['media_type'],
                media_url=request_dict['media_url'],
                video_id=video_id_from_url(request_dict['media_url']),
                difficulty=request_dict['difficulty'],
                description=request_dict['description'],
                equipment=[line.strip().lower() for line in request_dict['equipment'].split('\n')],
                ingredients=[line.strip().lower() for line in request_dict['ingredients'].split('\n')],
                techniques=[line.strip().lower() for line in request_dict['techniques'].split('\n')],
                instructions=[line.strip() for line in request_dict['instructions'].split('\n')],
                tags=request_dict['tag'])

    new_tip.save()
    return new_tip

def form_to_recipe_dict(formdata):
    mapping = {'search':'recipe_name',
                'tag_select':'tags'}
    search_dict = {}
    for key, val in formdata.items():
        if key not in ['select'] and val != []: # expand this as needed
            search_dict[mapping[key]] = val
    return search_dict

def check_for_fractions(ingred):
    replacements = {r"(\d) (1\/2)":r"\1 and a half",
                    r"(\d) (1\/3)":r"\1 and a third",
                    r"(\d) (1\/4)":r"\1 and a quarter",
                    r"(\d) (1\/8)":r"\1 and an eighth",
                    r"(\d) (3\/4)":r"\1 and three quarters",
                    r"(\d) (2\/3)":r"\1 and two thirds",
                    r"^1\/2":"Half", r"(\D) (1\/2)":r"\1 half",
                    r"^1\/3":"One third", r"(\D) (1\/3)":r"\1 one third",
                    r"^1\/4":"One quarter", r"(\D) (1\/4)":r"\1 one quarter",
                    r"^1\/8":"One eighth", r"(\D) (1\/8)":r"\1 one eigth",
                    r"^3\/4":"Three quarters", r"(\D) (3\/4)":r"\1 three quarters",
                    r"^2\/3":"Two thirds", r"(\D) (2\/3)":r"\1 two thirds",
                    r'(\d) (\½)':r"\1 and a half",
                    r"(\d) (\⅓)":r"\1 and a third",
                    r"(\d) (\¼)":r"\1 and a quarter",
                    r"(\d) (\⅛)":r"\1 and an eighth",
                    r"(\d) (\¾)":r"\1 and three quarters",
                    r"(\d) (\⅔)":r"\1 and two thirds",
                    r"^\½":"Half",
                    r"^\⅓":"One third",
                    r"^\¼":"One quarter",
                    r"^\⅛":"One eighth",
                    r"^\¾":"Three quarters",
                    r"^\⅔":"Two thirds"}
    lines = ingred.split("\n")
    replaced = []
    for line in lines:
        for err, rpl in replacements.items():
            line = re.sub(err, rpl, line, flags=re.U)
        replaced.append(line)
    return "\n".join(replaced)

def form_to_tip_dict(formdata):
    mapping = {'search':'tip_name',
                'tag_select':'tags'}
    search_dict = {}
    for key, val in formdata.items():
        if key not in ['select'] and val != []: # expand this as needed
            search_dict[mapping[key]] = val
    return search_dict

def get_all_recipe_text(recipe_obj):
    """Create a large string of the text in a recipe's equipment, ingredient,
    and instruction lists to be used for searching for relevant tags.
    """
    # All of the fields listed give lists of strings.
    fields = ['ingredients', 'equipment', 'instructions']
    recipe_text = ''
    for field in fields:
        recipe_text += ' '.join([recipe_obj[field]])
    return recipe_text

def connect_line_and_tip(recipe_obj, tips):
    for matcher, tip in tips.items():
        if tip != "Add Tips":
            tip_obj = Tip.query.get_or_404(tip)
            [tip_type, line_num] = matcher.split('-')
            line_num = int(line_num)
            match_dict = {'Instruction':recipe_obj.instructions,
                          'Ingredient':recipe_obj.ingredients,
                          'Equipment':recipe_obj.equipment}
            category = match_dict[tip_type][line_num].set_tip(tip, tip_obj.tip_name)

    recipe_obj.save()
