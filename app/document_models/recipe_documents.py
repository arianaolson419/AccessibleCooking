from flask_mongoalchemy import *
import re
from .tip_documents import Tip
from .object_documents import TippedEntryField
from app.helper_functions.query_helpers import RecipeQuery
from app import db

class Recipe(db.Document):
    """
    Represents the definition of a recipe
    in the repository.

    Fields:
    recipe_name             Title of the recipe. Required
                                    takes a string

    description             Text description of the recipe. Required
                                    takes a string

    submitter               Name of the submitter. Optional.
                                    takes a string

    difficulty              Difficulty of the recipe. Optional.
                                    takes an integer

    time                    Time taken to finish the recipe. Optional.
                                    takes a string (TODO: discuss this one -> mandatory in minutes? active/passive time?)

    servings                Yield of recipe. Optional
                                    takes a string (TODO: decide. Int for servings? string for all?)

    equipment               Necessary equipment. Optional.
                                    takes a list of strings.

    ingredients             Necessary ingredients. Optional.
                                    takes a list of strings.

    tags                    Tags for searching for the recipe. Optional.
                                    takes a list of strings.

    video_id                The video identification number used to embed a youtube video. Optional
                                    takes a string.

    media_url               The url of the supplemental meadio. Optional.
                                    takes a string

    media_type               Type of supplemental media provided. Required.
                                    takes a string.

    instructions             Steps of recipe. Optional.
                                    takes a list of strings.

    tips                    Tips related to recipe. Optional.
                                    List of references to Tips
    """
    query_class = RecipeQuery

    recipe_name = db.StringField(required=True)
    description = db.StringField(required=True)
    submitter = db.StringField(required=False)

    difficulty = db.StringField(required=False)
    time = db.StringField(required=False)
    servings = db.StringField(required=False)

    equipment = db.ListField(TippedEntryField(required=False))
    ingredients = db.ListField(TippedEntryField(required=False))
    instructions = db.ListField(TippedEntryField(required=False))
    tags = db.ListField(db.StringField(required=False))

    video_id = db.StringField(required=False)
    media_url = db.StringField(required=False)
    media_type = db.StringField(required=False)
    tips = db.ListField(db.DocumentField(Tip, required=False), required = False)

    def get_id(self):
        return str(self.mongo_id)

    def link_tips(self):
        pass
