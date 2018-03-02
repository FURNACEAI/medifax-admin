import requests
import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import app
from app.models import User
from app.forms import LoginForm, AddEmployeeForm

@app.template_filter('ctime')
def timectime(s):
    return '2018-02-15'
    # return datetime.datetime.fromtimestamp(s).strftime('%m-%d')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        auth = user.auth(form.username.data, form.password.data)
        if not auth:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Medifax Admin Login', form=form)

@app.route('/employees/delete/<user_id>', methods=['GET'])
def delete_employee(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    url = "https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/%s" % user_id
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    r = requests.delete(url, headers=headers)
    flash('Success. The employee record was deleted.')
    return redirect(url_for('list_employees'))

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = AddEmployeeForm()
    if form.validate_on_submit():
        user = User()
        create = user.add(form.first_name.data, form.last_name.data, form.password.data, form.email.data, form.user_role.data, form.active.data)
        if create:
            flash("New employee created with the username %s" % form.email.data)
            return redirect(url_for('list_employees'))
        else:
            flash('Employee creation failed.')
    return render_template('employees/add.html', title='Add an Employee | Medifax', form=form)


@app.route('/employees', methods=['GET'])
def list_employees():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    # payload = json.dumps(payload)
    r = requests.get('https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/list', headers=headers)
    return render_template('employees/list.html', title='Employees | Medifax', data=r.json())

@app.route('/logout')
def logout():
    """
    Logs the user out of the admin panel
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Medifax Dashboard')
    else:
        return redirect(url_for('login'))
