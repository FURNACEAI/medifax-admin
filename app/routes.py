from flask import render_template
from app import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = {'username': 'Miguel'}
    return render_template('login.html', title='Medifax Admin Login', user=user)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
