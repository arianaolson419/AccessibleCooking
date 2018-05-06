from flask import flash, render_template, jsonify, request, redirect
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app.forms import RecipeSearchForm
from app import app

from app.helper_functions.media import video_id_from_url
from app.helper_functions.conversions import request_to_dict, form_to_recipe_dict, form_to_tip_dict, dict_to_recipe, dict_to_tip, connect_line_and_tip

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/styleguide')
def styleguide():
    return render_template('style_guide.html')

@app.route('/recipes')
def recipe():
    s_form = RecipeSearchForm(request.form)
    recipes = Recipe.query.all()
    return render_template('search.html', form=s_form, results=recipes)

@app.route('/tip')
def tip():
    tips = Tip.query.all()
    content = '<h1>Tips</h1><ol>'
    for tip in tips:
        content += '<li>{}: {}</li>'.format(tip.tip_name, tip.get_id())
    content += '</ol>'
    return content

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

    if search.data['select'] == 'recipe':
        search_dict = form_to_recipe_dict(search.data)
        results = Recipe.query.recipe_from_dict(search_dict)

    elif search.data['select'] == 'tip':
        search_dict = form_to_tip_dict(search.data)
        results = Tip.query.tip_from_dict(search_dict)

    if not results:
            flash('No results found!')
            return redirect('/')
    else:
            return render_template('search.html', form=s_form, results=results, search_type=search.data['select'])

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    tips = [tip.get_id() for tip in recipe.tips]
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe, tips=tips)
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        recipe = dict_to_recipe(request_dict)
        # linked_tips = [Tip.query.get(tiplink) for tiplink in request_dict['tiplinks'].split('\n')]
        # recipe.tips = [tip for tip in linked_tips if tip is not None]
        # recipe.recipe_name = request_dict['recipe_name']
        # recipe.media_type = request_dict['media_type']
        # recipe.media_url = request_dict['media_url']
        # recipe.video_id = video_id_from_url(request_dict['media_url'])
        # recipe.difficulty = request_dict['difficulty']
        # recipe.description = request_dict['description']
        # recipe.time = request_dict['time']
        # recipe.servings = request_dict['servings']
        # recipe.equipment = request_dict['equipment'].split('\n')
        # recipe.ingredients = request_dict['ingredients'].split('\n')
        # recipe.instructions = request_dict['instructions'].split('\n')
        # recipe.tags = request_dict['tag']
        # recipe.save()
        return redirect('/recipe/' + recipe.get_id())

@app.route('/upload_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        recipe = dict_to_recipe(request_dict)
        return redirect('/add_tips/' + recipe.get_id())
    # Render the upload recipe form in the case of GET method.
    return render_template('upload_recipe_form.html')

@app.route('/add_tips/<recipe_id>', methods=['GET', 'POST'])
def add_tips(recipe_id):
    """
    """
    if request.method == 'POST':
        tips = request_to_dict(request)
        recipe = Recipe.query.get_or_404(recipe_id)
        connect_line_and_tip(recipe, tips)
        return render_template('upload_recipe_success.html')
    recipe = Recipe.query.get_or_404(recipe_id)
    equip_tips = Tip.query.is_type('equipment')
    ingred_tips = Tip.query.is_type('ingredient')
    method_tips = Tip.query.is_type('method')
    basic_tips = Tip.query.is_type('basic')
    return render_template('add_tips.html', recipe=recipe)

@app.route('/upload_tip', methods=['GET', 'POST'])
def add_new_tip():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        # TODO: implement required fields and error handling.
        new_tip = dict_to_tip(request_dict)
        return render_template('upload_tip_success.html')
    return render_template('upload_tip_form.html')

@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def specific_recipe(recipe_id):
    if request.method == 'POST':
        return edit_recipe(recipe_id)
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_template.html', recipe=recipe)

@app.route('/tip/<tip_id>')
def specific_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    return render_template('tip_template.html', tip=tip)

