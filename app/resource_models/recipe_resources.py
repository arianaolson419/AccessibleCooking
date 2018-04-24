from flask import jsonify, request, abort, Response, make_response
from flask_restful import Resource, Api
#from flask_mongoalchemy import ValidationError

import pdb
import requests

from app import db
from app.helper_functions.conversions import *
from app.document_models.recipe_documents import Recipe

class RecipeAPI(Resource):

    def get(self, recipe_id):
        """ Fetches a recipe from the database """
        if recipe_id:  # use recipe id if present
            result = db.Recipe.objects(id=event_id).first()

            if not result:
                return "Event not found with identifier '{}'".format(recipe_id), 404
            return mongo_to_dict(result)

        else:  # search database based on parameters
            # make a query to the database
            query_dict = get_to_recipe_search(request) # TODO: implement query
            query = recipe_query(query_dict)
            results = db.Recipe.objects(__raw__ = query)
            if not results: # if no results were found
                return []

            recipes_list = []
            for recipe in results:
                recipes_list.append(mongo_to_dict(recipe))

            return recipes_list

    def post(self, request):
        """ Adds a recipe to the database through args or form """
        received_data = request_to_dict(request)
        print('the received data')
        new_recipe = Recipe(**recieved_data)
        new_recipe.save()
        return mongo_to_dict(new_recipe), 201
#        try:
#            new_recipe = db.Recipe(**received_data)
#            new_event.save()
#        except ValidationError as error:
#            return {'error_type': 'validation',
#                    'validation_errors': [str(err) for err in error.errors],
#                    'error_message': error.message}, 400
#        else:  # return success
            #return mongo_to_dict(new_event), 201

    def put(self):
        """ Modify a recipe """
        pass

    def delete(self):
        """ Delete a recipe """
        pass

