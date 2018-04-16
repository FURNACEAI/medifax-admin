import requests
import datetime
import os, sys
import json
from app import config as cfg
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import application
from app.models import User, Customer
from app.forms import LoginForm, AddEmployeeForm, CreateCustomerForm, EditCustomerForm

@application.template_global(name='zip')
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
    return common_entries(*args)

def common_entries(*dcts):
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield (i,) + tuple(d[i] for d in dcts)

@application.template_filter('ctime')
def timectime(s):
    """ Formats a Python timestamp to a human-readable format """
    return datetime.datetime.fromtimestamp(s).strftime('%m/%d/%Y')

@application.template_filter('lbreak')
def timectime(s):
    """ Formats a Python timestamp to a human-readable format """
    return "<br />".join(s.split("\n"))


@application.route('/login', methods=['GET', 'POST'])
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

""" LOGOUT """
@application.route('/logout')
def logout():
    """
    Logs the user out of the admin panel
    """
    logout_user()
    flash('You have been logged out of your session.')
    return redirect(url_for('login'))



""" EMPLOYEE > DELETE """
@application.route('/employees/delete/<user_id>', methods=['GET'])
def delete_employee(user_id):
    """ Delete the employee record and return the user back to the list of employees """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    url = "https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/%s" % user_id
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    r = requests.delete(url, headers=headers)
    flash('Success. The employee record was deleted.')
    return redirect(url_for('list_employees'))


""" EMPLOYEE > ADD """
@application.route('/employees/add', methods=['GET', 'POST'])
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


""" EMPLOYEE > LIST """
@application.route('/employees', methods=['GET'])
def list_employees():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    # payload = json.dumps(payload)
    r = requests.get('https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/list', headers=headers)
    return render_template('employees/list.html', title='Employees | Medifax', data=r.json())

""" CUSTOMER > LIST """
@application.route('/customers', methods=['GET'])
def list_customers():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    url = "%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['list'])
    r = requests.get(url, headers=headers)
    return render_template('customers/list.html', title='Customers | Medifax', data=r.json())


""" CUSTOMER > VIEW """
@application.route('/customers/view/<user_id>', methods=['GET'])
def view_customer(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    return render_template('customers/view.html', title='Customer Record | Medifax', data=r.json())

""" CUSTOMER > VIEW """
@application.route('/customers/upload/<user_id>/<img_type>/<img_filename>', methods=['GET', 'POST'])
def upload_customer(user_id, img_type, img_filename):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # http://127.0.0.1:5000/customers/upload/c85cf638-3aa0-11e8-8bb4-5e566f9ab6c7/medical/filename.jpg

    # Fetch a one-time URL for S3 upload
    payload = {
        "s3key": "%s" % (user_id)
    }
    payload = json.dumps(payload)
    url = "%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['onetimes3url'])
    r = requests.post(url, data=payload)
    req = r.json()
    return req['s3url']


    #form = EditCustomerForm() # HACK Upload form should be broken out to it's own form
    # filename = form.img_file.data.filename
    # form.img_file.data.save('uploads/' + filename)
    # On successful upload
    #return redirect("/customers/edit/%s" % form.user_id.data)



@application.route('/customers/edit/<user_id>', methods=['GET', 'POST'])
def edit_customer(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = EditCustomerForm()
    if form.validate_on_submit():
        user = Customer()
        update = user.edit(form, request.form)
        # print(update)
        if update:
            flash('Customer Record Updated')
        else:
            flash('Customer record update failed.')

    # Fetch the customer record
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    data = r.json()

    # Load the form data
    form.user_id.data = user_id
    form.first_name.data = data['name']['first']
    form.middle_initial.data = data['name']['middle_initial']
    form.last_name.data = data['name']['last']
    form.dob.data = data['dob']
    form.access_code.data = data['access_code']

    form.home_phone.data = data['phone']['home']
    form.mobile_phone.data = data['phone']['mobile']
    form.email.data = data['email']

    form.street_address.data = data['home_address']['street_address']
    form.street_address_2.data = data['home_address']['street_address_2']
    form.city.data = data['home_address']['city']
    form.state.data = data['home_address']['state']
    form.zipcode.data = data['home_address']['zipcode']

    form.gender.data = data['gender']
    form.height.data = data['height']
    form.weight.data = data['weight']
    form.heart_rate.data = data['heart_rate']
    form.bmi.data = data['bmi']
    # form.blood_type.data = data['blood_type']

    form.blood_pressure_systolic.data = data['blood_pressure_systolic']
    form.blood_pressure_diastolic.data = data['blood_pressure_diastolic']

    form.patient_preferences.data = data['patient_preferences']
    form.patient_consents.data = data['patient_consents']
    form.family_history.data = data['family_history']
    form.allergies.data = data['allergies']
    form.referrals.data = data['referrals']
    form.lab_results.data = data['lab_results']
    form.care_plan.data = data['care_plan']
    form.lifestyle_history.data = data['lifestyle_history']
    form.social_history.data = data['social_history']

    form.current_problems_0.data = data['current_problems_0']
    form.current_problems_1.data = data['current_problems_1']
    form.current_problems_2.data = data['current_problems_2']
    form.current_problems_3.data = data['current_problems_3']
    form.current_problems_4.data = data['current_problems_4']
    form.current_problems_5.data = data['current_problems_5']
    form.current_problems_6.data = data['current_problems_6']
    form.current_problems_7.data = data['current_problems_7']
    form.current_problems_8.data = data['current_problems_8']
    form.current_problems_9.data = data['current_problems_9']

    form.medication_name_0.data = data['medication_name_0']
    form.medication_name_1.data = data['medication_name_1']
    form.medication_name_2.data = data['medication_name_2']
    form.medication_name_3.data = data['medication_name_3']
    form.medication_name_4.data = data['medication_name_4']
    form.medication_name_5.data = data['medication_name_5']
    form.medication_name_6.data = data['medication_name_6']
    form.medication_name_7.data = data['medication_name_7']
    form.medication_name_8.data = data['medication_name_8']
    form.medication_name_9.data = data['medication_name_9']

    form.medication_dose_0.data = data['medication_dose_0']
    form.medication_dose_1.data = data['medication_dose_1']
    form.medication_dose_2.data = data['medication_dose_2']
    form.medication_dose_3.data = data['medication_dose_3']
    form.medication_dose_4.data = data['medication_dose_4']
    form.medication_dose_5.data = data['medication_dose_5']
    form.medication_dose_6.data = data['medication_dose_6']
    form.medication_dose_7.data = data['medication_dose_7']
    form.medication_dose_8.data = data['medication_dose_8']
    form.medication_dose_9.data = data['medication_dose_9']

    form.medication_freq_0.data = data['medication_freq_0']
    form.medication_freq_1.data = data['medication_freq_1']
    form.medication_freq_2.data = data['medication_freq_2']
    form.medication_freq_3.data = data['medication_freq_3']
    form.medication_freq_4.data = data['medication_freq_4']
    form.medication_freq_5.data = data['medication_freq_5']
    form.medication_freq_6.data = data['medication_freq_6']
    form.medication_freq_7.data = data['medication_freq_7']
    form.medication_freq_8.data = data['medication_freq_8']
    form.medication_freq_9.data = data['medication_freq_9']

    # Dental
    form.dentist_name.data = data['dentist_name']
    form.dentist_email.data = data['dentist_email']
    form.dentist_phone.data = data['dentist_phone']
    form.dental_condition.data = data['dental_condition']

    # Dental Insurance
    form.ins_planid_dental.data = data['ins_planid_dental']
    form.ins_provider_dental.data = data['ins_provider_dental']
    form.ins_street_addr_dental.data = data['ins_street_addr_dental']
    form.ins_city_dental.data = data['ins_city_dental']
    form.ins_state_dental.data = data['ins_state_dental']
    form.ins_zipcode_dental.data = data['ins_zipcode_dental']
    form.ins_phone_dental.data = data['ins_phone_dental']
    form.ins_email_dental.data = data['ins_email_dental']

    # Medical Insurance
    form.ins_planid_med.data = data['ins_planid_med']
    form.ins_provider_med.data = data['ins_provider_med']
    form.ins_street_addr_med.data = data['ins_street_addr_med']
    form.ins_city_med.data = data['ins_city_med']
    form.ins_state_med.data = data['ins_state_med']
    form.ins_zipcode_med.data = data['ins_zipcode_med']
    form.ins_phone_med.data = data['ins_phone_med']
    form.ins_email_med.data = data['ins_email_med']


    return render_template('customers/edit.html', access_code=data['access_code'], title='Customer Record | Medifax', form=form, data=data)

""" CUSTOMER > ADD """
@application.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CreateCustomerForm()
    if form.validate_on_submit():
        user = Customer()
        create = user.create(form)
        if create:
            flash("New customer created with the email: %s" % form.email.data)
            url = "/customers"
            return redirect(url)
        else:
            flash('Employee creation failed.')
    return render_template('customers/add.html', title='Add a Customer | Medifax', form=form)

""" EMPLOYEE > DELETE """
@application.route('/customers/delete/<user_id>', methods=['GET'])
def delete_customer(user_id):
    """ Delete the customer record and return the user back to the list of employees """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'], cfg._AWS['status'], cfg._AWS['customers']['delete'], user_id)
    print(url)
    r = requests.delete(url, headers=cfg._AWS['headers'])
    flash('The customer record was deleted.')
    return redirect(url_for('list_customers'))

@application.route('/images/upload')
def upload():
    if current_user.is_authenticated:
        bucket = 'medifax-customers-images-dev'
    else:
        return redirect(url_for('login'))


@application.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Medifax Dashboard')
    else:
        return redirect(url_for('login'))

@application.route('/')
@application.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('list_customers'))
        # return render_template('dashboard.html', title='Medifax Dashboard')
    else:
        return redirect(url_for('login'))
