from flask import Flask
from flask_mongoalchemy import MongoAlchemy
import os

app = Flask(__name__)

app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.environ.get("MONGODB_URI", 'mongodb://localhost')
app.config['MONGOALCHEMY_DATABASE'] = os.environ.get("MONGOALCHEMY_DATABASE", 'heroku_q47p17zb')

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", '1')
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL", None)
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS", None)

db = MongoAlchemy(app)

from app import routes

