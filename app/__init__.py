from flask import Flask
from flask_mongoalchemy import MongoAlchemy
import os

app = Flask(__name__)
# app.config['MONGOALCHEMY_DATABASE'] = 'recipes'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.environ.get("MONGODB_URI", None)

app.config['MONGOALCHEMY_DATABASE'] = 'heroku_q47p17zb'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.environ["MONGODB_URI"]

db = MongoAlchemy(app)

from app import routes

