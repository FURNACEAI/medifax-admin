import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'
