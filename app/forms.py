from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

STATE_ABBREV = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
                ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IO', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
                ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
                ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
                ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virgina'), ('WA', 'Washington'), ('WV', 'West Virgina'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

GENDER = [('Male', 'Male'), ('Female', 'Female')]

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
    """ """
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
    # active = SelectField('Active Account', choices=[('true',' Yes '),('false',' No ')], validators=[DataRequired()])
    # Actions
    submit = SubmitField('Create Customer')

class EditCustomerForm(CreateCustomerForm):
    blood_pressure_systolic = StringField('Blood Pressure Systolic')
    blood_pressure_diastolic = StringField('Blood Pressure Diastolic')
    heart_rate = StringField('Heart Rate')
    height = StringField('Height')
    weight = StringField('Weight')
    bmi = StringField('BMI')

    # Medications
    medication_name = StringField('Medication Name')
    medication_dose = StringField('Medication Dose')
    medication_freq = SelectField('Medication Frequency', choices=[('', 'Daily Frequency'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])

    gender = SelectField('Gender', choices=GENDER)
    patient_preferences = TextAreaField('Patient Preferences')
    patient_consents = TextAreaField('Patient Consents')
    family_history = TextAreaField('Family History')
