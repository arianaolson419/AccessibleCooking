from flask.ext.mongoalchemy import Document

class Tip(Document):
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

	title = StringField(required=True)
	text = StringField(required=True)
	submitter = StringField(required=True)

	related_equip = ListField(StringField())
	related_ingr = ListField(StringField())

	aud_vid = URLField()