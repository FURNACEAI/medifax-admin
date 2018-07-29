from flask import Flask
from flask_login import LoginManager
# from config import Config

application = Flask(__name__)
application.config['SECRET_KEY'] = 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'

login = LoginManager(application)
from app import routes, models
