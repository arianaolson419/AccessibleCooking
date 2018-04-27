# forms.py

from wtforms import Form, StringField, SelectField

class RecipeSearchForm(Form):
	choices = [('Tag', 'tags'),
				('Difficulty', 'difficulty')]
	select = SelectField('Search for Recipe:', choices = choices)
	search = StringField('')