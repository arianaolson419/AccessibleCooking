from flask.ext.mongoalchemy import *
from tip_documents import Tip
from app.database import *

class Recipe(db.Document):
	"""
	Represents the definition of a recipe
	in the repository.

	Fields:
	recipe_name		Title of the recipe. Required
					takes a string

	description		Text description of the recipe. Required
					takes a string

	submitter		Name of the submitter. Optional.
					takes a string

	difficulty		Difficulty of the recipe. Optional.
					takes an integer

	time			Time taken to finish the recipe. Optional.
					takes a string (TODO: discuss this one -> mandatory in minutes? active/passive time?)

	servings		Yield of recipe. Optional
					takes a string (TODO: decide. Int for servings? string for all?)

	equipment		Necessary equipment. Optional.
					takes a list of strings.

	ingredients		Necessary ingredients. Optional.
					takes a list of strings.

	tags			Tags for searching for the recipe. Optional.
					takes a list of strings.

	media_url		Audio/video component. Optional.
					takes a url.

	instruction		Steps of recipe. Optional.
					takes a list of strings.

	tips			Tips related to recipe. Optional.
					List of references to Tips
	"""

	recipe_name = db.StringField(required=True)
	description = db.StringField(required=True)
	submitter = db.StringField()

	difficulty = db.IntField()
	time = db.StringField()
	servings = db.StringField()

	equipment = db.ListField(StringField())
	ingredients = db.ListField(StringField())
	instruction = db.ListField(StringField())
	tags = db.ListField(StringField())

	media_url = db.URLField()
	tips = db.ListField(ReferenceField(Tip))