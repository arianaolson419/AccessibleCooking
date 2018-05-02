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

        text                    The tip itself. Required.
                                        takes a string

        submitter               Name of the submitter. Required.
                                        takes a string

        related_equip   Names of equipment that might relate to this tip. Optional.
                                        takes a list of strings

        related_ingr    Names of ingredients that might relate to this tip. Optional.
                                        takes a list of strings

        aud_vid                 Audio/video component. Optional.
                                        takes a url
        """
        # TODO: update schema to match tip form fields.
        query_class = TipQuery

        tip_name = db.StringField(required=True)
        media_type = db.StringField(required=True)
        media_url = db.StringField(required=False)
        video_id = db.StringField(required=False)
        submitter = db.StringField(required=False)
        description = db.StringField(required=True)
        difficulty = db.StringField(required=True)
        equipment = db.ListField(db.StringField(required=False), required=False)
        ingredients = db.ListField(db.StringField(required=False), required=False)
        instructions = db.ListField(db.StringField(required=False), required=False)
        tags = db.ListField(db.StringField(required=False), required=False)

        def get_id(self):
            return str(self.mongo_id)
