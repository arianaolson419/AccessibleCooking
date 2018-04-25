from app import db
import re
from flask_mongoalchemy import BaseQuery
# import requests
from app.helper_functions.conversions import *



class RecipeQuery(BaseQuery):
    
    def recipe_from_dict(search_dict):
        """ Looks for matches from a search dictionary """
        params_recipe = {
            'recipe_name': lambda name: 'recipe_name':re.compile(r+name, re.IGNORECASE),
            'tags': lambda tags: { '$in': tags},
        }

    def has_name(self, name):
        """ Checks for a recipe that matches the name """
        return self.filter(self.type.recipe_name.regex(name, ignore_case = True))

    def has_tag(self, tag):
        """ Checks for a specific tag in a recipe, returns a list of
        query objects """
        return self.filter(self.type.tags.in_(tag))

    def has_ingredient(self, ingredient):
        return self.filter(self.type.ingredients.in_(ingredient))

    def has_equip(self, equip):
        return self.filter(self.type.equipment.in_(equip))