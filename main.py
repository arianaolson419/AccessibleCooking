import os
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
# from app.document_models.tip_documents import Tip
# from app.document_models.recipe_documents import Recipe

# app = Flask(__name__)
# app.config['MONGOALCHEMY_DATABASE'] = 'recipes'
# # app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://<username>.<pass>@<this will be copied and pasted from online db>'
# db = MongoAlchemy(app)

# class Tip(db.Document):
# 	"""
# 	Represents the definition of a tip in the
# 	repository.

# 	Fields:
# 	title			Title of the tip. Required.
# 					takes a string.

# 	text			The tip itself. Required.
# 					takes a string

# 	submitter		Name of the submitter. Required.
# 					takes a string

# 	related_equip	Names of equipment that might relate to this tip. Optional.
# 					takes a list of strings

# 	related_ingr	Names of ingredients that might relate to this tip. Optional.
# 					takes a list of strings

# 	aud_vid			Audio/video component. Optional.
# 					takes a url
# 	"""

# 	title = db.StringField(required=True)
# 	text = db.StringField(required=True)
# 	submitter = db.StringField(required=True)

# 	related_equip = db.ListField(db.StringField())
# 	related_ingr = db.ListField(db.StringField())

	# aud_vid = db.AnythingField()
