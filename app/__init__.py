from flask import Flask
from flask_login import LoginManager
#from config import Config
import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'

# TODO: Figure out why this isn't working later
# app.config.from_object(Config)

login = LoginManager(app)
from app import routes, models
