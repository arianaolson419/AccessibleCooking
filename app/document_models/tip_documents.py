from flask_mongoalchemy import *
from app import db
from app.helper_functions.query_helpers import TipQuery

class Tip(db.Document):
    """
    Represents the definition of a tip in the
    repository.

    Fields:
    tip_name                Name of the tip. Required.
                                    takes a string.

    description             Brief description of the tip. Required.
                                    takes a string

    difficulty              Level of difficulty for the tip. Required.
                                    takes a string: 'beginner', 'intermediate', or 'advanced'

    media_type              Type of supplemental media. Required.
                                    takes a string: 'No Supplemental Media', 'Video', or 'Audio

    media_url               Audio component. Optional.
                                    takes a string.

    video_id                ID of a youtube video, used to embed. Optional.
                                    takes a string.

    submitter               Name of the submitter. Required.
                                    takes a string

    equipment               Names of equipment that might relate to this tip. Optional.
                                    takes a list of strings

    ingredients             Names of ingredients that might relate to this tip. Optional.
                                    takes a list of strings

    techniques              Names of techniques that might relate to this tip. Optional.
                                    takes a list of strings

    instructions            Main text of the tip.
                                    takes a string

    tags                    List of the categories it falls into
                                    takes a list of strings (method, ingredient, equipment)
    """
    query_class = TipQuery
    tip_name = db.StringField(required=True)
    description = db.StringField(required=True)
    difficulty = db.StringField(required=True)
    media_type = db.StringField(required=True)
    media_url = db.StringField(required=False)
    video_id = db.StringField(required=False)
    submitter = db.StringField(required=False)
    equipment = db.ListField(db.StringField(required=False), required=False)
    ingredients = db.ListField(db.StringField(required=False), required=False)
    techniques = db.ListField(db.StringField(required=False), required=False)
    instructions = db.ListField(db.StringField(required=False), required=False)
    tags = db.ListField(db.StringField(required=False), required=False)

    def get_id(self):
        return str(self.mongo_id)
