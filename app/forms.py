# forms.py

from wtforms import Form, StringField, SelectField, SelectMultipleField, widgets
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()

class RecipeSearchForm(Form):
	choices = [('recipe', 'Recipes'),
				('tip', 'Tips')]
	tags = [('Dinner', 'Dinner'),
			('Breakfast', 'Breakfast'),
			('Lunch', 'Lunch'),
			('Dessert', 'Dessert')]
	select = SelectField('Search the Repository:', choices = choices)
	search = StringField('')
	tag_select = MultiCheckboxField('Tags', choices = tags)

class AddTipsForm(Form):
	pass