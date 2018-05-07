# forms.py

from wtforms import Form, StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField, validators, widgets
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
	search = StringField('Search Box', description='Enter search term')
	tag_select = MultiCheckboxField('Tags', choices = tags)

class AddTipsForm(Form):
	pass

class ContactForm(Form):
	name = StringField("Name", [validators.InputRequired("Name is required")])
	email = StringField("Email", [validators.InputRequired("Email is required"), validators.Email("Must input a valid email")])
	subject = StringField("Subject", [validators.InputRequired("Subject is required")])
	message = TextAreaField("Message", [validators.InputRequired("Message is required")])
	submit = SubmitField("Send")
