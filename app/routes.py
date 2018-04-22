from flask import render_template, jsonify
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app import app

@app.route('/')
@app.route('/index')
def index():

    return jsonify({"Name":"Kaitlyn"})