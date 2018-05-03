from app import db
import re
from flask_mongoalchemy import BaseQuery
# import requests
# from app.helper_functions.conversions import 



class RecipeQuery(BaseQuery):
    
    def recipe_from_dict(self, search_dict):
        """ Looks for matches from a search dictionary """
        params_recipe = {
            'recipe_name': lambda name: {'recipe_name': {'$options': 'i', '$regex': name}},
            'tags': lambda tags: {'tags': {'$in': tags}},
            'ingredients': lambda ingredients: {'tags': {'$in': ingredients}},
            'equipment': lambda equip: {'tags': {'$in': equip}},
        }

        query_recipes = {}
        for key, pattern in params_recipe.items():
            if key in search_dict.keys() and search_dict[key] != []:
                query_recipes.update(pattern(search_dict[key]))

        return self.filter(query_recipes)

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


class TipQuery(BaseQuery):

    def tip_from_dict(self, search_dict):
        """Looks for matches from a search dictionary
        """
        params_tip = {
                'tip_name': lambda name: {'tip_name': {'$options': 'i', '$regex': name}},
                'tags': lambda tags: {'tags': {'$in': tags}},
                'ingredients': lambda ingredients: {'tags': {'$in': ingredients}},
                'equipment': lambda equip: {'tags': {'$in': equip}}
        }

        query_tips = {}
        for key, pattern in params_tip.items():
            if key in search_dict.keys() and search_dict[key] != []:
                query_tips.update(pattern(search_dict[key]))

        return self.filter(query_tips)

    def in_name(self, name):
        """ Checks for a tip with a similar name """
        return self.filter(self.type.tip_name.regex(name, ignore_case=True))

    def is_type(self, tag):
        return self.filter(self.type.tags.in_(tag))

    def has_keyword(self, keywords):
        """ Checks for matching key words in ingredients or equipment 
            :input:
            keywords: list of strings 
        """
        return self.filter(
            {'equipment':{'$in':keywords},
            'ingredients':{'$in':keywords}})

