from flask import flash, render_template, jsonify, request
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app.forms import RecipeSearchForm
from app import app

from app.helper_functions.media import video_id_from_url
from app.helper_functions.conversions import request_to_dict, form_to_recipe_dict, dict_to_recipe

@app.route('/')
@app.route('/index')
def index():
    return render_template('about.html')

@app.route('/recipes')
def recipe():
    s_form = RecipeSearchForm(request.form)
    recipes = Recipe.query.all()
    return render_template('search.html', form=s_form, results=recipes)

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    search = RecipeSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('search.html', form=search)

def search_results(search):
    results = []
    search_string = search.data['search']
    s_form = RecipeSearchForm(request.form)

    if search.data['select'] == 'Recipe':
        search_dict = form_to_recipe_dict(search.data)
        results = Recipe.query.recipe_from_dict(search_dict)

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('search.html', form=s_form, results=results)

@app.route('/upload_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        dict_to_recipe(request_dict)
        return render_template('upload_recipe_success.html')
    # Render the upload recipe form in the case of GET method.
    return render_template('upload_recipe_form.html')
#       return render_template('recipe_page.html', recipe=recipe)

@app.route('/<recipe_id>')
def specific_recipe(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        return render_template('recipe_template.html', recipe=recipe)

@app.route('/upload_tip', methods=['GET', 'POST'])
def add_new_tip():
    """Uses form input to add a new tip to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        new_tip = Tip(
                title=request_dict['tip_name'],
                text=request_dict['description'],
                submitter='Ariana',
                related_equip=request_dict['equipment'].split('\n'),
                related_ingr=request_dict['equipment'].split('\n'))
        return render_template('upload_tip_success.html')
    return render_template('upload_tip_form.html')
