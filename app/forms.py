from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

STATE_ABBREV = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class AddEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_role = SelectField('Role', choices=[('admin','Admin'),('manager','Manager'), ('staff','Staff')], validators=[DataRequired()])
    active = SelectField('Active Account', choices=[('true',' Yes '),('false',' No ')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')

class CreateCustomerForm(FlaskForm):

    # Identity
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_initial = StringField('Middle Initial')
    last_name = StringField('Last Name', validators=[DataRequired()])
    # Contact
    email = StringField('Email', validators=[DataRequired()])
    home_phone = StringField('Home Phone')
    mobile_phone = StringField('Mobile Phone', validators=[DataRequired()])
    # Address
    street_address = StringField('Street Address', validators=[DataRequired()])
    street_address_2 = StringField('Street Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=STATE_ABBREV, validators=[DataRequired()])
    zipcode = StringField('ZIP', validators=[DataRequired()])
    # DOB
    dob = StringField('Date of Birth', validators=[DataRequired()])
    # Status
    active = SelectField('Active Account', choices=[('true',' Yes '),('false',' No ')], validators=[DataRequired()])
    # Actions
    submit = SubmitField('Create Customer')
