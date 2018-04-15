from flask.ext.mongoalchemy import Document

class Recipe(Document):
	"""
	Represents the definition of a recipe
	in the repository.

	Fields:
	title			Title of the recipe. Required
					takes a string

	desc			Text description of the recipe. Required
					takes a string

	submitter		Name of the submitter. Required
					takes a string

	diff			Difficulty of the recipe. Optional.
					takes an integer

	time			Time taken to finish the recipe. Optional.
					takes a string (TODO: discuss this one -> mandatory in minutes? active/passive time?)

	num_serv		Yield of recipe. Optional
					takes a string (TODO: decide. Int for servings? string for all?)

	equip			Necessary equipment. Optional.
					takes a list of strings.

	ingredients		Necessary ingredients. Optional.
					takes a list of strings.

	tags			Tags for searching for the recipe. Optional.
					takes a list of strings.

	aud_vid			Audio/video component. Optional.
					takes a url.

	steps			Steps of recipe. Optional.
					takes a list of strings.

	tips			Tips related to recipe. Optional.
					TODO: figure out this format. could be dictionary of indices to urls?
	"""

	title = StringField(required=True)
	desc = StringField(required=True)
	submitter = StringField(required=True)

	diff = IntField()
	time = StringField()
	num_serv = StringField()

	equip = ListField(StringField())
	ingredients = ListField(StringField())
	steps = ListField(StringField())
	tags = ListField(StringField())

	aud_vid = URLField()
	tips = ListField(DictField())