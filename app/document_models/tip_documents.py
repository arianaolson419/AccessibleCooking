from flask_mongoalchemy import *
from app import db

class Tip(db.Document):
	"""
	Represents the definition of a tip in the
	repository.

	Fields:
	title			Title of the tip. Required.
					takes a string.

	text			The tip itself. Required.
					takes a string

	submitter		Name of the submitter. Required.
					takes a string

	related_equip	Names of equipment that might relate to this tip. Optional.
					takes a list of strings

	related_ingr	Names of ingredients that might relate to this tip. Optional.
					takes a list of strings

	aud_vid			Audio/video component. Optional.
					takes a url
	"""
	title = db.StringField(required=True)
	text = db.StringField(required=True)
	submitter = db.StringField(required=False)

	related_equip = db.ListField(db.StringField(), required=False)
	related_ingr = db.ListField(db.StringField(), required=False)

	aud_vid = db.AnythingField(required=False)