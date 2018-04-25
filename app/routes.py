from flask import render_template, jsonify, request
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app import app
from app.helper_functions.conversions import request_to_dict

@app.route('/')
@app.route('/index')
def index():
    return jsonify({"Name":"Ariana"})

@app.route('/recipe')
def recipe():
    recipes = Recipe.query.all()
    content = '<h1>Recipes</h1><ol>'
    for recipe in recipes:
        content += '<li>{}</li>'.format(recipe.recipe_name)
    content += '</ol>'
    return content

@app.route('/upload_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        # TODO: separate into smaller functions
        
        # TODO: implement error handling and required fields in form.
        # Currently, the function assumes that all of the field are filled in,
        # and if they are not, an internal server error is thrown.
        new_recipe = Recipe(
                recipe_name=request_dict['recipe_name'],
                description=request_dict['description'],
                ingredients=request_dict['ingredients'].split('\n'),
                equipment=request_dict['equipment'].split('\n'),
                instructions=request_dict['instructions'].split('\n'),
                difficulty=request_dict['difficulty'],
                tags=[request_dict['tag']],
                tips=[])
        new_recipe.save()
        return render_template('upload_recipe_success.html')
    # Render the upload recipe form in the case of GET method.
    return render_template('upload_recipe_form.html')

@app.route('/cookies')
def cookie_page():
	search_dict = {'recipe_name':'cookie'}
	cookie = Recipe.query.recipe_from_dict(search_dict).first()
	return render_template('recipe_page.html', recipe=cookie)

@app.route('/upload_tip', methods=['GET', 'POST'])
def add_new_tip():
    """Uses form input to add a new tip to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        print('REQUEST DICT', request_dict)
        new_tip = Tip(
                title=request_dict['tip_name'],
                text=request_dict['description'],
                submitter='Ariana',
                related_equip=request_dict['equipment'].split('\n'),
                related_ingr=request_dict['equipment'].split('\n'))
        return render_template('upload_tip_success.html')
    return render_template('upload_tip_form.html')
