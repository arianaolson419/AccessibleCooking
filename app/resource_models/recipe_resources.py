from flask import jsonify, request, abort, Response, make_response
from flask_restful import Resource
from flask.ext.mongoalchemy import ValidationError

import pdb
import requests

from app import database
from app.helper_functions.conversions import *

class RecipeAPI(Resource):

	def get(self):
		""" Fetches a recipe from the database """
		pass

	def post(self):
		""" Adds a recipe to the database through args or form """
		received_data = request_to_dict(request)
		try:
            new_recipe = database.Recipe(**received_data)
            new_event.save()
        except ValidationError as error:
            return {'error_type': 'validation',
                    'validation_errors': [str(err) for err in error.errors],
                    'error_message': error.message}, 400
        else:  # return success
            return mongo_to_dict(new_event), 201

	def put(self):
		""" Modify a recipe """
		pass

	def delete(self):
		""" Delete a recipe """
		pass